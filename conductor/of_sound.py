import os
from constants.service_ports import TONE_GENERATOR_PORT
from utils.get_ip_for_color import get_ip_for_color

def play_pitch(pitch, duration, color):
    curl_command = f'curl \'{TONE_GENERATOR_PORT}/start?duration={duration}&pitch={pitch}\''
    command = f'ssh \'pi@{get_ip_for_color(color)}\' \"{curl_command}\"'
    print(f'command is going to be {command}')
    os.system(command)

def start_pitch(pitch, shape, color):
    curl_command = f'curl \'{TONE_GENERATOR_PORT}/go?pitch={pitch}&shape={shape}\''
    command = f'ssh \'pi@{get_ip_for_color(color)}\' \"{curl_command}\"'
    print(f'command is going to be {command}')
    os.system(command)

def stop_pitch(color):
    curl_command = f'curl \'{TONE_GENERATOR_PORT}/stop\''
    command = f'ssh \'pi@{get_ip_for_color(color)}\' \"{curl_command}\"'
    os.system(command)




