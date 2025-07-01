#!/usr/bin/env python3

import sys
import datetime
import subprocess
import time

last_check_time = input("Please tell me last gascheck time (Answer like 21:49)  ")
print("Last check: ", last_check_time)

#____ User param ____
#timediff_minutes=2*60+30 #[min]
#timediff_minutes=2*60 #[min]
timediff_minutes=4*60 #[min]
#timediff_minutes=0.5 #[min]
#timediff_minutes=8*60 #[min]
#____________________
last_check_arr=last_check_time.split(":")
last_check_hour=last_check_arr[0]
last_check_min=last_check_arr[1]
last_check_hour=int(last_check_hour)
last_check_min=int(last_check_min)
last_time = datetime.time(last_check_hour,last_check_min)

while True:
  current_time = datetime.datetime.now().time()
  elapsed_time = datetime.datetime.combine(datetime.date.today(), current_time)- datetime.datetime.combine(datetime.date.today(), last_time)
  if elapsed_time.total_seconds() < 0:
    elapsed_time = datetime.datetime.combine(datetime.date.today(), current_time) - datetime.datetime.combine(datetime.date.today()-datetime.timedelta(days=1), last_time)
  if elapsed_time.total_seconds() >= timediff_minutes * 60:  # [sec]
    print("Please go gas check!")
    # subprocess.Popen(['aplay','/home/sks/sound/gascheck.wav'])
    # time.sleep(4)
    # subprocess.Popen(['aplay','/home/sks/sound/gascheck.wav'])
    command = 'aplay -q /home/sks/sound/gascheck.wav'
    # command = 'play -q /home/sks/sound/gascheck.wav'
    subprocess.run(command, shell=True)
    time.sleep(1)
    subprocess.run(command, shell=True)
    last_time = current_time
    continue
  else:
    print("Last gas check: ", last_time)
    print("elpased time:   ", elapsed_time)
    print("gas check call is working... (time interval: ", timediff_minutes, " min)")
  time.sleep(120)
  # time.sleep(1)
