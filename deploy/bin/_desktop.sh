#!/bin/bash
# Create desktop shortcut

mkdir -p ~/.config/autostart

echo "*** Creating desktop autostart file ***" 

desktop_file=~/.config/autostart/proto-pi.desktop

echo "[Desktop Entry]" > $desktop_file
echo "Type=Application" >> $desktop_file
echo "Name=Micronets Proto-Pi" >> $desktop_file

thisdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cmd="/usr/bin/python3 $(echo $thisdir | rev | cut -d'/' -f3- | rev)/python3/proto_pi.py"

echo "Exec=$cmd" >> $desktop_file
