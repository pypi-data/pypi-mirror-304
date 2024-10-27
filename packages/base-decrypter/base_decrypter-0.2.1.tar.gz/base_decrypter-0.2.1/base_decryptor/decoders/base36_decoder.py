import base36


def decode_base36(encoded_string):
    try:
        # Ensure the input is treated as a string
        encoded_string = encoded_string.replace(" ", "")  # Remove spaces if any
        decoded_value = int(encoded_string, 36)  # Decode using base36

        # Custom decoding back to text (assuming it represents ASCII characters)
        decoded_string = ''
        while decoded_value > 0:
            decoded_string = chr(decoded_value % 256) + decoded_string
            decoded_value //= 256

        # Return the type and decoded value
        return "Base36", str(decoded_string)
    except Exception as e:
        return "Base36", f"Error: {str(e)}"
