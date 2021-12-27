import re
import os

def get_file_data():
    whole_note = float(input('enter whole note value\n'))
    tempo = float(input('enter tempo\n'))
    return [whole_note, tempo]

def get_track_name(track):
    result = re.search("Track Name -> text=b'([a-zA-z\s]+)'", str(track))
    if result:
        return result.group(1)
    return None

def persist(key, value):
    with open(f'utils/midi2json/{key}.temp.txt', 'w+') as f:
        f.write(str(value))

def get_whole_note():
    with open('utils/midi2json/whole_note.temp.txt', 'r') as f:
        return float(f.read())

def get_division():
    with open('utils/midi2json/division.temp.txt', 'r') as f:
        return float(f.read())

def get_tempo():
    with open('utils/midi2json/tempo.temp.txt', 'r') as f:
        return float(f.read())

def get_encoding():
    with open('utils/midi2json/encoding.temp.txt', 'r') as f:
        entries = f.read()
        dict = {}
        for _, entry in enumerate(entries.split('\n')):
            pitch, sub = entry.split('=')
            dict[pitch] = sub
        return dict

def delete_temp_data():
    os.remove('utils/midi2json/whole_note.temp.txt')
    os.remove('utils/midi2json/division.temp.txt')
    os.remove('utils/midi2json/tempo.temp.txt')
    os.remove('utils/midi2json/encoding.temp.txt')
