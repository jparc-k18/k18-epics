#!/bin/bash

exec sshpass -p "axis" ssh axis@eb0 aplay -q /home/axis/sound/chicken-cry1.wav
