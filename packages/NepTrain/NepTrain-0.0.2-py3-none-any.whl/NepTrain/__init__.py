#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/10/24 16:22
# @Author  : 兵
# @email    : 1747193328@qq.com
import configparser
import os
import shutil
from NepTrain import utils




config_path = utils.get_config_path()

module_path = os.path.dirname(__file__)

if not os.path.exists(config_path)  :
    shutil.copy(os.path.join(module_path,"config.ini"), config_path)

Config = configparser.RawConfigParser()
Config.read(config_path,encoding="utf8")


