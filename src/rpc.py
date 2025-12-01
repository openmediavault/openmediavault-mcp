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
import json
import logging

import requests

from config import config
from utils import obfuscate

logger = logging.getLogger(__name__)


class RPC:
    def __init__(self, url: str):
        self._url = url.rstrip("/")
        self._session = requests.Session()

    def login(self, username: str, password: str) -> None:
        _ = self.request(
            "session", "login", {"username": username, "password": password}
        )

    def logout(self) -> None:
        _ = self.request("session", "logout", check_status=False)
        self._session = requests.Session()

    def request(
        self, service: str, method: str, params: dict = None, check_status: bool = True
    ) -> any:
        logger.info(
            f"RPC request: Service={service}, Method={method}, Params={obfuscate(params, ['password', 'pwd'])}"
        )

        resp = self._session.post(
            self._url,
            data=json.dumps({"service": service, "method": method, "params": params}),
            verify=False,
        )

        if check_status:
            resp.raise_for_status()

        resp = resp.json()
        if isinstance(resp, dict) and "response" in resp:
            resp = resp["response"]

        return resp


rpc = RPC(config.get("rpc.url"))
