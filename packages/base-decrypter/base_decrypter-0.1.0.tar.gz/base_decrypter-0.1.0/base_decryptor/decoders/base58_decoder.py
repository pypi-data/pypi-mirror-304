import base58


def decode_base58(encoded_string):
    """
    Decodes a Base58 encoded string.

    Parameters
    ----------
    encoded_string : str
        The Base58 encoded string to decode.

    Returns
    -------
    tuple
        A tuple with the type of encoding as the first element and the decoded
        string as the second element. If there is an error decoding the string,
        the error message is returned as the second element of the tuple.
    """
    try:
        decoded = base58.b58decode(encoded_string).decode('utf-8')
        return "Base58", decoded
    except Exception as e:
        return "Base58", f"Error decoding Base58: {str(e)}"
