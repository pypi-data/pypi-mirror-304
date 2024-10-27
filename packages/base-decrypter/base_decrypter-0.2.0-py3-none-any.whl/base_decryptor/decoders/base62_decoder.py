import base62


def decode_base62(encoded_string):
    """
    Decodes a Base62 encoded string to a UTF-8 string.

    Args:
        encoded_string (str): A string encoded in Base62.

    Returns:
        tuple: A tuple containing the decoding type and the decoded string.
    """
    try:
        # Decode the Base62 string using the pybase62 library
        decoded_bytes = base62.decodebytes(encoded_string)
        decoded_string = decoded_bytes.decode('utf-8')
        return "Base62", decoded_string
    except Exception as e:
        return "Base62", f"Error decoding Base62: {str(e)}"
