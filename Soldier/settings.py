"""
    Soldier 配置文件
"""


import platform


# commander ip 以及端口信息
COMMANDER_IP = '127.0.0.1'
COMMANDER_PORT = 13140


# 判断当前操作系统
SYSTEM_TYPE = platform.system()


# 被禁一天后，是否关机
SHUTDOWN = False
SHUTDOWN_COMMAND = 'shutdown ' + '-s 0' if SYSTEM_TYPE == 'Windows' else '-h'
