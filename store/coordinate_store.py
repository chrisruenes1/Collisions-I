import os
from overlay_generator.linear import Point
from constants import COORDINATE_STORE_PATH


def store_point(point):
    file = open(COORDINATE_STORE_PATH, 'w')
    file.write(str(point))
    file.close()

def retrieve_latest_point():
    file = open(COORDINATE_STORE_PATH, 'r')
    coordinates = file.read()
    file.close()
    if coordinates is None:
        return ''
    else:
        return Point(coordinates.split(','))


def clear_store():
    os.system(f'rm {COORDINATE_STORE_PATH}')
