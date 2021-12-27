import pdb
import re
from ui import confirm, response_negative, confirm_entry
from metadata import persist

def get_encoding(autorequire = False):
    needs_encoding = confirm('does the file require encoding?', ['y','n']) if not autorequire else 'y'
    if (response_negative(needs_encoding)):
        return []
    else:
        encoding = input('enter encoding in the comma-separated format pitch=str, ie G3=pedal,D3=region')
        if validate_encoding(encoding):
            if confirm_entry(encoding, get_encoding):
                persist('encoding', re.sub(',', '\n', encoding))
        else:
            print('invalid entry')
            get_encoding(True)

def decode(pitches, encoding):
    for _, pitch in enumerate(list(encoding.keys())):
        pitches = re.sub(pitch, encoding[pitch], pitches)
    return pitches

def validate_encoding(str):
    regex = re.compile('[A-G][0-9]=\S+')
    entries = str.split(',')
    for _, entry in enumerate(entries):
        if not regex.match(entry):
            return False
    return True

