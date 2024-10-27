import base45


def decode_base45(encoded_string):
    """
    Decodes a Base45 encoded string into a UTF-8 string.

    Parameters
    ----------
    encoded_string : str
        The Base45 encoded string to be decoded.

    Returns
    -------
    (str, str)
        A tuple containing the encoding type and the decoded string.
        The encoding type is always "Base45".
    """
    try:
        # Decode the Base45 string using the base45 library
        decoded_bytes = base45.b45decode(encoded_string)
        decoded_string = decoded_bytes.decode('utf-8')
        return "Base45", decoded_string
    except Exception as e:
        return "Base45", f"Error decoding Base45: {str(e)}"
