from pathlib import Path

import os
import json

from .coretex import *

__version__ = 1


def syncConfigWithEnv() -> None:
    configPath = Path("~/.config/coretex/config.json").expanduser()

    if not configPath.exists():
        return

    with configPath.open("r") as configFile:
        config = json.load(configFile)

    if not "CTX_API_URL" in os.environ:
        os.environ["CTX_API_URL"] = config["serverUrl"]

    if not "CTX_STORAGE_PATH" in os.environ:
        os.environ["CTX_STORAGE_PATH"] = config["storagePath"]

    if not "CTX_NODE_NAME" in os.environ:
        os.environ["CTX_NODE_NAME"] = config["nodeName"]

    if not "CTX_ORGANIZATION_ID" in os.environ:
        os.environ["CTX_ORGANIZATION_ID"] = config["organizationID"]


syncConfigWithEnv()
