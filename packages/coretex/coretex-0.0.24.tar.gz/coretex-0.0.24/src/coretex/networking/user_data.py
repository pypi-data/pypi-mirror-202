from typing import Any, Optional, Dict
from pathlib import Path

import json
import os


def getEnvVar(key: str, default: str) -> str:
    if os.environ.get(key) is None:
        os.environ[key] = default

    return os.environ[key]


CONFIG_PATH = Path("~/.config/coretex/config.json").expanduser()
DEFAULT_CONFIG = {
    "username": None,
    "password": None,
    "token": None,
    "refreshToken": None,
    "serverUrl": getEnvVar("CTX_API_URL", "https://devext.biomechservices.com:29007/"),
    "storagePath": getEnvVar("CTX_STORAGE_PATH", "~/.coretex"),

    # Configuration related to Coretex.ai Node
    "nodeName": None,
    "organizationID": None,
    "image": None
}


# Only used by NetworkManager, should not be used anywhere else
class UserData:

    def __init__(self) -> None:
        if not CONFIG_PATH.exists():
            self.__writeConfig(DEFAULT_CONFIG)

        with open(CONFIG_PATH, "r") as configFile:
            self.__values: Dict[str, Any] = json.load(configFile)

    def __getOptionalStr(self, key: str) -> Optional[str]:
        value = self.__values[key]
        if value is None:
            return None

        if isinstance(value, str):
            return value

        raise ValueError(f">> [Coretex] {key} is not of type optional str")

    def __setValue(self, key: str, value: Any) -> None:
        if not key in self.__values:
            raise KeyError(f">> [Coretex] {key} not found")

        self.__values[key] = value

        if CONFIG_PATH.exists():
            self.__writeConfig(self.__values)

    @property
    def hasStoredCredentials(self) -> bool:
        return self.username is not None and self.password is not None

    @property
    def username(self) -> Optional[str]:
        return self.__getOptionalStr("username")

    @username.setter
    def username(self, value: Optional[str]) -> None:
        self.__setValue("username", value)

    @property
    def password(self) -> Optional[str]:
        return self.__getOptionalStr("password")

    @password.setter
    def password(self, value: Optional[str]) -> None:
        self.__setValue("password", value)

    @property
    def apiToken(self) -> Optional[str]:
        return self.__getOptionalStr("token")

    @apiToken.setter
    def apiToken(self, value: Optional[str]) -> None:
        self.__setValue("token", value)

    @property
    def refreshToken(self) -> Optional[str]:
        return self.__getOptionalStr("refreshToken")

    @refreshToken.setter
    def refreshToken(self, value: Optional[str]) -> None:
        self.__setValue("refreshToken", value)

    @classmethod
    def __writeConfig(cls, values: Dict[str, Any]) -> None:
        with open(CONFIG_PATH, "w") as configFile:
            json.dump(values, configFile, indent = 4)
