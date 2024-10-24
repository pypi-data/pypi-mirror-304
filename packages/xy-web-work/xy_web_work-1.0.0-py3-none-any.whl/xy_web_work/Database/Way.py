# -*- coding: UTF-8 -*-
__author__ = "helios"
__doc__ = "Way"
"""
  * @File    :   Way.py
  * @Time    :   2023/04/26 03:02:04
  * @Author  :   helios
  * @Version :   1.0
  * @Contact :   yuyang.0515@qq.com
  * @License :   (C)Copyright 2019-2023, Ship of Ocean
  * @Desc    :   None
"""

from enum import IntEnum


class Way(IntEnum):
    MYSQL = 0
    SQLITE = 1
    REDIS = 2
    POSTGRESQL = 3
    MONGO = 4
