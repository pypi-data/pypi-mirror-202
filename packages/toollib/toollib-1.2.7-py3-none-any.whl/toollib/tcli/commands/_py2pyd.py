"""
@author axiner
@version v1.0.0
@created 2023/4/7 16:12
@abstract
@description
@history
"""
from toollib.decorator import sys_required
from toollib.py2pyder import Py2Pyder
from toollib.tcli.base import BaseCmd
from toollib.tcli.option import Options, Arg


class Cmd(BaseCmd):

    def __init__(self):
        super().__init__()

    def add_options(self):
        options = Options(
            name='py2pyd',
            desc='py转pyd',
            optional={self.py2pyd: [
                Arg('-s', '--src', required=True, type=str, help='源（py目录）'),
                Arg('-p', '--postfix', type=str, help='后缀（默认为Pyd）'),
                Arg('-i', '--ignore-pattern', type=str, help='忽略正则'),
            ]}
        )
        return options

    @sys_required()
    def py2pyd(self):
        src = self.parse_args.src
        postfix = self.parse_args.postfix
        ignore_pattern = self.parse_args.ignore_pattern
        py2pyder = Py2Pyder(src, postfix, ignore_pattern)
        py2pyder.run()
