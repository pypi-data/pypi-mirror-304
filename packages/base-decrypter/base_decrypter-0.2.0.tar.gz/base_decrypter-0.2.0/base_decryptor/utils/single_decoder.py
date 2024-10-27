from ..decoders.base2_decoder import decode_base2
from ..decoders.base8_decoder import decode_base8
from ..decoders.base10_decoder import decode_base10
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
    decoders = [
        decode_base64,  # Standard and widely used
        decode_urlsafe_base64,  # Variant of Base64 for URLs
        decode_base32,  # Commonly used in certain applications
        decode_base2,  # Binary (Base2)
        decode_base8,  # Octal (Base8)
        decode_base10,  # Decimal (Base10)
        decode_hex,  # Common in computing for binary data
        decode_base36,  # Alphanumeric (Base36)
        decode_base58,  # Bitcoin and other applications
        decode_base62,  # Alphanumeric with case sensitivity
        decode_base85,  # ASCII-based encoding (Base85)
        decode_ascii85,  # ASCII-based variant for Base85
        decode_base91,  # Higher density than Base85
        decode_base92,  # Further optimized encoding
        decode_base45,  # Compact encoding standard for certain fields
        decode_base4096,  # Very high-density encoding
        decode_base122,  # Extended character set encoding
        decode_uuencode,  # Unix encoding method
        decode_base100  # Experimental/extended encoding
    ]

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
