#!/bin/bash

#exec sshpass -p "axis" ssh axis@eb0 aplay -q /home/axis/sound/se_hatena.wav  // before 2021
#exec sshpass -p "beamtime" ssh sks@k18epics.monitor.k18net aplay -q /home/sks/sound/se_hatena.wav # before June2023
exec sshpass -p "beamtime" ssh sks@k18epics.monitor.k18net aplay -q /home/sks/sound/zudamon_ESSMonitor_streo.wav # before June2023
