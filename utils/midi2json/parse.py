#!/usr/bin/env python

# TODO learn how to move this around, but for now must be called from root of directory
import argparse

from tracks import print_raw_track_events, select_tracks
from ui import confirm, confirm_entry
from metadata import get_file_data, delete_temp_data, persist
from json_utils import to_json, add_data_to_json, prepare_file_for_current_track, prepare_json_file
from midi_utils import load_and_prepare_midi_file
from note_pair import convert_midi_messages_to_note_pairs
from encoding import get_encoding
from wave_types import get_wave_type_data
from regex import note_event_regex

parser = argparse.ArgumentParser(description='get movement name')
parser.add_argument(
    'name', type=str, help='the name (without path) of the movement to parse')
args = parser.parse_args()

path = f"./Score/Midi/{args.name}.mid"
print(f"path is {path}")
file = load_and_prepare_midi_file(path)

division = file.division
persist('division', division)

print('review last track data, and determine required (start_point and whole_note) values from it')
print_raw_track_events(file.tracks[-1])

confirm('enter "y" once done reviewing\n', ['y'])

whole_note, tempo = get_file_data()
confirm_entry(f'whole_note is {whole_note}, and tempo is {tempo}', get_file_data)

persist('whole_note', whole_note)
persist('tempo', tempo)

included_tracks = select_tracks(file)

# TODO better way to do this?
def call_select_tracks():
    select_tracks(file)

confirm_entry(f'included tracks are: {included_tracks}', call_select_tracks)

json_filename = f'json/{args.name}.json'
prepare_json_file(json_filename)

get_encoding()

for idx, included_track in enumerate(included_tracks):
    track_name, track = included_track
    track_data = track.split('\n')
    note_event_midi_messages = list(filter(note_event_regex.match, track_data))
    note_pairs = convert_midi_messages_to_note_pairs(note_event_midi_messages)
    wave_type_data = None
    if input(f'skip wave type data for {track_name}? y/n') == 'y':
        processed_note_events = note_pairs
        # TODO it could come up that I still need to compress some of this?
        # though it is potentially less important, it may just sitll lead to a bunch
        # of unnecessary and very quick movement
    else:
        wave_type_data, processed_note_events = get_wave_type_data(track_name, note_pairs)
    prepare_file_for_current_track(json_filename, track_name)
    for idx, note_pair in enumerate(processed_note_events):
        data = to_json(note_pair, wave_type_data[idx] if wave_type_data else None)
        add_data_to_json(json_filename, track_name, data)

print(f'wrote json data to {json_filename}')
delete_temp_data()
