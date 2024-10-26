import base64


def decode_base85(encoded_string):
    """
    Decodes a Base85 encoded string.

    Args:
        encoded_string (str): The Base85 encoded string to decode.

    Returns:
        tuple: A tuple containing the type of encoding ("Base85") and the decoded string.
               If decoding fails, the second element of the tuple is an error message.
    """
    try:
        decoded = base64.b85decode(encoded_string).decode()
        return "Base85", decoded
    except Exception as e:
        return "Base85", f"Error decoding Base85: {str(e)}"
