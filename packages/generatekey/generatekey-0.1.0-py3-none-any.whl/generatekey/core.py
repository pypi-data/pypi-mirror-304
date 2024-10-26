"""
generatekey.core
=======================
This module provides functions to generate secret keys and user passwords.
It can also be executed as a command-line tool.
"""

import argparse
import base64
import secrets
import string
import sys


def get_secret_key(nbytes: int = 64) -> str:
    """
    Generate a URL-safe base64-encoded secret key.

    Parameters
    ----------
    nbytes : int, optional
        Number of bytes for the secret key. Must be a positive integer. Default is 64.

    Returns
    -------
    str
        A URL-safe base64-encoded secret key string.

    Raises
    ------
    ValueError
        If nbytes is not a positive integer.
    """

    if nbytes <= 0:
        raise ValueError("nbytes must be a positive integer")

    key = secrets.token_bytes(nbytes)
    key_base64 = base64.urlsafe_b64encode(key).decode("utf-8")
    return key_base64


def generate_user_password(length: int = 12) -> str:
    """
    Generate a random password for user accounts.

    Parameters
    ----------
    length : int, optional
        Length of the password to generate. Must be a positive integer. Default is 12.

    Returns
    -------
    str
        A randomly generated password including letters, digits, and punctuation.

    Raises
    ------
    ValueError
        If `length` is not a positive integer.
    """

    if length <= 0:
        raise ValueError("length must be a positive integer")

    characters = f"{string.ascii_letters}{string.digits}{string.punctuation}"
    password = "".join(secrets.choice(characters) for _ in range(length))
    return password


def main():
    """
    Entry point for the command-line interface.

    Parses command-line arguments and executes the appropriate function based on the provided subcommand.

    Usage
    -----
    generatekey secretkey [--nbyte NBYTE]
    generatekey userpass [--length LENGTH]
    """
    parser = argparse.ArgumentParser(
        description="Generate secret keys and user passwords."
    )
    subparsers = parser.add_subparsers(title="Commands", dest="command", required=True)

    parser_secretkey = subparsers.add_parser("secretkey", help="Generate a secret key.")
    parser_secretkey.add_argument(
        "--nbyte",
        type=int,
        default=64,
        help="Number of bytes for the secret key (default: 64).",
    )

    parser_userpass = subparsers.add_parser(
        "userpass", help="Generate a user password."
    )
    parser_userpass.add_argument(
        "--length",
        type=int,
        default=12,
        help="Length of the user password (default: 12).",
    )

    args = parser.parse_args()

    if args.command == "secretkey":
        out_str = get_secret_key(nbytes=args.nbyte)
    elif args.command == "userpass":
        out_str = generate_user_password(length=args.length)
    else:
        parser.print_help()
        sys.exit(1)

    print(out_str)


if __name__ == "__main__":
    main()
