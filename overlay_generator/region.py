import random
import math
from .linear import Point, Line
from .constants import (
    REMAINING_PITCHES,
    WIDTH,
    HALF_WIDTH,
    HEIGHT,
    HALF_HEIGHT
)
from .utility import remove_random_element

# TODO this file can almost certainly be streamlined
class Boundaries:
    def __init__(self, min_x=0, max_x=WIDTH, min_y=0, max_y=HEIGHT):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def contain_point(self, point):
        return (
            self.min_y <= point.y <= self.max_y and
            self.min_x < point.x <= self.max_x
        )


class Region:
    # both upper_bound and lower_bound are Line objects
    # lower means closer to 0 degrees on the unit circle
    def __init__(self, lower_bound, upper_bound):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.pitch = remove_random_element(REMAINING_PITCHES)

    def either_bound(self):
        return random.choice([self.lower_bound, self.upper_bound])

    def is_y_oriented(self):
       return self.lower_bound.end.has_extreme_y() and self.upper_bound.end.has_extreme_y()

    def get_random_point_in_region(self):
        if self.is_y_oriented():
            if self.either_bound().end.y == 0:
                random_y = random.randrange(HALF_HEIGHT)
            else:
                random_y = random.randrange(HALF_HEIGHT - 1, HEIGHT)

            print(f'random y is {random_y}')

            lower_bound_x = self.lower_bound.get_x_from(random_y)
            upper_bound_x = self.upper_bound.get_x_from(random_y)
            # will get an error if these are in the wrong order
            # TODO verify that I actually need to test this
            min_x = math.floor(min(lower_bound_x, upper_bound_x))
            max_x = math.ceil(max(lower_bound_x, upper_bound_x))

            random_x = random.randrange(min_x, max_x)

            return Point((random_x, random_y))
        else:
            if self.either_bound().end.x == 0:
                random_x = random.randrange(HALF_WIDTH)
            else:
                random_x = random.randrange(HALF_WIDTH - 1, WIDTH)

            lower_bound_y = self.lower_bound.get_y_from(random_x)
            upper_bound_y = self.upper_bound.get_y_from(random_x)
            # will get an error if these are in the wrong order
            # TODO verify that I actually need to test this
            min_y = math.floor(min(lower_bound_y, upper_bound_y))
            max_y = math.ceil(max(lower_bound_y, upper_bound_y))

            random_y = random.randrange(min_y, max_y)

            return Point((random_x, random_y))
    def get_edge(self):
        if self.is_y_oriented():
            edge_start = self.lower_bound.end.x
            edge_end = self.upper_bound.end.x
            y_val = self.either_bound().end.y
            return Line(
                Point((edge_start, y_val)),
                Point((edge_end, y_val))
            )
        else:
            edge_start = self.lower_bound.end.y
            edge_end = self.upper_bound.end.y
            x_val = self.either_bound().end.x
            return Line(
                Point((x_val, edge_start)),
                Point((x_val, edge_end))
            )

    def get_midpoint_in_region(self):
        center = self.either_bound().start
        if self.is_y_oriented():
            max_x = max(self.lower_bound.end.x, self.upper_bound.end.x)
            min_x = min(self.lower_bound.end.x, self.upper_bound.end.x)
            mid_x = min_x + ((max_x - min_x) / 2)
            y_val = self.either_bound().end.y
            endpoint_for_midline = Point([mid_x, y_val])
            print(f'endpoint for y oriented line is {endpoint_for_midline}')
            print(f'its original ends were {self.upper_bound.end} and {self.lower_bound.end}')
        else:
            max_y = max(self.lower_bound.end.y, self.upper_bound.end.y)
            min_y = min(self.lower_bound.end.y, self.upper_bound.end.y)
            mid_y = min_y + ((max_y - min_y) / 2)
            x_val = self.either_bound().end.x
            endpoint_for_midline = Point([x_val, mid_y])
            print(f'endpoint for x oriented line is {endpoint_for_midline}')
            print(f'its original ends were {self.upper_bound.end} and {self.lower_bound.end}')
        midpoint_x = center.x + ((endpoint_for_midline.x - center.x) / 2)
        midpoint_y = center.y + ((endpoint_for_midline.y - center.y) / 2)
        midpoint = Point([midpoint_x, midpoint_y])
        print(f'midpoint is {midpoint}')
        return midpoint

    def is_point_in_self(self, coordinates):
        # ray casting algorithm: https://en.wikipedia.org/wiki/Point_in_polygon
        x,max_y = coordinates
        center = self.either_bound().start
        if self.is_y_oriented():
            if self.either_bound().end.y == 0:
                # TODO: is this conditional necessary?
                if max_y > self.either_bound().start.y:
                    max_y = self.either_bound().start.y
            min_x = min(self.lower_bound.end.x, self.upper_bound.end.x)
            max_x = max(self.lower_bound.end.x, self.upper_bound.end.x)
            boundaries = Boundaries(max_y = max_y, min_x = min_x, max_x = max_x)
        else:
            if self.either_bound().end.x < center.x:
                max_x = center.x
                boundaries = Boundaries(max_y = max_y, max_x = max_x)
            else:
                min_x = center.x
                boundaries = Boundaries(max_y=max_y, min_x=min_x)

        lower_bound_intersection = self.lower_bound.get_y_from(x, boundaries)
        upper_bound_intersection = self.upper_bound.get_y_from(x, boundaries)
        if self.is_y_oriented():
            # if region is x oriented, then edge is a vertical line.
            # this will be parallel to the drawn ray, so there will be no intersection
            max_x = max(self.lower_bound.end.x, self.upper_bound.end.x)
            min_x = min(self.lower_bound.end.x, self.upper_bound.end.x)
            x_boundaries = Boundaries(max_x = max_x, min_x = min_x, max_y = max_y)
            edge_intersection = self.get_edge().get_y_from(x, x_boundaries)
        else:
            edge_intersection = None
        possible_intersections = [lower_bound_intersection, upper_bound_intersection, edge_intersection]

        intersections = list(
            filter(lambda x: x is not None, possible_intersections))
        if len(intersections) % 2 == 1:
            return True
        else:
            return False
