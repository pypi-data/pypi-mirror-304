# spicy_ids/utils/get_object_type.py

from datetime import datetime


def get_object_type(spicy_id: str) -> None:
    COMMON_OBJECT_TYPES: dict[str, str] = {
        "obj": "object",
        "tbl" : "table",
        "vw": "view",
        "rec": "record",
        "lst": "list",
    }
    spicy_str: str = str(spicy_id)
    # logger.debug(f"{spicy_str = }")
    obj_type: str = spicy_str[:spicy_str.find("_", 0)]
    # logger.debug(f"{obj_type = }")
    try:
        obj_val: str = COMMON_OBJECT_TYPES.get(obj_type)
        obj_type: str = f"Object type is {obj_val}"
    except KeyError:
        obj_type: str = f"Uncommon type. Prefix found is {obj_type}"
    return obj_type


def get_object_timestamp(spicy_id: str) -> str:
    spicy_str: str = str(spicy_id)
    timestamped_fg: bool | str = False if spicy_str.find("-", 0) == -1 else spicy_str.find("-", 0)
    if not timestamped_fg:
        raise ValueError("The provided Spicy Id is not timestamped.")
    timestamp: int = int(int(spicy_str[spicy_str.find("-", 0) + 1:]) / 4024)
    # logger.debug(f"{timestamp}")
    date_unfmt: datetime = datetime.fromtimestamp(timestamp)
    date_ts: str = datetime.strftime(date_unfmt, "%Y-%m-%d")
    # logger.debug(f"{date_ts = }")
    return date_ts
