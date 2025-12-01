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
import logging
import sys

import uvicorn
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from config import config
from server import server

# After the server has been initialized, import the resource and tools.
import prompts  # noqa: F401, isort: skip
import resources  # noqa: F401, isort: skip
import tools  # noqa: F401, isort: skip

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    try:
        logger.info(f"Using configuration: {config.obfuscate()}")

        host: str = config.get("server.host")
        port: int = config.get("server.port")
        transport: str = config.get("server.transport")

        if transport in ["http", "streamable-http"]:
            server_app = server.http_app(
                middleware=[
                    Middleware(
                        CORSMiddleware,
                        allow_credentials=True,
                        allow_headers=["*"],
                        allow_methods=["*"],
                        allow_origins=["*"],
                        expose_headers=["mcp-session-id"],
                    )
                ],
                transport=transport,
            )
            uvicorn.run(server_app, host=host, port=port)
        else:
            server.run(transport="stdio")

        return 0

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
