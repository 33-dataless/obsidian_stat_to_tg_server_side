
import json
import base64
from nacl.secret import Aead
from nacl.exceptions import CryptoError
from data.config import config

class Crypto:
    def __init__(self):
        self._key = base64.b64decode(
            config.BASE64_KEY.get_secret_value(),
            validate=True
        )
        self._cipher = Aead(self._key)

    def decrypt(self, encrypted: bytes) -> dict:
        try:
            raw = self._cipher.decrypt(encrypted)
            data = json.loads(raw)
            if not isinstance(data, dict):
                raise ValueError("payload must be a JSON object")
            return data
        except (CryptoError, ValueError, UnicodeDecodeError, json.JSONDecodeError):
            raise ValueError("failed to decrypt payload")
