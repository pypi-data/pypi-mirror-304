import base58


def decode_base58(encoded_string):
    try:
        decoded = base58.b58decode(encoded_string).decode('utf-8')
        return "Base58", decoded
    except Exception as e:
        return "Base58", f"Error decoding Base58: {str(e)}"
