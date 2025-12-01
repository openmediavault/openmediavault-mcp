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
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastmcp import FastMCP
from mcp.types import Icon

from config import config
from rpc import rpc


@asynccontextmanager
async def lifespan(_: FastMCP) -> AsyncIterator[Any]:
    try:
        rpc.login(config.get("rpc.auth.username"), config.get("rpc.auth.password"))
        yield {}
    finally:
        rpc.logout()


server = FastMCP(
    version="1.0.0",
    name="openmediavault MCP server",
    instructions="This server provides tools and resources to interact with an openmediavault network attached storage (NAS) system.",
    website_url="https://www.openmediavault.org",
    icons=[
        Icon(
            src="https://www.openmediavault.org/favicon.svg",
            mimeType="image/svg+xml",
        ),
    ],
    lifespan=lifespan,
)
