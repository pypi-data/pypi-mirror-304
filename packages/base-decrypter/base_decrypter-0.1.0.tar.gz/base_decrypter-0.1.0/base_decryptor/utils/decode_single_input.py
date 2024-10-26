from .decode_all import decode_all
from .single_decoder import single_decoder
from rich.console import Console
from rich.text import Text
from tabulate import tabulate

console = Console()


# Function to decode a single string input with or without the --all option
def decode_single_input(encoded_string, show_all):
    if show_all:
        # Show all possible decodings if --all is specified
        results = decode_all(encoded_string)

        # Check each decoded output; only highlight in green if there's no error
        colorized_results = []
        for encoding, decoded_output in results:
            decoded_output_str = str(decoded_output)
            if "Error" in decoded_output_str or "Unable to decode" in decoded_output_str:
                colorized_results.append((f"[blue]{encoding}[/blue]", decoded_output))  # No color if there's an error
            else:
                colorized_results.append((f"[blue]{encoding}[/blue]", f"[green]{decoded_output}[/green]"))

        # Display the table with colorized results
        console.print(tabulate(colorized_results, headers=["Encoding", "Decoded Output"], tablefmt="fancy_grid"))
    else:
        # Default to single decoding detection if --all is not specified
        encoding_type, decoded = single_decoder(encoded_string)

        # Colorized output
        encoded_text = Text(f"Encoded String: {encoded_string}", style="cyan")
        encoding_text = Text(f"Detected Encoding: {encoding_type}", style="blue")

        # Check if the decoded string indicates failure
        if "Unable to decode" in decoded:
            decode_colour = 'red'  # No highlight if there's an error
        else:
            decode_colour = 'green'
        decoded_text = Text(f"Decoded String: {decoded}\n", style=decode_colour)

        console.print(encoded_text)
        console.print(encoding_text)
        console.print(decoded_text)

        # Only show the options message if the encoding was not detected successfully
        if encoding_type == "Unknown":
            options_message = Text("Please try with the ", style="")
            options_message.append("-a", style="bold magenta")  # Highlight -a
            options_message.append("/", style="")
            options_message.append("--all", style="bold magenta")  # Highlight --all
            options_message.append(" option to bruteforce the base decoding.\n", style="")

            console.print(options_message)
