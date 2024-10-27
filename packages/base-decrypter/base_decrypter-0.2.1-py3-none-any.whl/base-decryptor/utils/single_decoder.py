from decoders import decode_base64, decode_base58, decode_hex, decode_base4096, decode_base45, decode_base32, \
    decode_base36, decode_base62, decode_base85, decode_base91, decode_base122


# Function to auto-detect and decode a single base-encoded string
def single_decoder(encoded_string):
    # List of primary decoders for auto-detection
    decoders = [decode_base64, decode_base62, decode_base58, decode_hex, decode_base32, decode_base36, decode_base45,
                decode_base85, decode_base91, decode_base122, decode_base4096]

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
