import pybase100


def decode_base100(encoded_string):
    """
    Decodes a Base100 encoded string.

    Args:
        encoded_string (str): A Base100 encoded string.

    Returns:
        tuple: A tuple containing the name of the encoding used and the decoded string.
    """
    try:
        decoded = pybase100.decode(encoded_string)
        return "Base100", decoded.decode()
    except Exception as e:
        return "Base100", f"Error decoding Base100: {str(e)}"


