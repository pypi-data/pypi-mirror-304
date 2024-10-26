# Base Decryptor

**A CLI tool to decode base-encoded strings.**

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)


## Features
- Decode various base-encoded strings
- Some of them are:
  - Base64
  - Base64 URL Safe
  - Base 16 (Hex)
  - Base32
  - Base36
  - Base45
  - Base58
  - Base62
  - Base85
  - Base91
  - Base92
  - Base100 (Emoji)
  - Base122
  - Base4096
  - UUEncode

- CLI interface for ease of use.
- Handles emoji in strings and decodes accordingly.
- Displays decoded results in a user-friendly table format with color-coded output.
- Error handling for decoding processes.

## Installation

You can install the `base-decryptor` package via pip. Run the following command:

```bash
pip install base-decryptor
```

## Usage

You can provide either a single encoded string or a file containing multiple encoded strings.

### Command Line Options

```bash
base-decryptor [OPTIONS] [ENCODED_STRING]
Arguments
ENCODED_STRING: (Optional) A single base-encoded string that you want to decode.
Options
-f, --file <file>: Specify a file containing encoded strings. Each line in the file will be processed for decoding.

-a, --all: If this flag is set, the tool will attempt to decode the input using all supported encoding methods (Base36, Base45, Base58, Base91, Base92, Base100).

-q, --quiet: Suppress the ASCII banner and author message when running the tool.
```
Examples
Decode a single encoded string:

```bash
base-decryptor "encoded_string_here"
```
Decode strings from a file:
```bash
base-decryptor --file encoded_strings.txt
```
Decode all encodings for a single string:
```bash
base-decryptor --all "encoded_string_here"
```

Decode all encodings from a file:
```bash
base-decryptor --file encoded_strings.txt --all
```
Run in quiet mode:
```bash
base-decryptor -q --file encoded_strings.txt
```

Help option
```bash
base-decryptor --help
```


## Dependencies
The following packages are required:

```
base36==0.1.1
base4096==1.0
base45==0.4.4
base58==2.1.1
base91==1.0.1
base92==1.0.3
pybase100==0.3.1
click==8.1.7
colorama==0.4.6
emoji==2.14.0
pybase62==1.0.0
pycryptodome==3.20.0
pyfiglet==1.0.2
requests==2.32.3
rich==13.9.3
tabulate==0.9.0
yaspin==3.1.0
```


## Contributing
Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.


## License
This project is licensed under the MIT License. See the LICENSE file for details.


## Contact
- Name: Aaryan Golatkar
- Email: aaryangolatkar@gmail.com
- GitHub: https://github.com/aaryan-11-x
- Linkedin: https://www.linkedin.com/in/aaryan-golatkar/