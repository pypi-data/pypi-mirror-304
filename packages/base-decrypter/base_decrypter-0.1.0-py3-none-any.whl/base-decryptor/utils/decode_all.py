from decoders import decode_base64, decode_urlsafe_base64, decode_base58, decode_hex, decode_base4096, decode_base45, decode_base32, \
    decode_base36, decode_base62, decode_base85, decode_base91, decode_base122, decode_uuencode


# Function to attempt decoding with all supported encodings and return all results (whether successful or not)
def decode_all(encoded_string):
    # List of decoders, including all supported encodings
    decoders = [decode_base64, decode_base62, decode_base58, decode_urlsafe_base64, decode_hex, decode_base32, decode_base36, decode_base45,
                decode_base85, decode_base91, decode_base4096, decode_base122, decode_uuencode]

    results = []
    # Try each decoder and collect all results
    for decoder in decoders:
        try:
            encoding_type, result = decoder(encoded_string)
            results.append((encoding_type, result))  # Store each decoding attempt, regardless of success
        except Exception as e:
            # Log the error for debugging purposes and include it in the results
            results.append((decoder.__name__, f"Error: {e}"))

    return results
