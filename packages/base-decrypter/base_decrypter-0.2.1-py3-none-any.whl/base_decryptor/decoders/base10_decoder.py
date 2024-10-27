# base10_decoder.py

def decode_base10(encoded_string):
    """
    Decodes a Base10 (decimal) encoded string.

    Args:
        encoded_string (str): The decimal-encoded string to decode.

    Returns:
        str: The decoded plain text.
    """
    try:
        # Split the encoded string by spaces to get individual numbers
        decimal_values = encoded_string.split()

        # Convert each decimal value to a character
        decoded_string = ''.join([chr(int(num)) for num in decimal_values])

        return "Base10 (Decimal)", decoded_string

    except Exception as e:
        return "Base10 (Decimal)", f"Error decoding Base10: {str(e)}"
