import base62


def decode_base62(encoded_string):
    try:
        # Decode the Base62 string using the pybase62 library
        decoded_bytes = base62.decodebytes(encoded_string)
        decoded_string = decoded_bytes.decode('utf-8')
        return "Base62", decoded_string
    except Exception as e:
        return "Base62", f"Error decoding Base62: {str(e)}"
