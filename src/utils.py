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
import random


def obfuscate(data: dict, sensitive_keys: list):
    """
    Return a new dict where values for keys in sensitive_keys are replaced
    with '*' of random length (1 to 10).
    """
    result = {}
    for key, value in data.items():
        if isinstance(value, dict):
            result[key] = obfuscate(value, sensitive_keys)
        else:
            if key in sensitive_keys:
                result[key] = "*" * random.randint(1, 10)
            else:
                result[key] = value
    return result
