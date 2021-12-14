#!/usr/bin/env python

# TODO learn how to move this around, but for now must be called from root of directory
import json
import argparse
import MIDI
import re
from subprocess import call
from collections import deque

def convert_timestamp_to_beat(timestamp, start_point):
    from_start = (timestamp / division) - start_point
    return from_start / whole_note * 4

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
    for _, event in enumerate(track.events):
        print(f'{event.time / division}: {event.message}')

def get_file_data():
    whole_note = float(input('enter whole note value\n'))
    tempo = float(input('enter tempo\n'))
    return [whole_note, tempo]


def confirm(prompt, valid_responses):
    awaiting_confirmation = True
    while awaiting_confirmation:
        response = input(prompt)
        if (response in valid_responses):
            awaiting_confirmation = False
            return response
        else:
            print('invalid response')


def response_negative(response):
    return response in ['n', None]

def confirm_entry(confirm_entries_prompt, get_data_fn):
    response = None
    while response_negative(response):
        response = confirm(
            f'{confirm_entries_prompt}. Confirm? y/n', ['y', 'n'])
        if (response_negative(response)):
            get_data_fn()

def select_tracks(file):
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

def get_track_name(track):
    result = re.search("Track Name -> text=b'([a-zA-z\s]+)'", str(track))
    if result:
        return result.group(1)
    return None

def process_note_event_pairs(note_on_events, note_off_events):
    validate_pair(note_on_events, note_off_events)
    base_note_on_event, base_note_off_event = [note_on_events[0], note_off_events[0]]
    # pdb.set_trace()
    start_time, end_time = [parse_time(base_note_on_event), parse_time(base_note_off_event)]
    duration_data = get_duration_data(start_time, end_time)
    pitches = list(map(parse_note ,note_on_events))
    duration_data.update({ 'pitches': pitches })
    return duration_data

def validate_pair(note_on_events, note_off_events):
    # TODO
    # need to make sure all note_on_events are note_on, and vice versa for note off
    # need to make sure pitches match up
    return True

def parse_time(note_event):
    time_regex = '(\d+\.\d+):'
    return round(float(re.search(time_regex, note_event).group(1)), 3)

def parse_note(note_event):
    # TODO: are these registers an octave higher than I expect?
    note_regex = '[A-G][#b]?[0-9]'
    return re.search(note_regex, note_event).group(0)

def convert_beats_to_ms(beats):
    return beats * 60 / tempo

def get_duration_data(start_time, end_time):
    return {
        'ms_start': convert_beats_to_ms(start_time),
        'ms_end': convert_beats_to_ms(end_time),
        'ms_duration': convert_beats_to_ms(end_time - start_time),
        '__beat_length__': end_time - start_time, 
    }

parser = argparse.ArgumentParser(description='get movement name')
parser.add_argument(
    'name', type=str, help='the name (without path) of the movement to parse')

args = parser.parse_args()

path = f"./Score/Midi/{args.name}.mid"
print(f"path is {path}")

try:
    file = MIDI.MIDIFile(path)
    print("loaded file successfully")
except:
    print('cannot find file. Make sure the file exists and that you are in the root of the directory')
    exit()
file.parse()
for _, track in enumerate(file.tracks):
        track.parse()

division = file.division

included_tracks = []

print('review last track data, and determine required (start_point and whole_note) values from it')
print_raw_track_events(file.tracks[-1])

confirm('enter "y" once done reviewing\n', ['y'])

whole_note, tempo = get_file_data()
confirm_entry(f'whole_note is {whole_note}, and tempo is {tempo}', get_file_data)

select_tracks(file)

# TODO better way to do this?
def call_select_tracks():
    select_tracks(file)

confirm_entry(f'included tracks are: {included_tracks}', call_select_tracks)

json_filename = f'json/{args.name}.json'
print(f'going to wrtie json data to {json_filename}')

def add_data_to_json(inst_name, data):
    json_file_for_reading = open(json_filename, 'r')
    json_object = json.load(json_file_for_reading)
    json_file_for_reading.close()

    json_object[inst_name].append(data)

    json_file_for_writing = open(json_filename, 'w')
    json.dump(json_object, json_file_for_writing, indent=4)
    json_file_for_writing.close()


with open(json_filename, 'w') as f:
    f.write(json.dumps({}))

for idx, included_track in enumerate(included_tracks):
    track_name, track = included_track
    track_data = track.split('\n')
    note_event_regex = re.compile('.*(OFF|ON).*')
    note_on_regex = re.compile('.*(ON).*')
    note_off_regex = re.compile('.*(OFF).*')
    note_events = list(filter(note_event_regex.match, track_data))
    note_on_events = []
    note_off_events = []
    with open(json_filename, 'r+') as f:
        current_json = json.loads(f.read())
        current_json[track_name] = []
        f.seek(0)
        f.write(json.dumps(current_json))
        f.truncate()
    queue = deque(note_events)
    with open(json_filename, 'r+') as f:
        while queue:
            while note_on_regex.match(queue[0]):
                note_on_events.append(queue.popleft())
            while len(note_off_events) < len(note_on_events):
                note_off_events.append(queue.popleft())
            data = process_note_event_pairs(note_on_events, note_off_events)
            note_on_events.clear()
            note_off_events.clear()
            add_data_to_json(track_name, data)
