import base64


def decode_base32(encoded_string):
    try:
        decoded = base64.b32decode(encoded_string).decode('utf-8')
        return "Base32", decoded
    except Exception as e:
        return "Base32", f"Error decoding Base32: {str(e)}"
