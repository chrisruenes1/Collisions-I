import json
from durations import get_duration_data

def to_json(note_pair, wave_type):
    json_data = get_duration_data(note_pair.start_time, note_pair.end_time)
    json_data.update({ 'pitches': note_pair.pitches })
    if wave_type:
        json_data.update({ 'waveType': wave_type })
    return json_data

def add_data_to_json(json_filename, track_name, data):
    json_file_for_reading = open(json_filename, 'r')
    json_object = json.load(json_file_for_reading)
    json_file_for_reading.close()

    json_object[track_name].append(data)

    json_file_for_writing = open(json_filename, 'w')
    json.dump(json_object, json_file_for_writing, indent=4)
    json_file_for_writing.close()

def prepare_json_file(file_name):
    with open(file_name, 'w') as f:
        f.write(json.dumps({}))

def prepare_file_for_current_track(file_name, track_name):
    with open(file_name, 'r+') as f:
        current_json = json.loads(f.read())
        current_json[track_name] = []
        f.seek(0)
        f.write(json.dumps(current_json))
        f.truncate()
