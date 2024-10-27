import argparse
import json
import os

import numpy as np
import tensorflow as tf
import tflite
from tabulate import tabulate

from pocketpose.apis import create_model, list_models


def parse_args():
    parser = argparse.ArgumentParser("Prints statistics about TFLite models")
    parser.add_argument(
        "--save_file",
        type=str,
        required=False,
        default="./results/analysis/tflite_models.json",
        help="Path to save results",
    )
    return parser.parse_args()


def estimate_flops(model_path):
    """Estimates the number of floating point operations in a TFLite model.

    Note: This is a rough estimate which only considers CONV_2D, DEPTHWISE_CONV_2D,
    FULLY_CONNECTED, ADD, and MUL operators.

    For FULLY_CONNECTED layer, we assume that the number of FLOPs is approximately 2
    times the number of elements in the weight matrix, which assumes that each weight
    participates in one multiplication and one addition.

    For ADD and MUL layers, we assume that each operation is performed element-wise,
    and so the number of FLOPs is equal to the total number of elements in the
    input tensor.

    Args:
        model_path (str): Path to TFLite model

    Returns:
        float: Number of estimated GFLOPs in the model
    """
    with open(model_path, "rb") as f:
        buf = f.read()
        model = tflite.Model.GetRootAsModel(buf, 0)

    graph = model.Subgraphs(0)

    total_flops = 0.0
    for i in range(graph.OperatorsLength()):
        op = graph.Operators(i)
        op_code = model.OperatorCodes(op.OpcodeIndex())
        op_code_builtin = op_code.BuiltinCode()

        op_opt = op.BuiltinOptions()

        flops = 0.0
        if op_code_builtin == tflite.BuiltinOperator.CONV_2D:
            filter_shape = graph.Tensors(op.Inputs(1)).ShapeAsNumpy()
            out_shape = graph.Tensors(op.Outputs(0)).ShapeAsNumpy()
            opt = tflite.Conv2DOptions()
            opt.Init(op_opt.Bytes, op_opt.Pos)
            flops = (
                2
                * out_shape[1]
                * out_shape[2]
                * filter_shape[0]
                * filter_shape[1]
                * filter_shape[2]
                * filter_shape[3]
            )

        elif op_code_builtin == tflite.BuiltinOperator.DEPTHWISE_CONV_2D:
            filter_shape = graph.Tensors(op.Inputs(1)).ShapeAsNumpy()
            out_shape = graph.Tensors(op.Outputs(0)).ShapeAsNumpy()
            flops = (
                2
                * out_shape[1]
                * out_shape[2]
                * filter_shape[0]
                * filter_shape[1]
                * filter_shape[2]
                * filter_shape[3]
            )

        elif op_code_builtin == tflite.BuiltinOperator.FULLY_CONNECTED:
            weight_shape = graph.Tensors(op.Inputs(1)).ShapeAsNumpy()
            flops = 2 * np.prod(weight_shape)

        elif (
            op_code_builtin == tflite.BuiltinOperator.ADD
            or op_code_builtin == tflite.BuiltinOperator.MUL
        ):
            input_shape = graph.Tensors(op.Inputs(0)).ShapeAsNumpy()
            flops = np.prod(input_shape)

        total_flops += flops

    return total_flops


def estimate_parameters(model_path):
    """Estimates the number of parameters in a TFLite model.

    Args:
        model_path (str): Path to TFLite model

    Returns:
        int: Number of parameters in the model
    """
    with open(model_path, "rb") as f:
        buf = f.read()
        model = tflite.Model.GetRootAsModel(buf, 0)

    graph = model.Subgraphs(0)

    total_params = 0
    for i in range(graph.OperatorsLength()):
        op = graph.Operators(i)
        op_code = model.OperatorCodes(op.OpcodeIndex())
        op_code_builtin = op_code.BuiltinCode()

        params = 0
        if op_code_builtin in {
            tflite.BuiltinOperator.CONV_2D,
            tflite.BuiltinOperator.DEPTHWISE_CONV_2D,
            tflite.BuiltinOperator.FULLY_CONNECTED,
        }:
            # The weights are the second input tensor for these ops
            weights = graph.Tensors(op.Inputs(1)).ShapeAsNumpy()
            params += np.prod(weights)

            # Check if there are biases, which is the third input tensor for these ops
            if op.InputsLength() > 2:
                biases = graph.Tensors(op.Inputs(2)).ShapeAsNumpy()
                params += np.prod(biases)

        total_params += params

    return total_params


