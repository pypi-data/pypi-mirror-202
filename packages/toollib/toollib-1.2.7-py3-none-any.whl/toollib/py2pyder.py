"""
@author axiner
@version v1.0.0
@created 2023/4/7 15:14
@abstract py转pyd
@description
@history
"""
import os
import re
import shutil
import subprocess

from toollib.common import byter
from toollib.utils import listfile

try:
    from Cython.Build import cythonize
except ImportError:
    raise

__all__ = ['Py2Pyder']


class Py2Pyder:
    """
    py转pyd
    使用示例：
        py2pyder = Py2Pyder(src=r'D:\pyprj', ignore_pattern=r'__init__.py|main.py|tests/')
        py2pyder.run()
        提醒：
            请规范命名：遵守python命名规则
            请在对应的平台执行：win平台生成.pyd，linux平台生成.so
            ignore_pattern: 忽略正则
                - 文件夹在目录名后加正斜杠/即可，如：tests/，也可以指定多目录 tests/a/
                - 多个则用|隔开，如：__init__.py|tests/
            输出：
                - Pyd目录（默认原目录+Pyd）
                - build目录
        +++++[更多详见参数或源码]+++++
    """

    def __init__(
            self,
            src: str,
            postfix: str = 'Pyd',
            ignore_pattern: str = None,
    ):
        """
        初始化
        :param src: 源（py目录）
        :param postfix: 后缀（默认为Pyd）
        :param ignore_pattern: 忽略正则
        """
        self.src = src.rstrip('/\\')
        self.postfix = postfix or 'Pyd'
        self.ignore_pattern = ignore_pattern
        if not re.search(r'^[a-zA-Z_][a-zA-Z0-9_]*$', os.path.basename(self.src)):
            self.dest = os.path.join(os.path.dirname(self.src), f'pleaseStandardNaming{self.postfix}')
        else:
            self.dest = self.src + self.postfix
        self.setuppy = os.path.join(self.dest, '.setuppy')

    def run(self):
        """执行"""
        shutil.copytree(self.src, self.dest, dirs_exist_ok=True)
        self.w2setup()
        self.build()

    def w2setup(self):
        """写入setup"""
        with open(self.setuppy, 'wb') as fp:
            fp.write(byter.pyd_setup)

    def build(self):
        """编译"""
        parent_dir = os.path.dirname(self.dest)
        os.chdir(parent_dir)
        _ = len(parent_dir)
        for pyfile in listfile(self.dest, '*.py', is_str=True, is_r=True):
            if os.path.getsize(pyfile) == 0:
                print(f'跳过为空：{pyfile}')
                continue
            rpyfile = pyfile[_:].lstrip('/')
            if self.ignore_pattern and re.search(self.ignore_pattern, rpyfile):
                print(f'跳过忽略：{pyfile}')
                continue
            print(f'正在处理：{pyfile}')
            subprocess.run([
                'python', self.setuppy, 'build_ext', '-i',
                pyfile.replace('/', os.sep),
                rpyfile[:-3].replace('/', '.'),
            ])
            os.remove(pyfile)
            cpyfile = pyfile[:-3] + '.c'
            if os.path.isfile(cpyfile):
                os.remove(cpyfile)
        os.remove(self.setuppy)
