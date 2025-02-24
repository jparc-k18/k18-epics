#!/usr/bin/env python3

import sys
import datetime
import subprocess
import time

last_check_time = None
if len(sys.argv) == 1:
  last_check_time = input("Please tell me last isoC4H10check time (Answer like 21:49)  ")
else:
  last_check_time = sys.argv[1]

#____ User param ____
timediff_minutes=30 #[min]
# timediff_minutes=0.2 #[min]

#____________________
last_check_arr=last_check_time.split(":")
last_check_hour=last_check_arr[0]
last_check_min=last_check_arr[1]
last_check_hour=int(last_check_hour)
last_check_min=int(last_check_min)
last_time = datetime.time(last_check_hour,last_check_min)

print("Last isoC4H10 check: ", last_time)

while True:
  current_time = datetime.datetime.now().time()
  elapsed_time = datetime.datetime.combine(datetime.date.today(), current_time) - datetime.datetime.combine(datetime.date.today(), last_time)
  if elapsed_time.total_seconds() < 0:  # [sec]
    elapsed_time = datetime.datetime.combine(datetime.date.today(), current_time) - datetime.datetime.combine(datetime.date.today()-datetime.timedelta(days=1), last_time)
  if elapsed_time.total_seconds() >= timediff_minutes * 60:  # [sec]
    print("Please go isoC4H10 check!")
    # command = 'play -q /home/sks/sound/isoC4H10check.wav'
    command = 'aplay -q /home/sks/sound/isoC4H10check.wav'    
    subprocess.run(command, shell=True)
    time.sleep(1)
    subprocess.run(command, shell=True)
    last_time = current_time
    continue
  else:
    print("\nLast isoC4H10 check: ", last_time)
    print("elapsed time:   ", elapsed_time)
    print("iso check call is working... (time interval: ", timediff_minutes, " min)")
  # time.sleep(120)
  time.sleep(timediff_minutes*60/2.)