def get_stats(model_path):
    # Load TFLite model and allocate tensors.
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    # Get input details
    input_shapes = []
    input_details = interpreter.get_input_details()
    for input in input_details:
        shape = input["shape"][1:]
        formatted_shape = "x".join(map(str, shape))
        input_shapes.append(formatted_shape)

    # Get output details
    output_shapes = []
    output_details = interpreter.get_output_details()
    for output in output_details:
        shape = output["shape"][1:]
        formatted_shape = "x".join(map(str, shape))
        output_shapes.append(formatted_shape)

    # Get total size of the model file
    model_size = os.path.getsize(model_path)
    model_size = model_size / float(1 << 20)  # Convert to MB

    # Estimate number of GFLOPs
    mflops = estimate_flops(model_path) / 1e9

    # Estimate number of parameters
    params = estimate_parameters(model_path) / 1e6

    return {
        "inputs": input_shapes,
        "outputs": output_shapes,
        "file_size": model_size,
        "params": params,
        "flops": mflops,
    }


def stats_to_table(current_stats, format="github"):
    table = []
    headers = [
        "Model",
        "Input Size",
        "Output Size",
        "Size (MB)",
        "Params (M)",
        "FLOPs (G)",
    ]
    for model_name, model_stats in current_stats.items():
        inputs = ", ".join(model_stats["inputs"])
        outputs = ", ".join(model_stats["outputs"])
        file_size = f"{model_stats['file_size']:.2f}"
        params = f"{model_stats['params']:.2f}"
        flops = f"{model_stats['flops']:.2f}"
        table.append([model_name, inputs, outputs, file_size, params, flops])

    # Write the stats to the README file
    return tabulate(table, headers=headers, tablefmt=format)


def main():
    args = parse_args()
    models = list_models(filter="format", filter_value="tflite", with_info=True)

    current_stats = {}
    for m in models:
        try:
            # Build the model (downloads if necessary)
            model_key = list(m.keys())[0]
            model_info = m[model_key]
            model = create_model(model_key)

            # Get stats for the model
            model_name = model_info["name"]
            model_stats = get_stats(model.model_path)
            current_stats[model_name] = model_stats
        except Exception as e:
            print(f"Failed to get stats for {m}: {e}")
            import traceback

            traceback.print_exc()

    # Update the JSON file with the stats
    json_path = args.save_file
    save_dir = os.path.dirname(json_path)
    os.makedirs(save_dir, exist_ok=True)
    existing_stats = {}
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            existing_stats = json.load(f)

    # Merge the existing stats with the new stats
    existing_stats.update(current_stats)
    existing_stats = dict(sorted(existing_stats.items()))

    # Write the stats to the JSON file
    with open(json_path, "w") as f:
        json.dump(existing_stats, f, indent=2)

    # Write current stats to the README file
    stats = stats_to_table(current_stats, format="github")
    stats_path = os.path.join(save_dir, "README.md")
    with open(stats_path, "w") as f:
        f.write("# Model Analysis (TFLite)\n\n")
        f.write(
            "This table contains the size and performance metrics for different variants of the model.\n\n"
        )
        f.write(stats)
        f.write("\n\n## License\n\n")
        f.write("This work is licensed under the Apache 2.0 License.\n\n")

    # Write all stats to a .md file in the same directory as the JSON file
    stats = stats_to_table(existing_stats, format="github")
    stats_path = os.path.splitext(json_path)[0] + ".md"
    with open(stats_path, "w") as f:
        f.write(stats)


if __name__ == "__main__":
    main()
