import random
import math
import requests
from threading import Timer
import numpy as np

from constants import PIXELS_PER_SECOND, DEGREES_PER_SECOND
from utils.get_ip_for_color import get_ip_for_color

# may be the opposite, "right" is currently in the "counterclockwise" position
directions = ['left', 'right']
direction_to_query_params = {
    'forward': 'lmp=100&rmp=100',
    'left': 'lmp=-100&rmp=100',
    'right': 'lmp=100&rmp=-100',
    'back': 'lmp=-100&rmp=-100'
}

def move_to_point(destination, current, overlay, color): # can remove overlay after testing
    print("current point is " + str(current))
    print("destination point is " + str(destination))
    ip = get_ip_for_color(color)
    overlay.drawObject.text([destination.x, destination.y], "Go Here", fill=(0,255,0))
    overlay.drawObject.line([current.x, current.y, destination.x, destination.y], fill=(0,255,0)) # hypotenuse
    overlay.drawObject.line([current.x, current.y, current.x, destination.y], fill=(255,0,0)) # adjacent
    overlay.drawObject.line([current.x, destination.y, destination.x, destination.y], fill=(255,0,0)) # adjacent
    overlay.image.save('out.png')
    # TODO these aren't universally correct
    opposite = destination.x - current.x
    adjacent = destination.y - current.y
    hypotenuse = math.sqrt((opposite ** 2) + (adjacent ** 2))
    print("delta_x is " + str(opposite))
    print("delta_y is " + str(adjacent))
    sine = opposite / hypotenuse
    theta = math.degrees(math.asin(sine))
    if destination.y < current.y:
        # take the complimenatry angle
        if theta > 0:
            theta = 90 - theta
        else:
            theta = -90 - theta
    print("theta is " + str(theta))
    should_turn_counterclockwise = random.getrandbits(1)
    if theta > 0:
        delta = theta if should_turn_counterclockwise else (theta - 360)
    else:
        delta = (360 - np.abs(theta)) if should_turn_counterclockwise else theta
    
    print("counterclockwise is " + str(should_turn_counterclockwise) + " so going to turn " + str(delta))

    longtime = hypotenuse / PIXELS_PER_SECOND
    print(f'longtime is {longtime}')

    spintime = np.abs(delta) / DEGREES_PER_SECOND

    global reverse_timeout
    reverse_timeout = Timer(spintime, lambda: requests.get(f'pi@{ip}/motors_stop'))

    def stop_moving_and_spin_back():
        global reverse_timeout
        requests.get(f'pi@{ip}/motors_stop')
        reverse_direction = direction_to_query_params[directions[0]] if should_turn_counterclockwise else direction_to_query_params[directions[1]]
        reverse_url = f'pi@{ip}/motors_tank?{reverse_direction}'
        print('reverse timeout starting')
        reverse_timeout.start()
        requests.get(reverse_url)
        reverse_timeout.join()
        
    global move_timeout
    def stop_spinning_and_move():
        global move_timeout
        requests.get(f'pi@{ip}/motors_stop')
        move_url = f'pi@{ip}/motors_tank?{direction_to_query_params["forward"]}'
        move_timeout = Timer(longtime, stop_moving_and_spin_back)
        print('move timeout starting')
        move_timeout.start()
        requests.get(move_url)
        move_timeout.join()

    print(f'spintime is {spintime}')
    angle_direction = directions[should_turn_counterclockwise]
    angle_url = f'pi@{ip}/motors_tank?{direction_to_query_params[angle_direction]}'
    angle_timeout = Timer(spintime, stop_spinning_and_move)
    print('angle timeout starting')
    angle_timeout.start()
    requests.get(angle_url)
    angle_timeout.join()

    # TODO could always add some randomness for backwards too

def move_in_direction(direction, color):
    ip = get_ip_for_color(color)
    requests.get(f'pi{ip}/motors_tank?{direction_to_query_params[direction]}')

def stop(color):
    ip = get_ip_for_color(color)
    requests.get(f'pi@{ip}/motors_stop')
