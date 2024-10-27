# spicy_ids/generate_random_strings.py

from random import sample
from string import ascii_lowercase, ascii_uppercase, digits
from typing import LiteralString


def generate_random_string(length: int = 15) -> str:
    if length is None:
        raise SyntaxError("The 'length' parameter is required")
    if not isinstance(length, int) and not isinstance(length, float):
        raise TypeError(f"The 'length' parameter is from an incompatible type. Expected 'int' or 'float', got '{type(length)}'")
    length: int = int(length)
    str_space: LiteralString = ascii_lowercase + ascii_uppercase + digits
    rnd_str: str = "".join(sample(population=str_space, k=length))
    # logger.debug(f"{rnd_str = }")
    return rnd_str


def main() -> None:
    return None


if __name__ == "__main__":
    main()
else:
    pass
