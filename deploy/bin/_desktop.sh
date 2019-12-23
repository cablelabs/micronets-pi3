#!/bin/bash
# Create desktop shortcut

mkdir -p ~/.config/autostart

desktop_file=~/.config/autostart/proto-pi.desktop

echo "[Desktop Entry]" > $desktop_file
echo "Type=Application" >> $desktop_file
echo "Name=Micronets Proto-Pi" >> $desktop_file

cmd="/usr/bin/python3 $(echo $PWD | rev | cut -d'/' -f3- | rev)/python3/proto_pi.py"

echo "Exec=$cmd" >> $desktop_file
