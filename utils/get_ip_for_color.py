from constants.ip_addr_constants import BLUE_ROBOT_IP, PINK_ROBOT_IP, YELLOW_ROBOT_IP


def get_ip_for_color(color):
    if color == 'pink':
        return PINK_ROBOT_IP
    if color == 'blue':
        return BLUE_ROBOT_IP
    if color == 'yello':
        return YELLOW_ROBOT_IP