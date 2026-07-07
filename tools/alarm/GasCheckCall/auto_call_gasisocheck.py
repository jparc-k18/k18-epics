#!/usr/bin/env python3

import os
import sys
import datetime
import subprocess
import time

col_red="\033[31m"
col_grn="\033[32m"
col_ylw="\033[33m"
col_blu="\033[34m"
col_cyn="\033[36m"
col_def="\033[0m"

last_check_time = input("Please tell me last gascheck time (Answer like 21:49)  ")
print("Last check: ", last_check_time)

#____ User param ____
gas_timediff_minutes=2*60 #[min]
#gas_timediff_minutes=4*60 #[min]
iso_timediff_minutes=30   #[min]
#iso_timediff_minutes=8*30   #[min]
# gas_timediff_minutes=1 #[min]
# iso_timediff_minutes=0.5  #[min]
#____________________
last_check_arr=last_check_time.split(":")
last_check_hour=last_check_arr[0]
last_check_min=last_check_arr[1]
last_check_hour=int(last_check_hour)
last_check_min=int(last_check_min)

last_gas_time = datetime.time(last_check_hour,last_check_min)
last_iso_time = datetime.time(last_check_hour,last_check_min)

def main():
  while True:
    clear_screen()
    current_time = datetime.datetime.now().time()

    global last_gas_time, last_iso_time
    check_interval = min(gas_timediff_minutes, iso_timediff_minutes)/5.
    print(f"check time: {current_time.replace(microsecond=0)} (interval: {check_interval} min)")

    #last_gas_time = call_check('gas', gas_timediff_minutes, current_time, last_gas_time)
    last_gas_time = call_check('GasHe', gas_timediff_minutes, current_time, last_gas_time)
    last_iso_time = call_check('isoC4H10', iso_timediff_minutes, current_time, last_iso_time)

    time.sleep(check_interval*60)

#____________________
def call_check(name, timediff, current_time, last_time):
  print(f"{col_grn}need {name} check?{col_def} [Last: {last_time.replace(microsecond=0)}]")
  elapsed_time = datetime.datetime.combine(datetime.date.today(), current_time) - datetime.datetime.combine(datetime.date.today(), last_time)
  if elapsed_time.total_seconds() < 0:
    elapsed_time = datetime.datetime.combine(datetime.date.today(), current_time) - datetime.datetime.combine(datetime.date.today()-datetime.timedelta(days=1), last_time)

  formatted_time = (datetime.datetime.min+elapsed_time).strftime("%H:%M:%S")
  if elapsed_time.total_seconds() >= timediff * 60:  # [sec]
    print(f"  {formatted_time} > {timediff} min")
    print(f"  -> {col_ylw}Please go {name} check!{col_def}")
    command = 'aplay -q /home/sks/sound/'+name+'check.wav'
    # print(command)
    # time.sleep(1)
    # print(command)
    subprocess.run(command, shell=True)
    time.sleep(1)
    subprocess.run(command, shell=True)
    return current_time
  else:
    print(f"  {formatted_time} < {timediff} min")
    print(f"  -> No need {name} check")
    return last_time

#___________________________
def clear_screen():
  os.system('cls' if os.name == 'nt' else 'clear')

#____________________
if __name__ == "__main__":
  main()
