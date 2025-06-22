def hex_to_rgb(hex_code):
    """
    Convert hex color code to RGB tuple

    Args:
        hex_code: String like "#FF0000" or "FF0000"

    Returns:
        tuple: (r, g, b) values from 0-255
    """
    # Remove the # if present
    hex_code = hex_code.lstrip("#")

    # Convert to RGB
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))