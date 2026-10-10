"""
===========================================================
Cloud Secure Hospital Management & Accounting ERP System
Module  : Security
Version : 2.0
===========================================================
"""

import bcrypt
import secrets
import string


class Security:

    # -----------------------------
    # Password Hash
    # -----------------------------
    @staticmethod
    def hash_password(password: str) -> str:

        hashed = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        )

        return hashed.decode()

    # -----------------------------
    # Verify Password
    # -----------------------------
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:

        return bcrypt.checkpw(
            password.encode(),
            hashed_password.encode()
        )

    # -----------------------------
    # Generate Random Password
    # -----------------------------
    @staticmethod
    def generate_password(length=10):

        chars = (
            string.ascii_letters +
            string.digits +
            "@#$%&*"
        )

        return "".join(
            secrets.choice(chars)
            for _ in range(length)
        )

    # -----------------------------
    # Generate Secret Key
    # -----------------------------
    @staticmethod
    def generate_secret_key():

        return secrets.token_hex(32)