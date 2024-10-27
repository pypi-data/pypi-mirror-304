import binascii


def decode_hex(encoded_string):
    try:
        decoded = binascii.unhexlify(encoded_string).decode('utf-8')
        return "Base16 (Hex)", decoded
    except Exception as e:
        return "Base16 (Hex)", f"Error decoding Hex: {str(e)}"
