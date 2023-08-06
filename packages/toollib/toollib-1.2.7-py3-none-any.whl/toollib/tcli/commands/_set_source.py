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
            desc='设置配置',
            optional={self.set_source: None}
        )
        return options

    @sys_required('centos|\.el\d', errmsg='仅支持centos|el')
    def set_source(self):
        sh = here.joinpath('commands/plugins/set_source.sh.x')
        cmd = ['chmod', 'u+x', sh, '&&', sh]
        subprocess.run(cmd)
