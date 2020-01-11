#!/bin/sh
rm ~/.config/GIMP/2.10/plug-ins/FontGen.py
cp ./FontGen.py ~/.config/GIMP/2.10/plug-ins/.
chmod 777 ~/.config/GIMP/2.10/plug-ins/FontGen.py
pkill "gimp"
gimp&
