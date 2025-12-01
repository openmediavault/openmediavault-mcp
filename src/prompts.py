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
from server import server


@server.prompt
def list_disks() -> str:
    return """
Show me a list of all available disks on my NAS.
"""


@server.prompt
def list_filesystems() -> str:
    return """
Show me a list of all available filesystems on my NAS.
"""


@server.prompt
def list_smart_info() -> str:
    return """
Show me the SMART information of all available disks on my NAS.
"""


@server.prompt
def get_smart_info_by_device(device_file: str) -> str:
    return f"""
Show me the SMART information from the disk with the device file '{device_file}'.
"""


@server.prompt
def reboot() -> str:
    return """
Reboot my network attached storage (NAS) system.
"""


@server.prompt
def shutdown() -> str:
    return """
Shut down my openmediavault network attached storage (NAS) system.
"""


@server.prompt
def standby() -> str:
    return """
Put my network attached storage (NAS) system into standby mode.
"""
