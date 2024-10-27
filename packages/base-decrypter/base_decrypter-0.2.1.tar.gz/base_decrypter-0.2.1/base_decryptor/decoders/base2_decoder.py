# base2_decoder.py

def decode_base2(encoded_string):
    """
    Decodes a Base2 (binary) encoded string.

    Args:
        encoded_string (str): The binary-encoded string to decode.

    Returns:
        str: The decoded plain text.
    """
    try:
        # Remove any whitespace (e.g., spaces) from the binary string
        sanitized_string = encoded_string.replace(" ", "")

        # Split the binary string into chunks of 8 bits (1 byte)
        bytes_list = [sanitized_string[i:i + 8] for i in range(0, len(sanitized_string), 8)]

        # Convert each byte to a character
        decoded_string = ''.join([chr(int(byte, 2)) for byte in bytes_list])

        return "Base2 (Binary)", decoded_string

    except Exception as e:
        return "Base2 (Binary)", f"Error decoding Base2: {str(e)}"
