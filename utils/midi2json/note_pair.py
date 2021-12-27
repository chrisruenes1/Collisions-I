from collections import deque
from message_processing import parse_note, parse_time
from regex import note_on_regex, note_off_regex

class NotePair:
    def __init__(self, note_on_events, note_off_events):
        if (len(note_on_events) != len(note_off_events)):
            raise Exception(f'note on and off events must be same length ({len(note_on_events)} != {len(note_off_events)}')
        self.start_time = parse_time(note_on_events[0])
        self.end_time = parse_time(note_off_events[-1])
        on_pitches = list(map(parse_note, note_on_events))
        off_pitches = list(map(parse_note, note_off_events))
        if (on_pitches != off_pitches):
            raise Exception(f'on an off pitch events do not match; on: {on_pitches} / off: {off_pitches}')
        self.pitches = on_pitches
        self.__on_events__ = note_on_events
        self.__off_events__ = note_off_events

def convert_midi_messages_to_note_pairs(note_events):
    event_pairs = []
    queue = deque(note_events)
    while queue:
        note_on_events = []
        note_off_events = []
        while note_on_regex.match(queue[0]):
            note_on_events.append(queue.popleft())
        while len(note_off_events) < len(note_on_events):
            event = queue.popleft()
            if not note_off_regex.match(event):
                raise Exception(f'expected note on event to be note off event: {event}')
            note_off_events.append(event)
        event_pairs.append(NotePair(note_on_events, note_off_events))
    return event_pairs