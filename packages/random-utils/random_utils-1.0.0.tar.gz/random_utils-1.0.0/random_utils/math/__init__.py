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

from functools import reduce
from .vector import Vector


def is_prime(num):
    if num == 2 or num == 3: return True
    if num < 2 or num % 2 == 0: return False
    if num < 9: return True
    if num % 3 == 0: return False
    r = int(num**0.5)
    f = 5
    while f <= r:
        if num % f == 0: return False
        if num % (f+2) == 0: return False
        f += 6
    return True


def find_factors(num, sort=True):
    step = 2 if num % 2 else 1
    factors = ([i, num // i] for i in range(1, int(num ** 0.5) + 1, step) if num % i == 0)
    rv = set(reduce(list.__add__, factors))
    return sorted(rv) if sort else list(rv)
