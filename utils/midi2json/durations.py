from metadata import get_division, get_whole_note, get_tempo

def convert_beats_to_ms(beats):
    tempo = get_tempo()
    return beats * 60 / tempo

def convert_timestamp_to_beat(timestamp, start_point):
    division = get_division()
    whole_note = get_whole_note()
    from_start = (timestamp / division) - start_point
    return from_start / whole_note * 4

def get_duration_data(start_time, end_time):
    return {
        'ms_start': convert_beats_to_ms(start_time),
        'ms_end': convert_beats_to_ms(end_time),
        'ms_duration': convert_beats_to_ms(end_time - start_time),
        '__beat_length__': end_time - start_time, 
    }