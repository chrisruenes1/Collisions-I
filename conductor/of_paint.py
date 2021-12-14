import os
from constants.ip_addr_constants import YELLOW_ROBOT_IP
from constants.service_ports import PAINT_GUN_PORT
from utils.get_ip_for_color import get_ip_for_color

def fire(color):
    curl_command = f'curl localhost:{PAINT_GUN_PORT}/fire'
    command = f'ssh \'pi@{get_ip_for_color(color)}\' \"{curl_command}\"'
    print(f'command is going to be {command}')
    os.system(command)
