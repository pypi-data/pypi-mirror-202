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

class Stack:
    def __init__(self, *args):
        self.arr = list(args)

    def size(self):
        return len(self)

    def empty(self):
        return len(self) == 0

    def push(self, element):
        self.arr.append(element)

    def put(self, element):
        self.push(element)

    def append(self, element):
        self.push(element)

    def pop(self):
        return self.arr.pop(-1)

    def get(self):
        return self.pop()

    def get_list(self):
        return self.arr

    def get_array(self):
        return self.arr

    def add(self, lst):
        self.arr.extend(lst)

    def extend(self, lst):
        self.add(lst)

    def sub(self, val):
        for i in range(len(self.arr)):
            self.arr[i] -= val

    def mult(self, val, individually=True):
        if individually:
            for i in range(len(self.arr)):
                self.arr[i] *= val
        else:
            self.arr *= val

    def div(self, val):
        for i in range(len(self.arr)):
            self.arr[i] /= val

    def __getitem__(self, slice):
        return self.arr[slice]

    def __iter__(self):
        return iter(self.arr)

    def __add__(self, lst):
        tmp = self.arr.copy()
        tmp.extend(lst)
        return Stack(tmp)

    def __sub__(self, val):
        tmp = self.arr.copy()
        for i in range(len(tmp)):
            tmp[i] -= val
        return Stack(tmp)

    def __mul__(self, val, individually=True):
        tmp = self.arr.copy()
        if individually:
            for i in range(len(tmp)):
                tmp[i] *= val
        else:
            tmp *= val
        return Stack(tmp)

    def __div__(self, val):
        tmp = self.arr.copy()
        for i in range(len(tmp)):
            tmp[i] /= val
        return Stack(tmp)

    def __len__(self):
        return len(self.arr)

    def __repr__(self):
        return "[" + ", ".join(list(map(str, self.arr))) + "]"
