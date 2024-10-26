"""
generatekey
===========
Key Generator Package
---------------------

This package provides functions to generate secret keys and user passwords.
It can be used as a command-line tool or imported as a module in other projects.
"""

from generatekey.core import generate_user_password, get_secret_key

__all__ = ["get_secret_key", "generate_user_password"]
