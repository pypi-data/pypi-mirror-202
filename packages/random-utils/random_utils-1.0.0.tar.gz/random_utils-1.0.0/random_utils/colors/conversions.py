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

import colorsys
import numpy as np


def rgb_to_hsv(rgb):
    color = np.array(rgb)
    return np.array(colorsys.rgb_to_hsv(*(color/255))) * 255


def rgb_to_hls(rgb):
    color = np.array(rgb)
    return np.array(colorsys.rgb_to_hls(*(color/255))) * 255


def rgb_to_yiq(rgb):
    color = np.array(rgb)
    return np.array(colorsys.rgb_to_yiq(*(color/255))) * 255


def hsv_to_rgb(hsv):
    color = np.array(hsv)
    return np.array(colorsys.hsv_to_rgb(*(color/255))) * 255


def hls_to_rgb(hls):
    color = np.array(hls)
    return np.array(colorsys.hls_to_rgb(*(color/255))) * 255


def yiq_to_rgb(yiq):
    color = np.array(yiq)
    return np.array(colorsys.yiq_to_rgb(*(color/255))) * 255


def hsv_to_hls(hsv):
    return rgb_to_hls(hsv_to_rgb(hsv))


def hsv_to_yiq(hsv):
    return rgb_to_yiq(hsv_to_rgb(hsv))


def hls_to_hsv(hls):
    return rgb_to_hsv(hls_to_rgb(hls))


def yiq_to_hsv(yiq):
    return rgb_to_hsv(yiq_to_rgb(yiq))


def yiq_to_hls(yiq):
    return rgb_to_hls(yiq_to_rgb(yiq))


def hls_to_yiq(hls):
    return rgb_to_yiq(hls_to_rgb(hls))
