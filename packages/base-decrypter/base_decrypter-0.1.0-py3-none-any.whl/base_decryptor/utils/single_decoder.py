from ..decoders.base32_decoder import decode_base32
from ..decoders.base36_decoder import decode_base36
from ..decoders.base45_decoder import decode_base45
from ..decoders.base58_decoder import decode_base58
from ..decoders.base62_decoder import decode_base62
from ..decoders.base64_decoder import decode_base64
from ..decoders.base64_urlsafe_decoder import decode_urlsafe_base64
from ..decoders.base85_decoder import decode_base85
from ..decoders.ascii85_decoder import decode_ascii85
from ..decoders.base91_decoder import decode_base91
from ..decoders.base92_decoder import decode_base92
from ..decoders.base122_decoder import decode_base122
from ..decoders.base4096_decoder import decode_base4096
from ..decoders.hex_decoder import decode_hex
from ..decoders.uuencode_decoder import decode_uuencode
from ..decoders.base100_decoder import decode_base100


# Function to auto-detect and decode a single base-encoded string
def single_decoder(encoded_string):
    # List of primary decoders for auto-detection
    decoders = [decode_base64, decode_urlsafe_base64, decode_base62, decode_base58, decode_hex, decode_base32, decode_base36, decode_base45,
                decode_base85, decode_ascii85, decode_base91, decode_base92, decode_base122, decode_base4096, decode_uuencode, decode_base100]

    # Try each decoder until one works, while handling any potential errors
    for decoder in decoders:
        try:
            encoding_type, result = decoder(encoded_string)
            if "Error" not in result:
                return encoding_type, result
        except Exception as e:
            # Log the error for debugging purposes and continue to the next decoder
            print(f"Error with {decoder.__name__}: {e}")

    return "Unknown", "Unable to decode string."
