from PIL import Image
from PIL import ImageDraw
from .constants import WIDTH, HEIGHT
from .linear import Point, Line
from .region import Region
from .utility import endpoint_for_nth_line, points_for_range
class Overlay:
    def __init__(self, regions, image, drawObject):
        self.regions = regions
        self.image = image
        self.drawObject = drawObject
    def find_pitch_for_point(self, point):
        self.drawObject.text(point, "HERE")
        for region in self.regions:
            if region.is_point_in_self(point):
                return region.pitch
    def get_random_point_for_pitch(self, pitch):
        pitch_class = pitch % 12
        region = next((region for region in self.regions if region.pitch == pitch_class))
        return region.get_random_point_in_region()

def generate():
    # MODE, SIZE, COLOR
    im = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    lines = []
    regions = []
    center = Point([WIDTH / 2, HEIGHT / 2])

    for index in range(12):
        endpoint = endpoint_for_nth_line(index)
        points = points_for_range(center, endpoint)
        line = Line(center, endpoint, points)

        if len(lines):
            region = Region(lines[-1], line)
            regions.append(region)

        lines.append(line)

        coordinate_sequence = list(map(lambda point: point.coordinates, points))
        draw.line(coordinate_sequence)

    regions.append(Region(lines[-1], lines[0]))

    for region in regions:
        point = region.get_midpoint_in_region()
        print("HERE I AM")
        draw.text(point.coordinates, str(region.pitch))
        im.save('out.png')

    return Overlay(regions, im, draw)
