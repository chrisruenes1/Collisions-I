from durations import convert_timestamp_to_beat
from metadata import get_track_name
from ui import confirm, response_negative
from subprocess import call

from metadata import get_division

def select_tracks(file):
    included_tracks = []
    print('review each track, and type either "y" or "n" to determine whether it should be included')
    for _, track in enumerate(file.tracks):
        track_name = get_track_name(track)
        print(track_name)
        response = confirm('include track? y/n', ['y', 'n'])
        if not response_negative(response):
            print_raw_track_events(track)
            start_point = float(input('enter_start_point_value'))
            included_tracks.append([track_name, print_track_events(track, start_point, False)])
            call('clear')
    return included_tracks

def print_track_events(track, start_point, to_stdout = True):
    parsed_events = []
    for _, event in enumerate(track.events):
        message = f'{convert_timestamp_to_beat(event.time, start_point)}: {event.message}'
        if to_stdout:
            print(message)
        else:
            parsed_events.append(message)
    if not to_stdout:
        return '\n'.join(parsed_events)

def print_raw_track_events(track):
    division = get_division()
    for _, event in enumerate(track.events):
        print(f'{event.time / division}: {event.message}')