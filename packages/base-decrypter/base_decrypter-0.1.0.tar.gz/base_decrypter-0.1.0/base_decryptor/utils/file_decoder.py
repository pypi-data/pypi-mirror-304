from .decode_all import decode_all
from .single_decoder import single_decoder
from tabulate import tabulate
from ..decoders.base100_decoder import decode_base100
import emoji


def contains_emoji(s):
    """Check if the string contains any emoji."""
    return any(char in emoji.EMOJI_DATA for char in s)


# ANSI escape codes for colors and styles
COLOR_ENCODING = "\033[94m"  # Blue for encoding
COLOR_DECODED_OUTPUT = "\033[92m"  # Green for decoded output
COLOR_ENCODED_STRING = "\033[96m"  # Cyan for encoded string
COLOR_RESET = "\033[0m"  # Reset to default
COLOR_BOLD = "\033[1m"  # Bold text


# Function to decode strings from a file with or without the --all option
def file_decoder(file, show_all):
    results_list = []  # To store results for all lines in the file

    for line in file:
        encoded_string = line.strip()
        if contains_emoji(encoded_string):
            encoding_type, decoded = decode_base100(encoded_string)
            results_list.append((encoded_string, [(encoding_type, decoded)]))
        elif show_all:
            results = decode_all(encoded_string)
            results_list.append((encoded_string, results))
        else:
            encoding_type, decoded = single_decoder(encoded_string)
            results_list.append((encoded_string, [(encoding_type, decoded)]))

    # Format and print results in a table
    for encoded_string, results in results_list:
        # Format results for tabulation with colors
        colored_results = []
        for result in results:
            encoding_type, decoded_output = result
            # Ensure decoded_output is treated as a string
            decoded_output_str = str(decoded_output)  # Convert to string for error checking

            # Check for error in decoded_output
            if "Error" in decoded_output_str or decoded_output_str.isprintable() is False:
                colored_decoded_output = decoded_output_str  # No color if there's an error
            else:
                colored_decoded_output = f"{COLOR_DECODED_OUTPUT}{decoded_output_str}{COLOR_RESET}"

            colored_results.append([
                f"{COLOR_ENCODING}{encoding_type}{COLOR_RESET}",
                colored_decoded_output
            ])

        # Print the encoded string with color
        print(f"\nEncoded String: {COLOR_ENCODED_STRING}{encoded_string}{COLOR_RESET}")

        # Print the table with bold headers
        print(tabulate(colored_results,
                       headers=[f"{COLOR_BOLD}Encoding{COLOR_RESET}", f"{COLOR_BOLD}Decoded Output{COLOR_RESET}"],
                       tablefmt="fancy_grid"))
