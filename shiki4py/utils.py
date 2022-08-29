from typing import Any, Dict


def prepare_params(**params: Dict[str, Any]) -> Dict[str, Any]:
    cleared_params = dict()
    for key, value in params.items():
        if value == None:
            continue
        elif isinstance(value, bool):
            cleared_params[key] = int(value)
        else:
            cleared_params[key] = value
    return cleared_params


def prepare_json(json: Dict[str, Any]) -> Dict[str, Any]:
    cleared_json = dict()
    for key, value in json.items():
        if value == None:
            continue
        elif isinstance(value, dict):
            nested_cleared_json = prepare_json(value)
            if len(nested_cleared_json) > 0:
                cleared_json[key] = nested_cleared_json
        else:
            cleared_json[key] = value
    return cleared_json
