"""
@author axiner
@version v1.0.0
@created 2022/6/26 15:51
@abstract
@description
@history
"""
prog = 'pytcli'
description = 'A command line for python toollib package'
usage = """Usage:
  pytcli <command> [options]
Commands:
  -h/--help         帮助
  set-conda         设置conda国内源
  set-pip           设置pip国内源
  set-sshkey        设置ssh免密登录(可批量设置)
  set-yum           设置yum阿里源
  docker            docker安装等
  py2pyd            py转pyd
"""

set_conda = """usage:
  pytcli set-conda
options:
  -h/--help     帮助
"""

set_pip = """usage:
  pytcli set-pip
options:
  -h/--help     帮助
"""

set_sshkey = """usage:
  pytcli set-sshkey
options:
  -h/--help     帮助
  -u/--user     用户 
  -p/--passwd   密码
  -i/--ips      ips（多个ip可用逗号隔开,也可指定文件(一行一ip)）
"""

set_yum = """usage:
  pytcli set-yum
options:
  -h/--help     帮助
"""

docker = """usage:
  pytcli docker [options]
options:
  -h/--help     帮助
  install       安装
  start         启动
    -n/--name     镜像名称
"""

py2pyd = """usage:
  pytcli py2pyd [options]
options:
  -h/--help         帮助
  -s/--src          源（py目录或文件）
  -p/--postfix      后缀（默认为Pyd）
  -e/--exclude      排除编译（适用正则，使用管道等注意加引号）
  -i/--ignore       忽略复制（多个逗号隔开）
  -c/--clean        清理临时
"""
