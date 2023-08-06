#
#  Random utils
#  
#  Copyright Arjun Sahlot 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import ctypes
import numpy as np


def flatten(list_to_flatten) -> iter:
    for item in list_to_flatten:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


def crash():
    ctypes.pointer(ctypes.c_char.from_address(5))[0]


def diff(l1, l2):
    return np.array(l1) - np.array(l2)


def map_range(x, from_range, to_range, to_int=True):
    val = np.interp(x, from_range, to_range)
    return int(val) if to_int else val


def useless_func(*args):
    if len(args) == 1:
        return args[0]
    else:
        return args
