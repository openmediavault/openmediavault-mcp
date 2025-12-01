# -*- coding: utf-8 -*-
#
# This file is part of openmediavault.
#
# @license   https://www.gnu.org/licenses/gpl.html GPL Version 3
# @author    Volker Theile <volker.theile@openmediavault.org>
# @copyright Copyright (c) 2025 Volker Theile
#
# openmediavault is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# openmediavault is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with openmediavault. If not, see <https://www.gnu.org/licenses/>.
import os
from pathlib import Path
from typing import Any

import yaml

from utils import obfuscate


class Config:
    def __init__(self, path: str):
        self._path = Path(path)
        self._config = {
            "server": {
                "host": os.getenv("OMV_MCP_SERVER_HOST", "127.0.0.1"),
                "port": os.getenv("OMV_MCP_SERVER_PORT", "8511"),
                "transport": os.getenv("OMV_MCP_SERVER_TRANSPORT", "streamable-http"),
            },
            "rpc": {
                "url": None,
                "auth": {
                    "username": os.getenv("OMV_MCP_RPC_AUTH_USERNAME", "admin"),
                    "password": os.getenv("OMV_MCP_RPC_AUTH_PASSWORD", "openmedivault"),
                },
            },
        }
        self._load_config()

    def _load_config(self):
        if not self._path.exists():
            return

        with open(self._path, "r") as f:
            try:
                cfg = yaml.safe_load(f)
                if isinstance(cfg, dict):
                    self._config = self._config | cfg
            except yaml.YAMLError as e:
                raise yaml.YAMLError(f"Error parsing config file: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split(".")
        value = self._config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value

    def has(self, key: str) -> bool:
        return self.get(key) is not None

    def obfuscate(self) -> dict:
        return obfuscate(self._config, ["password", "pwd"])


config = Config("config.yaml")
