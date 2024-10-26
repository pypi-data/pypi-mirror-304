import pybase100


def decode_base100(encoded_string):
    try:
        decoded = pybase100.decode(encoded_string)
        return "Base100", decoded.decode()
    except Exception as e:
        return "Base100", f"Error decoding Base100: {str(e)}"


