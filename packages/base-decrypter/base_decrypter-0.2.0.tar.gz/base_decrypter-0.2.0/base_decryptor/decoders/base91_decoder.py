import base91


def decode_base91(encoded_string):
    """
    Decodes a Base91 encoded string.

    Parameters
    ----------
    encoded_string : str
        The Base91 encoded string to decode.

    Returns
    -------
    tuple
        A tuple with the type of encoding as the first element and the decoded
        string as the second element. If there is an error decoding the string,
        the error message is returned as the second element of the tuple.
    """
    try:
        decoded = base91.decode(encoded_string).decode()
        return "Base91", decoded
    except Exception as e:
        return "Base91", f"Error decoding Base91: {str(e)}"
