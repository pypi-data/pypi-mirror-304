import sys

PY2 = sys.version_info[0] == 2
kShortened = 0b111  # last two-byte char encodes <= 7 bits
kIllegals = [chr(0), chr(10), chr(13), chr(34), chr(38), chr(92)]
kIllegalsSet = {chr(0), chr(10), chr(13), chr(34), chr(38), chr(92)}


def decode_base122(encoded_string, warnings=True):
    try:
        if PY2 and warnings:
            raise NotImplementedError(
                "This hasn't been tested on Python2 yet! Turn this warning off by passing warnings=False."
            )

        # Convert input string with escape sequences to bytes
        if isinstance(encoded_string, str):
            # Decode escape sequences like \x19 to actual bytes
            byte_data = bytearray(encoded_string.encode("latin1").decode("unicode_escape").encode("latin1"))
        elif isinstance(encoded_string, (bytes, bytearray)):
            byte_data = encoded_string
        else:
            raise TypeError("Input must be a string or bytes.")

        decoded = []
        curByte = bitOfByte = 0

        def push7(byte):
            nonlocal curByte, bitOfByte, decoded
            byte <<= 1
            curByte |= (byte % 0x100000000) >> bitOfByte
            bitOfByte += 7
            if bitOfByte >= 8:
                decoded.append(curByte)
                bitOfByte -= 8
                curByte = (byte << (7 - bitOfByte)) & 255

        for i in range(len(byte_data)):
            if byte_data[i] > 127:
                illegalIndex = ((byte_data[i] % 0x100000000) >> 8) & 7
                if illegalIndex != kShortened:
                    push7(ord(kIllegals[illegalIndex]))
                push7(byte_data[i] & 127)
            else:
                push7(byte_data[i])

        # Decode the result to UTF-8
        return "Base122", bytearray(decoded).decode()

    except Exception as e:
        return "Base122", f"Error: {e}"
