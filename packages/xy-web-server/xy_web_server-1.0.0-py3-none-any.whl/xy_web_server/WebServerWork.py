# -*- coding: UTF-8 -*-
__author__ = "helios"
__doc__ = "WebServerWork"
"""
  * @File    :   WebServerWork.py
  * @Time    :   2023/04/25 23:03:56
  * @Author  :   helios
  * @Version :   1.0
  * @Contact :   yuyang.0515@qq.com
  * @License :   (C)Copyright 2019-2023, Ship of Ocean
  * @Desc    :   None
"""
import logging
import shutil
from pathlib import Path
from argparse import ArgumentParser

from xy_file.File import File

import xy_web_server
from .Work import Work
from .Settings.Settings import Settings
from .ModuleData import ModuleData


class WebServerWork(Work):
    settings: Settings | None = Settings()

    prog: str = xy_web_server.__name__
    description: str = f""">>>>>>>>>>>> {xy_web_server.__name__} - v{xy_web_server.__version__} <<<<<<<<<<<<<"""
