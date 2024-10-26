import base45


def decode_base45(encoded_string):
    try:
        # Decode the Base45 string using the base45 library
        decoded_bytes = base45.b45decode(encoded_string)
        decoded_string = decoded_bytes.decode('utf-8')
        return "Base45", decoded_string
    except Exception as e:
        return "Base45", f"Error decoding Base45: {str(e)}"
