import os
from typing import Any

import numpy as np
import tensorflow as tf
import tflite


def estimate_flops_tflite(model_path: str) -> float:
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


def estimate_parameters_tflite(model_path: str) -> int:
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


def get_stats_tflite(model_path: str) -> tuple[str, dict[str, Any]]:
    # Get model name
    model_name = os.path.splitext(os.path.basename(model_path))[0]
    model_name = model_name.replace(".", "-")
    # everything after the first dash is the version, but there can be multiple dashes
    # in the name, so we need to split on the first dash
    model_name, model_version = model_name.split("_", 1)

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

    # Get types of the tensors in the model
    dtype_map = {
        np.float32: "fp32",
        np.float64: "fp64",
        np.float16: "fp16",
        np.uint8: "int8",
        np.uint16: "int16",
        np.uint32: "int32",
        np.uint64: "int64",
        np.int8: "int8",
        np.int16: "int16",
        np.int32: "int32",
        np.int64: "int64",
        np.bool_: "bool",
        np.complex64: "c64",
        np.complex128: "c128",
    }
    tensor_types = set([t["dtype"] for t in interpreter.get_tensor_details()])
    tensor_types = [dtype_map[t] for t in tensor_types if t in dtype_map]
    tensor_types = sorted(tensor_types)

    # Get model precision
    precision = 4
    if "fp16" in tensor_types or "int16" in tensor_types:
        precision = 2  # fp16 is quantized to 2 decimal places
    elif "int8" in tensor_types:
        precision = 1  # int8 is quantized to 1 decimal place

    # Estimate number of GFLOPs
    mflops = estimate_flops_tflite(model_path) / 1e6

    # Estimate number of parameters
    params = estimate_parameters_tflite(model_path) / 1e6

    return model_name, {
        model_version: {
            "inputs": input_shapes,
            "outputs": output_shapes,
            "precision": precision,
            "file_size": model_size,
            "flops": mflops,
            "params": params,
        }
    }
