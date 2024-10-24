# -*- coding: UTF-8 -*-
__author__ = "helios"
__doc__ = "Runner"
"""
  * @File    :   Runner.py
  * @Time    :   2023/04/25 23:57:00
  * @Author  :   helios
  * @Version :   1.0
  * @Contact :   yuyang.0515@qq.com
  * @License :   (C)Copyright 2019-2023, Ship of Ocean
  * @Desc    :   None
"""

from xy_work.Settings.Section.Runner import Runner as xyWorkRunner
from .Section import Section


class Runner(Section, xyWorkRunner):
    def get_name(self) -> str | None:
        return "xy_web_runner"
