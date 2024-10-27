import base64


def decode_urlsafe_base64(encoded_string):
    """
    Decodes a URL-safe base64 string.

    URL-safe base64 strings are the same as regular base64 strings except that
    they use '-' and '_' instead of '+' and '/' respectively. This is useful for
    passing base64 strings in URLs.

    Parameters
    ----------
    encoded_string : str
        The URL-safe base64 string to decode.

    Returns
    -------
    tuple
        A tuple containing the encoding type and the decoded string.
    """
    try:
        # Add padding if necessary
        padding_needed = len(encoded_string) % 4
        if padding_needed:
            encoded_string += '=' * (4 - padding_needed)

        # Decode the URL-safe base64 string
        decoded_bytes = base64.urlsafe_b64decode(encoded_string)
        return "Base64 (URL Safe)", decoded_bytes.decode('utf-8')

    except Exception as e:
        return "Base64 (URL Safe)", f"Error: {e}"
