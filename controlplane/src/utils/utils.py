def string_to_bool(value: str) -> bool:
    if isinstance(value, bool):
        return value
    return value.lower() in ["true", "1", "t", "y", "yes"]
