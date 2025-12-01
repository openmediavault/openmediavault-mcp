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
from typing import Any, Dict, List, Optional

from rpc import rpc
from server import server


@server.tool(annotations={"openWorldHint": True})
def reboot() -> Dict[str, Any]:
    """
    A tool that reboots the system.
    """
    rpc.request("System", "reboot")
    return {
        "success": True,
        "message": "The system will be rebooted.",
    }


@server.tool(annotations={"openWorldHint": True})
def shutdown() -> Dict[str, Any]:
    """
    A tool that shuts down the system.
    """
    rpc.request("System", "shutdown")
    return {
        "success": True,
        "message": "The system will be shut down.",
    }


@server.tool(annotations={"openWorldHint": True})
def standby() -> Dict[str, Any]:
    """
    A tool that puts the system into standby mode.
    """
    rpc.request("System", "standby")
    return {
        "success": True,
        "message": "The system will go into standby mode.",
    }


@server.tool(annotations={"openWorldHint": True}, tags=["system", "diagnostics"])
def get_system_information() -> Dict[str, Any]:
    """
    Get system information, e.g. hostname, CPU model, CPU usage,
    memory usage, load average, date and time, version, uptime, etc.

    Returns:
         A dictionary containing the system information.
    """
    return rpc.request("System", "getInformation")


@server.tool(
    annotations={"openWorldHint": True},
    tags=["system", "storage", "disk", "HDD", "SSD", "NVMe"],
)
def list_disks() -> Dict[str, Any]:
    """
    List all available disks in the system.

    Returns:
        A dictionary containing the list of all available disks.
    """
    return rpc.request("DiskMgmt", "getList", {"start": 0, "limit": -1})


@server.tool(
    annotations={"openWorldHint": True}, tags=["system", "storage", "filesystem"]
)
def list_filesystems() -> Dict[str, Any]:
    """
    List all available filesystems in the system.

    Returns:
        A dictionary containing the list of all available filesystems.
    """
    return rpc.request("FileSystemMgmt", "getList", {"start": 0, "limit": -1})


@server.tool(
    annotations={"openWorldHint": True}, tags=["system", "storage", "disk", "SMART"]
)
def list_smart() -> Dict[str, Any]:
    """
    List the SMART information and status of all available disks in
    the system.

    Returns:
        A dictionary containing the list of all available disks and their
        SMART status and information.
    """
    return rpc.request("Smart", "getList", {"start": 0, "limit": -1})


