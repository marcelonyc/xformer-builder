from secrets import token_urlsafe
import hashlib
import os
from dataclasses import dataclass


@dataclass
class _UserData:
    token: str
    id: str
    salt: bytes
    hashed_token: bytes

    def __call__(self, token, id, salt, hashed_token):
        self.token = token
        self.id = id
        self.salt = salt
        self.hash_token = hashed_token


class TokenManager:
    def __init__(self, token: str = None, salt: str = None):
        self.token = None
        self.salt = None
        self.id = None
        self.id_position = 8

    def generate_salt(self):
        # 128 bit salt value
        salt = os.urandom(16)
        return salt

    def _generate_token(self):
        self.token: str = token_urlsafe(36)

    def generate_user_data(self) -> _UserData:
        """
        Generates user data including token, id, salt, token and hashed_token.
        Validat that id is unique in the DB.
        Returns:
            tuple: A tuple containing the generated token, self.id, salt,token adn hashed_token.
        """
        self._generate_token()
        self.hash_token(self.token)
        self.id = self.token[: self.id_position]

        return _UserData(self.token, self.id, self.salt, self.hashed_token)

    def hash_token(self, token: str):
        def hash_token(self, token: str) -> bytes:
            """
            Hashes the given token using SHA256 algorithm.
            Parameters:
                token (str): The token to be hashed.
            Returns:
                bytes: The hashed token as bytes.
            """

        self.salt = self.generate_salt()
        self.hashed_token = hashlib.sha256(self.salt + token.encode()).digest()

        return self.hashed_token

    def verify_token(self, salt, hashed_token, token):
        new_hash = hashlib.sha256(salt + token.encode())
        return new_hash.digest() == hashed_token
