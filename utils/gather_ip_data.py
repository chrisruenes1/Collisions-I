import subprocess
import re
import paramiko
import json

# from constants.service_ports import INDEX_PORT

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def find_rpi_ips():
    with open('constants/ip_addr_constants.py', 'r+') as f:
        f.truncate(0)
    nmap_result = subprocess.run(
        [
            '/bin/bash', '-i', '-c',
            'find-pis-in-dtown'
        ],
        stdout=subprocess.PIPE
    ).stdout.decode('utf-8')

    parts = nmap_result.split('\n')
    ip_lines_regex = re.compile("Nmap scan report for *")
    filtered_list = list(filter(ip_lines_regex.match, parts))
    ips = list(map(parse_ip_output, filtered_list))
    for ip in ips:
        handle_ip(ip)

def parse_ip_output(ip_info): 
    return ip_info.replace('Nmap scan report for ', '')

def handle_ip(ip):
    ssh.connect(hostname=ip, username='pi')
    # revert to constant instead of hard-coded 5000
    command = f'curl localhost:{5000}'
    _, ssh_stdout, _ = ssh.exec_command(command)
    response =  ssh_stdout.read().decode('utf-8')
    color = json.loads(response)['color']
    with open('constants/ip_addr_constants.py', 'a') as f:
        line = f'{color.upper()}_ROBOT_IP = "{ip}"'
        f.write(line)

find_rpi_ips()
        
