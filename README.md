# Collisions-I
Public repo for work-in-progress collision bots codebase

This repo is a work in progress. Not everything here is guaranteed to work yet,
but with some tweeks, it is intended to work eventually.

What you can find in each folder:

- conductor: these files act as intermediaries between the main host server and the servers listening on the raspbery pis
- constants: self-explanatory, but includes ip addr and port info, and constants related to the robots' movement
- json: output from utils/generate_json_from_midi.py. A Player utility will consume these files and process in real time to coordinate the robot performance
- overlay_generator: generates a random overlay and assigns pitch classes to each resulting region
- provisioning: setup scripts and server definitions for raspberry pis
- store: very lightweight data store used by server
- utils: scripts for handling dynamic ip info and for parsing midi files

The robots behave slightly differently in each piece, but generally, when the server sends them a request to play a pitch, they:

- Attempt to travel to a randomly selected point in the region associated with the pitch
- Play the pitch once they arrive OR
- Wait for some other condition to be met, and then play the pitch OR
- Crash into each other or another object while traveling, and in these cases, spray paint on the floor, which is covered in giant blank sheet music paper