@server.tool(
    annotations={"openWorldHint": True}, tags=["system", "storage", "disk", "SMART"]
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


@server.tool(
    annotations={"openWorldHint": True}, tags=["system", "user management", "user"]
)
def list_users() -> Dict[str, Any]:
    """
    List ist of user accounts of the system, including their names, UIDs,
    GIDs, comments, directories, shells, groups, and other details.

    Returns:
        A dictionary containing the list of all user accounts.
    """
    return rpc.request("UserMgmt", "getUserList", {"start": 0, "limit": -1})


@server.tool(
    annotations={"openWorldHint": True}, tags=["system", "user management", "user"]
)
def get_user(name: str) -> Dict[str, Any]:
    """
    Get detailed information about a user account of the system based on
    their name.

    Returns:
        A dictionary containing the detailed user account information.
    """
    return rpc.request("UserMgmt", "getUser", {"name": name})


@server.tool(
    annotations={"openWorldHint": True, "destructiveHint": True},
    tags=["system", "user management", "user"],
)
def delete_user(name: str) -> Dict[str, Any]:
    """
    Delete a user account of the system based on their name.

    Returns:
        A dictionary containing the detailed account information of
        the deleted user to confirm the deletion.
    """
    return {
        "success": True,
        "message": f"User {name} deleted successfully.",
        "data": rpc.request("UserMgmt", "deleteUser", {"name": name}),
    }


@server.tool(
    annotations={"openWorldHint": True}, tags=["system", "user management", "group"]
)
def list_groups() -> Dict[str, Any]:
    """
    List all group accounts of the system.

    Returns:
        A dictionary containing the list of all group accounts of the system.
    """
    return rpc.request("UserMgmt", "getGroupList", {"start": 0, "limit": -1})


@server.tool(
    annotations={"openWorldHint": True}, tags=["system", "user management", "group"]
)
def get_group(name: str) -> Dict[str, Any]:
    """
    Get detailed information about a group account of the system based on
    their name.

    Returns:
        A dictionary containing the detailed group account information.
    """
    return rpc.request("UserMgmt", "getGroup", {"name": name})


@server.tool(
    annotations={"openWorldHint": True}, tags=["system", "user management", "group"]
)
def create_group(
    name: str,
    gid: Optional[int] = None,
    members: Optional[List[str]] = None,
    comment: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a new group account. The name is required, other parameters like
    the group ID (GID), a list of members or a comment are optional.

    Args:
        name: The name of the group.
        gid: The group ID.
        members: The list of members to be added to the group.
        comment: The comment for the group.

    Returns:
        A dictionary containing the detailed account information of
        the created group.
    """
    params: Dict[str, Any] = {
        "name": name,
        "members": [],
        "comment": "",
    }

    if isinstance(gid, int):
        params["gid"] = gid
    if isinstance(members, list) and len(members) > 0:
        params["members"] = members
    if isinstance(comment, str) and len(comment) > 0:
        params["comment"] = comment

    return {
        "success": True,
        "message": f"Group {name} created successfully.",
        "data": rpc.request("UserMgmt", "setGroup", params),
    }


@server.tool(
    annotations={"openWorldHint": True, "destructiveHint": True},
    tags=["system", "user management", "group"],
)
def update_group(
    name: str,
    members: Optional[List[str]] = None,
    comment: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Update an existing group account. The name is required, other parameters like the
    list of members or comment are optional.

    Args:
        name: The name of the group.
        members: The list of members of the group.
        comment: The comment for the group.

    Returns:
        A dictionary containing the detailed account information of
        the updated group.
    """

    try:
        group: Dict[str, Any] = rpc.request("UserMgmt", "getGroup", {"name": name})
    except Exception:
        return {
            "success": False,
            "message": f"Group {name} does not exist.",
        }

    if isinstance(members, list) and len(members) > 0:
        group["members"] = members
    if isinstance(comment, str) and len(comment) > 0:
        group["comment"] = comment

    return {
        "success": True,
        "message": f"Group {name} updated successfully.",
        "data": rpc.request("UserMgmt", "setGroup", group),
    }


@server.tool(
    annotations={"openWorldHint": True, "destructiveHint": True},
    tags=["system", "user management", "group"],
)
def delete_group(name: str) -> Dict[str, Any]:
    """
    Delete a group account of the system based on their name.

    Returns:
        A dictionary containing the detailed account information of
        the deleted group to confirm the deletion.
    """
    return {
        "success": True,
        "message": f"Group {name} deleted successfully.",
        "data": rpc.request("UserMgmt", "deleteGroup", {"name": name}),
    }


@server.tool(
    annotations={"openWorldHint": True}, tags=["system", "storage", "shared folder"]
)
def list_shared_folders() -> Dict[str, Any]:
    """
    List all configured shared folders.

    Returns:
        A dictionary containing the list of all shared folders.
    """
    return rpc.request("ShareMgmt", "getList", {"start": 0, "limit": -1})


# @server.tool(annotations={"openWorldHint": True}, tags=["system", "storage", "shared folder"])
# def create_shared_folders(name: str) -> Dict[str, Any]:
#     """
#     Create a shared folders.
#
#     Args:
#         name: The name of the shared folder.
#
#     Returns:
#         The shared folder database configuration object.
#     """
#     return rpc.request('ShareMgmt', 'set', {
#         'uuid': 'fa4b1c66-ef79-11e5-87a0-0002b3a176b4',
#         'name': name,
#     })
