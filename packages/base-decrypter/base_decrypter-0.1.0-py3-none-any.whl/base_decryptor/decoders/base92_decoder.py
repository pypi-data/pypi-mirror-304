# THE BEERWARE LICENSE (Revision 42):
# <thenoviceoof> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a beer in return
# - Nathan Hwang (thenoviceoof)
#
# Modified from: https://github.com/thenoviceoof/base92/blob/master/python/base92/base92.py


def base92_ord(val):
    """
    Converts a Base92 character to its integer value.

    Parameters
    ----------
    val : str
        A single character from the Base92 encoded string.

    Returns
    -------
    int
        The integer value of the Base92 character.
    """
    num = ord(val)
    if val == '!':
        return 0
    elif ord('#') <= num <= ord('_'):
        return num - ord('#') + 1
    elif ord('a') <= num <= ord('}'):
        return num - ord('a') + 62
    else:
        raise ValueError('val is not a base92 character')


def decode_base92(encoded_string):
    """
    Decodes a Base92 encoded string.

    Parameters
    ----------
    encoded_string : str
        The Base92 encoded string to decode.

    Returns
    -------
    tuple
        A tuple with the type of encoding as the first element and the decoded
        string as the second element. If there is an error decoding the string,
        the error message is returned as the second element of the tuple.
    """
    try:
        bitstr = ''
        resstr = ''
        if encoded_string == '~':
            return "Base92", ''

        # Decoding each pair of characters
        for i in range(len(encoded_string) // 2):
            x = base92_ord(encoded_string[2 * i]) * 91 + base92_ord(encoded_string[2 * i + 1])
            bitstr += '{:013b}'.format(x)

            while len(bitstr) >= 8:
                resstr += chr(int(bitstr[:8], 2))
                bitstr = bitstr[8:]

        # Handling last character if string length is odd
        if len(encoded_string) % 2 == 1:
            x = base92_ord(encoded_string[-1])
            bitstr += '{:06b}'.format(x)

            while len(bitstr) >= 8:
                resstr += chr(int(bitstr[:8], 2))
                bitstr = bitstr[8:]

        return "Base92", resstr

    except Exception as e:
        return "Base92", f"Error decoding Base92: {str(e)}"
