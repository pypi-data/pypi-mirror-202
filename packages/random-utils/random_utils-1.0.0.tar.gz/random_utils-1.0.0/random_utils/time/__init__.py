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

import time
from functools import wraps


def time_this(num_iter=1):
    num_iter = max(1, num_iter)
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            s = time.time()
            for _ in range(num_iter-1):
                func(*args, **kwargs)
            result = func(*args, **kwargs)
            print(f"Function: {func.__name__}, Time: {time.time() - s}, Iterations: {num_iter}")
            return result
        return wrapper
    return decorator
