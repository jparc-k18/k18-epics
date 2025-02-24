#!/usr/bin/env python3

import datetime
import subprocess
import time
import os
import socket
import sys
import requests
import time
import epics

import statistics
from collections import deque

from pathlib import Path

import global_variable as g

#___________________________
def clear_screen():
  os.system('cls' if os.name == 'nt' else 'clear')


def restart_ioc(session):
  # check if the session exists or not
  result = subprocess.run(
    ["tmux", "has-session", "-t", session],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
  )
  if result.returncode == 0:
    killcmd = ["tmux","kill-session","-t", session]
    subprocess.run(killcmd, check=True)
    time.sleep(1)
    home_dir = Path.home()
    startcmd = [f"{home_dir}/k18epics/epicsApp/start.sh"]
    subprocess.run(startcmd, check=True)
  else:
    print(f"Error: tmux session '{session}' doesn't exist!")

def ippower_cycle(server,ip, port, user, password):
    with open('ippower.log', 'a') as f:
      f.write(f'{datetime.datetime.now()}\n')
    proxies = {
      "http": f"http://{server}",
      "https": f"https://{server}"
    }
    session = requests.Session()
    session.proxies = proxies
    off_url = f"http://{user}:{password}@{ip}/set.cmd?cmd=setpower+p{port}=0"
    session.get(off_url)
    print(f"Port {port} OFF")
    time.sleep(5)
    on_url = f"http://{user}:{password}@{ip}/set.cmd?cmd=setpower+p{port}=1"
    session.get(on_url)
    print(f"Port {port} ON")

def get_pv_value(pv_name):
    try:
      pv = epics.PV(pv_name)
      time.sleep(0.1)

      if not pv.connected:
        with open('epics_notconnected.log', 'a') as f:
          f.write(f'pv not connected in get_pv_value({pv_name}): {datetime.datetime.now()}\n')
        print("Error in connecting to pv in  get_pv_value")
        time.sleep(2)
        return None
      pv_value = epics.caget(pv_name,timeout=1.0)
      print(f"{pv_name}: {type(pv_value)}")
      if isinstance(pv_value,float):
        return float(pv_value)
      else:
        return None
    except Exception as e:
      print(f"Error in get_pv_value: {e}")
      return None

def main():
    server = g.SERVER
    ip = g.IP_ADDRESS
    port = g.PORT
    user = g.USERNAME
    password = g.PASSWORD
    k18d4_max_size = 5
    s2sd1_max_size = 100
    k18d4list = deque(maxlen=k18d4_max_size)
    s2sd1list = deque(maxlen=s2sd1_max_size)
    while True:
      clear_screen()
      k18d4field = get_pv_value("K18MAG:D4:FLD")
      k18d4cmon = get_pv_value("HDPS:K18D4:CMON")
      k18d4cset = get_pv_value("HDPS:K18D4:CSET")
      k18d4cdiff = abs(abs(k18d4cmon)-abs(k18d4cset))
      if (k18d4field is not None):
        # if (k18d4cmon is not None) and
        #    (k18d4cset is not None) ):
        # mom = value * 0.299792 * 4
        mom = k18d4field * 0.299792 * 4
        k18d4list.append(k18d4field)
        formatted = ", ".join(f"{val:.6f}" for val in k18d4list)
        print(f"[{formatted}]")
        if len(k18d4list)==k18d4_max_size and len(set(k18d4list))==1:
          print(f'k18d4field is the same value in {k18d4_max_size} times')
        # arrange
        print(f"--------------------------")
        print(f"K18D4 FLD: {k18d4field:.5f} [T]")
        print(f"beam mom: {mom:.5f} [GeV/c]")
        if abs(k18d4field) < 0.05:
          if (k18d4cdiff<100):
            print("\033[31m\033[1mERROR\033[0m")
            # ippower_cycle(server,ip, port, user, password)
            time.sleep(5)
            # restart_ioc("ioc_sksd4")
      else:
        # if you have error
        print("Failed to get k18d4 field value.")
        if (k18d4cdiff<100):
          # ippower_cycle(server,ip, port, user, password)
          time.sleep(5)
          # restart_ioc("ioc_sksd4")

      time.sleep(2)

if __name__ == "__main__":
    main()
