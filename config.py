# -*- coding: utf-8 -*-
from datetime import datetime

param_dict = {}

with open('config.cfg') as config:
    for line in config:
        line = line.strip()
        line_list = line.split(' = ')
        param_dict[line_list[0]] = line_list[1]

token = str(param_dict.get('token'))
host = str(param_dict.get('host'))
amount_gpu = int(param_dict.get('amount_gpu'))
temperature_hi = int(param_dict.get('temperature_hi'))
speed_lo = int(param_dict.get('speed_lo'))
time_interval = int(param_dict.get('time_interval'))
repeat_val = int(param_dict.get('repeat_val'))

param_measures = {'gpu_power_usage': 'W', 'temperature': str(chr(0x00b0)), 'speed_sps': 'Sol/s'}


def current_time():
    c_time = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
    return c_time
