
from metadata import get_whole_note

def events_are_significant(pair_one, pair_two):
    whole_note = get_whole_note()
    meaningful_space = whole_note / 16
    if pair_one.pitches != pair_two.pitches:
        return True
    if (pair_two.start_time - pair_one.end_time) < meaningful_space:
        return False
    return True

def append_appropriate_events(pair, on_insignificant_streak, running):
    if on_insignificant_streak:
        running[-1].end_time = pair.end_time
    else:
        running.append(pair)

def merge_insignificant_events(event_pairs):
    whole_note = get_whole_note()
    merged_note_events = []
    on_insignificant_streak = False
    for idx, pair in enumerate(event_pairs):
        if (idx == len(event_pairs) - 1):
            append_appropriate_events(pair, on_insignificant_streak, merged_note_events)
        else:
            next_pair = event_pairs[idx + 1]
            if events_are_significant(pair, next_pair, whole_note):
                append_appropriate_events(pair, on_insignificant_streak, merged_note_events)
                on_insignificant_streak = False
            else:
                if not on_insignificant_streak:
                    merged_note_events.append(pair)
                on_insignificant_streak = True
    return merged_note_events

def compress_note_pairs(track_name, note_pairs, wave_type_str, schema = None):
    from wave_types import validate_wave_type_data
    if schema:
        # TODO implement this
        None
    else:
        processed_note_events = merge_insignificant_events(note_pairs)
        return validate_wave_type_data(track_name, processed_note_events, wave_type_str)