from typing import Dict

from sysgym.envs.rocksdb.parsers.constant_types import NUM_VALUE


def clean_key(k):
    return (
        k.strip()
        .lower()
        .replace(")", "")
        .replace(" ", "_")
        .replace("(", "_")
        .replace(".", "_")
    )


def merge_dictionary(some_dict: Dict, other_dict: Dict) -> Dict:
    return {**some_dict, **other_dict}


def parse_number_in_string(string_num: str) -> NUM_VALUE:
    try:
        if "." in string_num:
            num = float(string_num)
        else:
            num = int(string_num)
        return num

    except ValueError as e:
        raise ValueError(f"Casting {string_num} caused: {e}")


def ensure_value_in_mb(value: str, measurement: str):
    # TODO this is hacky surely there is a library for this but w/e
    measurement = measurement.lower()
    if "m" in measurement:
        measurement_multiplier = 1
    elif "k" in measurement:
        measurement_multiplier = 0.001
    elif "g" in measurement:
        measurement_multiplier = 1000
    else:
        raise ValueError(
            f"Received {measurement} as measurement: converting to MB failed"
        )
    return float(value) * measurement_multiplier
