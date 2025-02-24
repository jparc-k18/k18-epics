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
  result = subprocess.run(
    ["tmux", "has-session", "-t", session],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
  )
  # check if the session exists or not
  if result.returncode == 0:
    killcmd = ["tmux","kill-session","-t", session]
    subprocess.run(killcmd, check=True)
    time.sleep(1)
    home_dir = Path.home()
    startcmd = [f"{home_dir}/k18epics/epicsApp/start.sh"]
    subprocess.run(startcmd, check=True)
  else:
    print(f"Error: tmux session '{session}' doesn't exist!")
    home_dir = Path.home()
    startcmd = [f"{home_dir}/k18epics/epicsApp/start.sh"]
    subprocess.run(startcmd, check=True)
  time.sleep(10)

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
    time.sleep(5)

def get_pv_value(pv_name):
    try:
      pv = epics.PV(pv_name)
      time.sleep(0.1)
      if not pv.connected:
        with open('epics_notconnected.log', 'a') as f:
          f.write(f'pv not connected in get_pv_value: {datetime.datetime.now()}\n')
        print(f"Error in connecting to pv in  get_pv_value({pv_name})")
        return None
      pv_value = epics.caget(pv_name,timeout=1.0)
      if isinstance(pv_value,float):
        return float(pv_value)
      else:
        return None
    except Exception as e:
      print(f"Error in get_pv_value: {e}")
      return None

def rehold_NMR():
    """
    send S2SD1 NMR rehold signal
    """
    HOST = "192.168.30.20"
    PORT = int(10001)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((HOST,PORT))
      if s: print(f"connected to {HOST}:{PORT}")

    # if s.fileno() == -1:
    #   print(" connection failure ", HOST)
    #   sys.exit(1)

    filepath="/home/sks/k18epics/tools/k18mag/rehold_signal.txt"
    if os.path.exists(filepath):
      with open(filepath, "r") as f:
        content = f.read().strip()
      if len(content) > 0 and content[0] in ('a', 'b', 'c', 'd'):
        print("SKS NMR send rehold command")
        with open(filepath, "w") as fw:
          fw.write("0")
        s.sendall(content[0].encode('utf-8'))
        time.sleep(0.1)
    else:
      print("rehold_signal.txt was not found")


def main():
    server = g.SERVER
    ip = g.IP_ADDRESS
    port = g.PORT
    user = g.USERNAME
    password = g.PASSWORD
    iocname_k18d4 = "ioc_k18d4"
    k18d4_max_size = 5
    s2sd1_max_size = 100
    k18d4list = deque(maxlen=k18d4_max_size)
    s2sd1list = deque(maxlen=s2sd1_max_size)
    while True:
      k18d4field = get_pv_value("K18MAG:D4:FLD")
      k18d4cmon = get_pv_value("HDPS:K18D4:CMON")
      k18d4cset = get_pv_value("HDPS:K18D4:CSET")
      k18d4cdiff = abs(abs(k18d4cmon)-abs(k18d4cset))
      if(k18d4field is not None):
        mom = k18d4field * 0.299792 * 4
        k18d4list.append(k18d4field)
        print(f"--------------------------")
        print(f"K18D4 FLD: {k18d4field:.5f} [T]")
        print(f"beam mom: {mom:.5f} [GeV/c]")
        if abs(k18d4field) < 0.05:
          if (k18d4cdiff<100 and k18d4cset>100):
            print("\033[31m\033[1mERROR\033[0m")
            ippower_cycle(server,ip, port, user, password)
            with open('ippower.log', 'a') as f:
              f.write(f'k18d4fld {k18d4field}: {datetime.datetime.now()}\n')
            restart_ioc(iocname_k18d4)
        if len(k18d4list)==k18d4_max_size and len(set(k18d4list))==1:
          print(f'k18d4field is the same value in {k18d4_max_size} times')
          with open('epics_notconnected.log', 'a') as f:
            f.write(f'k18d4field is the same value in {k18d4_max_size} times: {datetime.datetime.now()}\n')
          ippower_cycle(server,ip, port, user, password)
          restart_ioc(iocname_k18d4)
      else:
        print("Failed to get k18d4 field value.")
        with open('epics_notconnected.log', 'a') as f:
          f.write(f'pv not connected in main: {datetime.datetime.now()}\n')
        print(f'cmon: {k18d4cmon}, cset: {k18d4cset}, diff: {k18d4cdiff}')
        if (k18d4cdiff<100):
          # ippower_cycle(server,ip, port, user, password)
          restart_ioc(iocname_k18d4)

      s2sd1field = get_pv_value("K18MAG:S2SD1:FLD")
      s2sd1cset = get_pv_value("HDPS:S2SD1:CSET")
      if s2sd1field is not None:
        print(f"--------------------------")
        print(f"S2SD1 FLD: {s2sd1field:.5f} [T]")
        print(f"S2SD1 Jump is monitoring...")
        s2sd1list.append(s2sd1field)
        if (abs(s2sd1field)<0.1 and s2sd1cset>100):
          print("\033[31m\033[1mERROR\033[0m")
          s2sd1cmon = get_pv_value("HDPS:S2SD1:CMON")
          s2sd1cset = get_pv_value("HDPS:S2SD1:CSET")
          diff = abs(abs(s2sd1cmon)-abs(s2sd1cset))
          if diff<100 and abs(s2sd1cmon)>1000:
            print(f"S2SD1 current: {s2sd1cmon:.1f} [A]")
            # rehold_NMR();
            print(" Need NMR rehold")
            if abs(s2sd1field)>0.1:
              time.sleep(3)
              print("Succeeded in reholding")
            print(f"--------------------------")
          s2sd1list.pop()
        else:
          s2sd1mean = statistics.mean(s2sd1list)
          print(f" mean: {s2sd1mean:.5f}[T]", end='')
          if abs(s2sd1field-s2sd1mean)>0.0002:
          # if abs(s2sd1field-s2sd1mean)>0.000010:
            print(f" (jumping!!)")
            command = 'aplay -q /home/sks/sound/d1jump.wav'
            # print(command)
            # time.sleep(5)
            # print(command)
            subprocess.run(command, shell=True)
            time.sleep(1)
            subprocess.run(command, shell=True)
            s2sd1list.pop()
          else:
            print()
      else:
        # if you have error
        print("\033[31m\033[1mERROR\033[0m")
        print("Failed to get s2sd1 field value.")
      time.sleep(3)
      clear_screen()

if __name__ == "__main__":
    main()
