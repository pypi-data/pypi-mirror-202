"""
@author axiner
@version v1.0.0
@created 2022/4/30 13:20
@abstract
@description
@history
"""
import os

from toollib import utils
from toollib.decorator import sys_required
from toollib.tcli.base import BaseCmd
from toollib.common import byter
from toollib.tcli.option import Options


class Cmd(BaseCmd):

    def __init__(self):
        super().__init__()

    def add_options(self):
        options = Options(
            name='set conda',
            desc='设置conda源',
            optional={self.set_conda: None}
        )
        return options

    @sys_required()
    def set_conda(self):
        print('设置镜像源.....')
        _home = utils.home()
        conf_file = os.path.join(_home, '.condarc')
        with open(conf_file, mode='wb') as f:
            f.write(byter.conda_conf)
            print(f'to Path>>> {conf_file}')
            print(byter.conda_conf.decode())
            print('设置完成')
