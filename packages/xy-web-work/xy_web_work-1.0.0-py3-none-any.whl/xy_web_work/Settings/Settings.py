# -*- coding: UTF-8 -*-
__author__ = "helios"
__doc__ = "Settings"
"""
  * @File    :   Settings.py
  * @Time    :   2023/04/25 22:30:24
  * @Author  :   helios
  * @Version :   1.0
  * @Contact :   yuyang.0515@qq.com
  * @License :   (C)Copyright 2019-2023, Ship of Ocean
  * @Desc    :   None
"""

from pathlib import Path
from xy_web_settings.Settings import Settings as xySettings
from .Section.Project import Project
from .Section.Runner import Runner


class Settings(xySettings):
    project: Project | None
    runner: Runner | None

    def reload(self, settings_cfg_path: Path):
        super().reload(settings_cfg_path)
        self.project = self.__make_section(Project)
        self.runner = self.__make_section(Runner)
