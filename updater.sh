#!/bin/bash
docker exec -it joins rm fas.py
#docker exec -it joins rm bond.py
docker exec -it joins rm keybds.py
wget -O fas.py https://raw.githubusercontent.com/Lordsniffer22/force/main/fas.py &>/dev/null
#wget -O bond.py https://raw.githubusercontent.com/Lordsniffer22/force/main/bond.py &>/dev/null
wget -O keybds.py https://raw.githubusercontent.com/Lordsniffer22/force/main/keybds.py &>/dev/null

docker cp fas.py joins:/app
#docker cp bond.py joins:/app
docker cp keybds.py joins:/app

sudo rm -rf *.py

docker restart joins
