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
from typing import Any, Dict

from rpc import rpc
from server import server


@server.resource("data://diagnostics/system-information", mime_type="application/json")
def get_system_information() -> Dict[str, Any]:
    """
    Get system information, e.g. hostname, CPU model, CPU usage,
    memory usage, load average, date and time, version, uptime, etc.

    Returns:
        A dictionary containing the system information.
    """
    return rpc.request("System", "getInformation")


@server.resource("data://storage/disks", mime_type="application/json")
def list_disks() -> Dict[str, Any]:
    """
    List all available disks in the system.

    Returns:
        A dictionary containing the list of all available disks.
    """
    return rpc.request("DiskMgmt", "getList", {"start": 0, "limit": -1})


@server.resource("data://storage/filesystems", mime_type="application/json")
def list_filesystems() -> Dict[str, Any]:
    """
    List all available filesystems in the system.

    Returns:
        A dictionary containing the list of all available filesystems.
    """
    return rpc.request("FileSystemMgmt", "getList", {"start": 0, "limit": -1})


@server.resource("data://storage/smart/devices", mime_type="application/json")
def list_smart() -> Dict[str, Any]:
    """
    List the SMART information and status of all available disks in
    the system.

    Returns:
        A dictionary containing the list of all available disks and their
        SMART status and information.
    """
    return rpc.request("Smart", "getList", {"start": 0, "limit": -1})


@server.resource(
    "data://storage/smart/devices/details/{device_file}", mime_type="application/json"
)
def get_smart_identity(device_file: str) -> Dict[str, Any]:
    """
    Get the SMART information of the specified disk.

    Args:
        device_file: The device file of the disk.

    Returns:
        A dictionary containing the SMART information.
    """
    return rpc.request("Smart", "getInformation", {"devicefile": device_file})
