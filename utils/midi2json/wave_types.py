def validate_wave_type_data(track_name, note_events, wave_type_str):
    from event_compression import compress_note_pairs
    if (len(wave_type_str) != len(note_events)):
        print(f'length of track ({len(note_events)}) and length of wave type string ({len(wave_type_str)}) are off')
        choice = input('choose how to handle:\n1) reenter wave type string\n2) autocompress track\n3) manually compress track\n')
        switcher = {
            1: lambda: get_wave_type_data(track_name, note_events),
            2: lambda: compress_note_pairs(track_name, note_events, wave_type_str),
            3: lambda: compress_note_pairs(
                track_name,
                note_events,
                wave_type_str,
                input('enter compression schema in the format ie 5-8,13-15')
            )
        }
        func = switcher.get(int(choice))
        return func()
    return wave_type_str, note_events

def get_wave_type_data(track_name, note_events):
    wave_type_str = input(f'enter string of wave types for track {track_name}.\n0=square, 1=triangle, 2=sine\n')
    return validate_wave_type_data(track_name, note_events, wave_type_str)