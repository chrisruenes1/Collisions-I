import MIDI

def load_and_prepare_midi_file(path):
    try:
        file = MIDI.MIDIFile(path)
        print("loaded file successfully")
    except:
        print('cannot find file. Make sure the file exists and that you are in the root of the directory')
        exit()
    file.parse()
    for _, track in enumerate(file.tracks):
            track.parse()
    return file