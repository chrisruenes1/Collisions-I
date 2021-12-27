import re

note_regex = '[A-G][#b]?[0-9]'
note_event_regex = re.compile(f'.*{note_regex} (OFF|ON).*')
note_on_regex = re.compile('.*(ON).*')
note_off_regex = re.compile('.*(OFF).*')
time_regex = '(\d+\.\d+):'