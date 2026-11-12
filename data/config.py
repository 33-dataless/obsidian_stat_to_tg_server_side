
from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import base64

from nacl.secret import Aead

class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    BASE64_KEY: SecretStr = Field(validation_alias="BASE64_KEY")
    TELEGRAM_BOT_TOKEN: SecretStr = Field(validation_alias="TELEGRAM_BOT_TOKEN")
    TELEGRAM_ADMIN_ID: SecretStr = Field(validation_alias="TELEGRAM_ADMIN_ID")

    @field_validator("BASE64_KEY")
    @classmethod
    def validate_key(cls, value: SecretStr) -> SecretStr:
        try:
            decoded = base64.b64decode(
                value.get_secret_value(),
                validate=True
            )
        except Exception:
            raise ValueError("BASE64_KEY must be valid Base64")

        if len(decoded) != Aead.KEY_SIZE:
            raise ValueError(
                f"BASE64_KEY must decode to {Aead.KEY_SIZE} bytes"
            )

        return value


config = Config()
