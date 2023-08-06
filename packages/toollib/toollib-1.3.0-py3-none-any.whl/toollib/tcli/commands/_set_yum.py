"""
@author axiner
@version v1.0.0
@created 2022/5/11 21:44
@abstract
@description
@history
"""
import subprocess

from toollib.decorator import sys_required
from toollib.tcli import here
from toollib.tcli.base import BaseCmd
from toollib.tcli.option import Options


class Cmd(BaseCmd):

    def __init__(self):
        super().__init__()

    def add_options(self):
        options = Options(
            name='set yum',
            desc='设置yum源',
            optional={self.set_yum: None}
        )
        return options

    @sys_required('centos|\.el\d', errmsg='仅支持centos|el')
    def set_yum(self):
        sh = here.joinpath('commands/plugins/set_yum.sh.x')
        cmd = ['chmod', 'u+x', sh, '&&', sh]
        subprocess.run(cmd)
