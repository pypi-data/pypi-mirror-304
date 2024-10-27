from typing import List, Optional, Union

import tabulate

from .registry import POSE_ESTIMATORS


def list_models(
    filter: Optional[str] = None,
    filter_value: Optional[str] = None,
    with_info: bool = False,
) -> Union[str, List[str]]:
    """
    List available pose estimation models with optional filtering and detailed information.

    Args:
        filter (Optional[str]): The attribute to filter models by. Supported filters are
            "format", "skeleton", "runner", and "license".
        filter_value (Optional[str]): The value corresponding to the filter to apply.
        with_info (bool): If True, include detailed information about each model in the output.

    Returns:
        Union[str, List[str]]:
            - If `with_info` is True, returns a formatted table string of models (filtered if applicable).
            - If `with_info` is False, returns a list of model names (filtered if applicable).

    Raises:
        ValueError: If an unsupported filter is provided or if a filter is specified without a value.
    """
    supported_filters = {"format", "skeleton", "runner", "license"}

    # Validate filter arguments
    if filter is not None:
        if filter not in supported_filters:
            raise ValueError(
                f"Filter '{filter}' is not supported. Supported filters are: {sorted(supported_filters)}"
            )
        if filter_value is None:
            raise ValueError(
                "A filter value must be provided when a filter is specified."
            )

    # Determine if model information needs to be retrieved
    need_info = with_info or filter is not None

    # Retrieve all available model names
    model_names = POSE_ESTIMATORS.list()

    if not need_info:
        # No additional information or filtering required; return the list of model names
        return model_names

    # Collect model information
    model_info = {}
    for model_name in model_names:
        try:
            # Initialize the model in info mode to retrieve its information
            model = create_model(model_name, info_mode=True)
            info = model.get_info()
            model_info[model_name] = info
        except Exception as e:
            # Log the error and skip the model if it fails to initialize
            # Replace this with appropriate logging as needed
            print(f"Warning: Failed to retrieve info for model '{model_name}': {e}")
            continue

    # Apply filtering if specified
    if filter and filter_value:
        filtered_models = {
            name: info
            for name, info in model_info.items()
            if info.get(filter, "").lower() == filter_value.lower()
        }
    else:
        filtered_models = model_info

    if with_info:
        # Prepare data for tabulation
        table = [
            [
                name,
                info.get("format", "N/A"),
                info.get("skeleton", "N/A"),
                info.get("runner", "N/A"),
                info.get("license", "N/A"),
            ]
            for name, info in filtered_models.items()
        ]

        headers = ["Model", "Format", "Skeleton", "Runner", "License"]
        info = tabulate.tabulate(table, headers=headers, tablefmt="grid")
        return list(filtered_models.keys()), info
    else:
        # Return the list of filtered model names
        return list(filtered_models.keys())


def create_model(model_name, *args, **kwargs):
    """Create a model from its name."""
    return POSE_ESTIMATORS.build(model_name, *args, **kwargs)
