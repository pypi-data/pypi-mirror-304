# spicy_ids/generate_spicy_id.py

from .generate_random_strings import generate_random_string
from .generate_timestamp_value import get_masked_ts


class SpicyId:
    def __init__(self, obj_type: str, length: int, timestamp: bool = False) -> None:
        self.obj_type: str = obj_type
        self.length: int = length
        self.timestamp = timestamp
        valid_fg: bool = self.__validate__()
        if valid_fg:
            self.value = self.generator()
        return None

    def __repr__(self):
        repr: str = f"Spicy Id, object type '{self.obj_type}', timestampped: {self.timestamp}"
        return repr

    def __str__(self):
        return self.value

    def __validate__(self) -> bool:
        if not isinstance(self.obj_type, str):
            raise TypeError(f"Invalid object format. Expected 'str', found '{type(self.obj_type)}'")
        if not isinstance(self.length, int):
            raise TypeError("Invalid length for spicy id")
        if self.length > 50:
            raise ValueError("Excessive spicy id length. length value must be below 50 chars.")
        return True

    def generator(self) -> str:
        random_string: str = generate_random_string(length=self.length)
        object_string: str = self.obj_type
        if self.timestamp:
            masked_timestamp: str = get_masked_ts()
            spicy_id: str = f"{object_string}_{random_string}-{masked_timestamp}"
        else:
            spicy_id: str = f"{object_string}_{random_string}"
        return spicy_id
