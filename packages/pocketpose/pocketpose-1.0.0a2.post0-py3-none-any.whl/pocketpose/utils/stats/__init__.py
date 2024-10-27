""" The module for computing model statistics. """

from .tflite import estimate_flops_tflite, estimate_parameters_tflite, get_stats_tflite


def tabulate_stats(statistics):
    """Converts raw statistics into list of dictionaries.

    Args:
        statistics (dict): The raw statistics.

    Returns:
        list of dict: The statistics in a tabular format. These can be
                      directly written to a table using the `tabulate` package
                      or the `write_to_table` function in `io` module.
    """
    table = []
    for model_name, model_variants in statistics.items():
        for variant_name, model_stats in model_variants.items():
            inputs = ", ".join(model_stats["inputs"])
            outputs = ", ".join(model_stats["outputs"])
            precision = str(model_stats["precision"])
            file_size = f"{model_stats['file_size']:.2f}"
            flops = f"{model_stats['flops']:.2f}"
            params = f"{model_stats['params']:.2f}"
            table.append(
                {
                    "Model": model_name,
                    "Variant": variant_name,
                    "Inputs": inputs,
                    "Outputs": outputs,
                    "Precision": precision,
                    "Size (MB)": file_size,
                    "FLOPs (M)": flops,
                    "Params (M)": params,
                }
            )

    return table


__all__ = [
    "estimate_flops_tflite",
    "estimate_parameters_tflite",
    "get_stats_tflite",
    "tabulate_stats",
]
