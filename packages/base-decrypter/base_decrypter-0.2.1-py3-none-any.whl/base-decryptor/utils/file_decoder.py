from .decode_all import decode_all
from .single_decoder import single_decoder
from tabulate import tabulate


# Function to decode strings from a file with or without the --all option
def file_decoder(file, show_all):
    results_list = []  # To store results for all lines in the file

    for line in file:
        encoded_string = line.strip()
        if show_all:
            results = decode_all(encoded_string)
            results_list.append((encoded_string, results))
        else:
            encoding_type, decoded = single_decoder(encoded_string)
            results_list.append((encoded_string, [(encoding_type, decoded)]))

    # Format and print results in a table
    for encoded_string, results in results_list:
        print(f"\nEncoded String: {encoded_string}")
        print(tabulate(results, headers=["Encoding", "Decoded Output"], tablefmt="fancy_grid"))
