import base91


def decode_base91(encoded_string):
    try:
        decoded = base91.decode(encoded_string).decode()
        return "Base91", decoded
    except Exception as e:
        return "Base91", f"Error decoding Base91: {str(e)}"
