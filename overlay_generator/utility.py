import random
from .constants import HALF_WIDTH, WIDTH, HEIGHT
from .linear import Point
from .circular import MULTIPLIERS

def remove_random_element(arr):
    index = random.randrange(len(arr))
    el = arr.pop(index)
    return el

def get_x_window_for(max_x):
    return range(HALF_WIDTH, WIDTH) if max_x >= HALF_WIDTH else range(0, HALF_WIDTH)

# TODO: use utility methods and handle undefined
def points_for_range(point_one, point_two):
    (x1, y1), (x2, y2) = point_one.coordinates, point_two.coordinates
    slope = float(y2 - y1) / (x2 - x1)

    def find_y_given(x):
        return (slope * (x - x1)) + y1
    min_x = min(x1, x2)
    max_x = max(x1, x2)
    x_range = max_x - min_x
    x_window = get_x_window_for(max_x)
    xs = [(HALF_WIDTH / x_range) * sample for sample in x_window]
    ys = [find_y_given(x) for x in xs]
    return list(map(lambda coordinates: Point(coordinates), list(zip(xs, ys))))

def endpoint_for_nth_line(n):
    base_x = WIDTH / 3
    base_y = HEIGHT / 3

    multiplier = MULTIPLIERS[n]
    return Point((multiplier.x * base_x, multiplier.y * base_y))
