import binascii


def decode_uuencode(encoded_string):
    try:
        # Convert the UUEncoded string to bytes
        decoded_bytes = binascii.a2b_uu(encoded_string)
        return "UUEncode", decoded_bytes.decode()

    except Exception as e:
        return "UUEncode", f"Error: {e}"
