# bin/bash

# usage ./generate_index_server blue

cp template.py index_server.py

sed -i ".bak" "s/COLOR/$1/" index_server.py
