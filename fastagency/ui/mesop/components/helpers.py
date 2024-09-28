def darken_hex_color(hex_color: str, factor: float = 0.8) -> str:
    """Darkens a hex color by a given factor.

    Args:
    hex_color: The hex color code (e.g., '#FF0000').
    factor: The darkening factor (0.0 to 1.0, where 1.0 is no change and 0.0 is completely dark).

    Returns:
    The darkened hex color code.
    """
    # Remove the '#' prefix if it exists
    hex_color = hex_color.lstrip("#")

    if len(hex_color) == 3:
        hex_color = "".join(char * 2 for char in hex_color)

    # Convert hex to RGB values
    rgb = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    # Darken each component
    darkened_rgb = tuple(int(channel * factor) for channel in rgb)

    # Convert back to hex
    darkened_hex = "#{:02X}{:02X}{:02X}".format(*darkened_rgb)

    return darkened_hex
