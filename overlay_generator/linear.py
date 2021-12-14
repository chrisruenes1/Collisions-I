from .constants import HEIGHT;

def calculate_slope_from(start, end):
    return (end.y - start.y) / (end.x - start.x)


def calculate_y_intercept_from(slope, point):
    return point.y - (slope * point.x)

class Point:
    def __init__(self, coordinate_duple):
        self.x = coordinate_duple[0]
        self.y = coordinate_duple[1]
        # TODO this should really be a function
        # so that it responds to changes in x and y
        self.coordinates = coordinate_duple

    def has_extreme_y(self):
        return self.y == 0 or self.y == HEIGHT

    def __str__(self):
        return str(self.x) + "," + str(self.y)

class Line:
    # TODO can probably remove all_points as an argument
    def __init__(self, start, end, all_points = []):
        self.all_points = all_points
        self.start = start
        self.end = end
        self.slope = calculate_slope_from(start, end)
        self.y_intercept = calculate_y_intercept_from(self.slope, end)

    # TODO it's possible I always want these to enforce the domain and range.
    def get_x_from(self, y):
        return (y - self.y_intercept) / self.slope

    def get_y_from(self, x, boundaries = None):
        y = (self.slope * x) + self.y_intercept
        if boundaries is None or boundaries.contain_point(Point((x,y))):
            return y
        else:
            return None
