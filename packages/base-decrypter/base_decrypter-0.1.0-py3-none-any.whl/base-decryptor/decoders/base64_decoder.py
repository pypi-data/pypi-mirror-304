import base64


def decode_base64(encoded_string):
    try:
        decoded = base64.b64decode(encoded_string).decode('utf-8')
        if decoded.isprintable():
            return "Base64", decoded
    except Exception as e:
        return "Base64", f"Error decoding Base64: {str(e)}"
