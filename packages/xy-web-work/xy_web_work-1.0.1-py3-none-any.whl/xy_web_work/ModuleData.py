# -*- coding: UTF-8 -*-
__author__ = "helios"
__doc__ = "ModuleData"
"""
  * @File    :   ModuleData.py
  * @Time    :   2023/04/25 22:27:28
  * @Author  :   helios
  * @Version :   1.0
  * @Contact :   yuyang.0515@qq.com
  * @License :   (C)Copyright 2019-2023, Ship of Ocean
  * @Desc    :   None
"""

from pathlib import Path

from importlib_resources import files

import xy_web_work


class ModuleData:
    def __init__(self) -> None:
        self.path = files(xy_web_work.__name__).joinpath("data")
        self.template_path = self.path.joinpath("template")
        self.project_path = self.template_path.joinpath("project")
        