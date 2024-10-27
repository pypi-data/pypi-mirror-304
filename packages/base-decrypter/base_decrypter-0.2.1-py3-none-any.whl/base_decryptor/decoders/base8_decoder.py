# base8_decoder.py

def decode_base8(encoded_string):
    """
    Decodes a Base8 (octal) encoded string.

    Args:
        encoded_string (str): The octal-encoded string to decode.

    Returns:
        str: The decoded plain text.
    """
    try:
        # Split the encoded string by spaces to get individual octal values
        octal_values = encoded_string.split()

        # Convert each octal value to a character
        decoded_string = ''.join([chr(int(num, 8)) for num in octal_values])

        return "Base8 (Octal)", decoded_string

    except Exception as e:
        return "Base8 (Octal)", f"Error decoding Base8: {str(e)}"
