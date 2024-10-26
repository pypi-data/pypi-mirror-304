import click
import pyfiglet
from rich.console import Console
from rich.text import Text
from yaspin import yaspin
from yaspin.spinners import Spinners
from utils.decode_single_input import decode_single_input
from utils.file_decoder import file_decoder
from colorama import init

# Initialize colorama for Windows compatibility
init()

console = Console()


@click.command()
@click.version_option('0.1.0', message="Version: %(version)s")
@click.argument("encoded_string", required=False, default=None)  # Argument for single input string
@click.option('-f', '--file', type=click.File('r'), help="Specify a file containing encoded strings")  # File input
@click.option('-a', '--all', is_flag=True,
              help="Show decoding results for all encodings")  # Show all possible decodings
@click.option('-q', '--quiet', is_flag=True,
              help="Suppress the ASCII banner and author message")  # Suppress banner and message
def input_handler(encoded_string, file, all, quiet):
    """
    Base Decryptor: Automatically detect and decode base-encoded strings.
    Provide an ENCODED_STRING or use the --file option to decode from a file.
    """
    if not quiet:
        display_banner()

    if encoded_string:
        decode_single_input(encoded_string, all)
    elif file:
        # Use yaspin spinner for decoding from file
        with yaspin(Spinners.dots, text="Decoding strings from file...", color="cyan") as spinner:
            file_decoder(file, all)
            spinner.stop()  # Stops the spinner after decoding
    else:
        console.print("[red]Please provide either an encoded string or a file using the --file option.[/red]")
        console.print("[yellow]Use --help for more information.[/yellow]")


def display_banner():
    """Display the ASCII art banner and author message."""
    ascii_art = pyfiglet.figlet_format("The Base Decryptor")
    colored_ascii = Text(ascii_art, style="bright_magenta")
    console.print(colored_ascii)

    message = Text("Made with 💖 by Aaryan Golatkar\n", style="bold bright_green")
    console.print(message, justify='left')

if __name__ == '__main__':
    input_handler()
