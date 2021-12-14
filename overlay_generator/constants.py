import math;

# TODO need to verify some assumptions about off-by-one-errors here
WIDTH = 640
HEIGHT = 480
HALF_WIDTH = math.floor(WIDTH / 2) + 1
HALF_HEIGHT = math.floor(HEIGHT / 2) + 1
REMAINING_PITCHES = list(range(12))