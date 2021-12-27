import re
from regex import time_regex, note_regex
from metadata import get_encoding
from encoding import decode

def parse_time(note_event):
    return round(float(re.search(time_regex, note_event).group(1)), 3)

def parse_note(note_event):
    # TODO: are these registers an octave higher than I expect?
    pitches = re.search(note_regex, note_event).group(0)
    encoding = get_encoding()
    return decode(pitches, encoding)