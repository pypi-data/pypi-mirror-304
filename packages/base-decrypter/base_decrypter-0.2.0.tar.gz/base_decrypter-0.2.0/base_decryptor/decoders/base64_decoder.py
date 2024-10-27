import base64


def decode_base64(encoded_string):
    """
    Decodes a given base64 encoded string.

    Parameters
    ----------
    encoded_string: str
        The base64 encoded string to be decoded.

    Returns
    -------
    A tuple containing the name of the encoding and the decoded string.
    If decoding failed, the second element of the tuple is an error message.
    """
    try:
        decoded = base64.b64decode(encoded_string).decode('utf-8')
        if decoded.isprintable():
            return "Base64", decoded
    except Exception as e:
        return "Base64", f"Error decoding Base64: {str(e)}"
