import struct


def decode_ascii85(data):
    """
    Decodes an ASCII85 encoded string.

    Parameters
    ----------
    data : str
        The ASCII85 encoded string to decode.

    Returns
    -------
    tuple
        A tuple with the type of encoding as the first element and the decoded
        byte string as the second element. If there is an error decoding the
        string, the error message is returned as the second element of the tuple.
    """
    try:
        # Convert the input string to bytes using ASCII encoding
        if isinstance(data, str):
            data = data.encode('ascii')

        n = b = 0
        out = b''

        for c in data:
            if 33 <= c <= 117:  # b'!' <= c <= b'u'
                n += 1
                b = b * 85 + (c - 33)
                if n == 5:
                    out += struct.pack('>L', b)
                    n = b = 0
            elif c == 122:  # b'z'
                assert n == 0
                out += b'\0\0\0\0'  # Represents zero length input
            elif c == 126:  # b'~'
                if n:
                    for _ in range(5 - n):
                        b = b * 85 + 84  # Fill remaining bytes
                    out += struct.pack('>L', b)[:n - 1]
                break

        return "ASCII85", out.decode()

    except Exception as e:
        return "ASCII85", f"Error decoding ASCII85: {str(e)}"
