import json
from collections import namedtuple

from .config import CREDENTIALS_PATH
from .exceptions import NoCredentialsError


class Credentials:
    def __init__(self, enc_user, enc_pass):
        self.enc_user = enc_user
        self.enc_pass = enc_pass

    @classmethod
    def from_unencrypted(cls, username, password):
        enc_user = cls._encrypt(username)
        enc_pass = cls._encrypt(password)

        return cls(enc_user, enc_pass)

    @classmethod
    def load_from_file(cls):
        data = CREDENTIALS_PATH.read_text()
        return Credentials(**json.loads(data))

    def decrypt(self):
        Interface = namedtuple("UnencryptedCredentials", ["username", "password"])
        return Interface(self._decrypt(self.enc_user), self._decrypt(self.enc_pass))

    @classmethod
    def _decrypt(cls, string):
        d = {}
        for c in (65, 97):
            for i in range(26):
                d[chr(i + c)] = chr((i + 13) % 26 + c)

        return "".join([d.get(c, c) for c in string])

    @classmethod
    def _encrypt(cls, string):
        d = {}
        for c in (65, 97):
            for i in range(26):
                d[chr(i + c)] = chr((i - 13) % 26 + c)

        return "".join([d.get(c, c) for c in string])

    def save(self):
        CREDENTIALS_PATH.parent.mkdir(exist_ok=True, parents=True)
        data = json.dumps({"enc_user": self.enc_user, "enc_pass": self.enc_pass})
        CREDENTIALS_PATH.write_text(data)
        return True


def get_credentials():
    if not CREDENTIALS_PATH.exists():
        raise NoCredentialsError

    creds = Credentials.load_from_file()
    return creds.decrypt()


def save_credentials(username, password):
    credentials = Credentials.from_unencrypted(username, password)
    return credentials.save()
