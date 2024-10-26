import base64


def decode_urlsafe_base64(encoded_string):
    try:
        # Add padding if necessary
        padding_needed = len(encoded_string) % 4
        if padding_needed:
            encoded_string += '=' * (4 - padding_needed)

        # Decode the URL-safe base64 string
        decoded_bytes = base64.urlsafe_b64decode(encoded_string)
        return "Base64 (URL Safe)", decoded_bytes.decode('utf-8')

    except Exception as e:
        return "Base64 (URL Safe)", f"Error: {e}"
