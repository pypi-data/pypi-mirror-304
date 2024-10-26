# GenerateKey

GenerateKey is a simple Python tool designed to generate secure secret keys and user passwords. It can be used both as a command-line utility and as a library within other Python projects.

### Features

•	Secret Key Generation: Create URL-safe base64-encoded secret keys of customizable byte length, suitable for cryptographic purposes such as signing tokens or encrypting data.
•	User Password Generation: Generate random user passwords of customizable length, including uppercase and lowercase letters, digits, and punctuation symbols.

### Installation

You can install GenerateKey using pip:
```bash
pip install generatekey
```

### Usage

Command-Line Interface

GenerateKey provides a CLI for generating keys and passwords directly from the terminal.

•	Display Help
To see the available commands and options, run:
```bash
generatekey -h
```

•	Generate a Secret Key with Default Settings (64 bytes)
```bash
generatekey secretkey
```

•	Generate a Secret Key with a Specific Number of Bytes
```bash
generatekey secretkey --nbyte 32
```

•	Generate a User Password with Default Length (12 characters)
```bash
generatekey userpass
```

•	Generate a User Password with a Specific Length
```bash
generatekey userpass --length 16
```


### As a Python Module

You can also import GenerateKey into your Python projects:
```python
from generatekey import get_secret_key, generate_user_password

# Generate a secret key of 32 bytes
secret_key = get_secret_key(nbytes=32)
print(f"Secret Key: {secret_key}")

# Generate a user password of length 16
password = generate_user_password(length=16)
print(f"User Password: {password}")
```

### Requirements

•	Python 3.10 or higher


### Contributing

Contributions are welcome! Please follow these steps:

1.	Fork the repository.
2.	Create a new branch for your feature or bug fix.
3.	Commit your changes with descriptive commit messages.
4.	Push your branch to your forked repository.
5.	Create a pull request to the main repository.

### Before submitting, ensure that:

•	All tests pass.
•	Your code follows the project’s coding style.
•	You have updated the documentation if necessary.

### License

This project is licensed under the MIT License. See the [![LICENSE](https://github.com/mpita/generatekey/blob/master/LICENSE) file for details.


### Acknowledgments

•	Thanks to the contributors of open-source libraries used in this project.
•	Inspired by the need for simple and secure key and password generation tools.

### Support

If you encounter any issues or have questions, feel free to open an issue on the GitHub [![repository](https://github.com/mpita/generatekey/issues).

### Changelog

Version 0.1.0

•	Initial release
•	Command-line interface for generating secret keys and user passwords
•	Functions available for import into other Python projects
•	Unit tests covering main functionalities

Feel free to modify this README to better suit your project’s specifics, such as updating URLs, adding badges, or including additional sections like a table of contents or FAQs.