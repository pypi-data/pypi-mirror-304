import base64


def decode_base85(encoded_string):
    try:
        decoded = base64.b85decode(encoded_string).decode()
        return "Base85", decoded
    except Exception as e:
        return "Base85", f"Error decoding Base85: {str(e)}"
