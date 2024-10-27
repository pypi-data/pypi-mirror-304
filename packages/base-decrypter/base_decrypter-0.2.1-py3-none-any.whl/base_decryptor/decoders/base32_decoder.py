import base64


def decode_base32(encoded_string):
    """
    Decodes a given base32 encoded string.

    Parameters
    ----------
    encoded_string: str
        The base32 encoded string to be decoded.

    Returns
    -------
    tuple
        A tuple containing two elements. The first element is
        a string describing the type of decoding done, and the second
        element is either the decoded string or an error message.
    """
    try:
        decoded = base64.b32decode(encoded_string).decode('utf-8')
        return "Base32", decoded
    except Exception as e:
        return "Base32", f"Error decoding Base32: {str(e)}"
