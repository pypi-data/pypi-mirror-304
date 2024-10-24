# -*- coding: UTF-8 -*-
__author__ = "helios"
__doc__ = "Work"
"""
  * @File    :   Work.py
  * @Time    :   2023/04/24 14:11:41
  * @Author  :   helios
  * @Version :   1.0
  * @Contact :   yuyang.0515@qq.com
  * @License :   (C)Copyright 2019-2023, Ship of Ocean
  * @Desc    :   None
"""

from xy_work.Work import Work as xyWork
from .Settings.Settings import Settings


class Work(xyWork):
    settings: Settings | None = Settings()
