#!/usr/bin/env python3

import datetime
import logging
import os
import subprocess

import global_variables as g

logger = logging.getLogger('__main__').getChild(__name__)

#______________________________________________________________________________
def event_number(run_number):
  with open(os.path.join(g.data_path, 'recorder.log')) as f:
    lines = f.readlines()
    for line in lines:
      columns = line.split()
      if len(columns) > 15:
        if run_number == int(columns[1]):
          print(int(columns[15]))
          return int(columns[15])
  print('cannot find')

#______________________________________________________________________________
def comment_info():
  info = dict()
  with open(os.path.join(g.data_path, 'misc', 'comment.txt'), 'r') as f:
    lines = f.readlines()
    for line in lines:
      columns = line.split()
      if len(columns) < 6:
        continue
      year = columns[0]
      date = columns[1]
      hms  = columns[2]
      run_number = int(columns[4][:-1])
      if run_number not in info:
        info[run_number] = dict()
      if '*:' in columns[5]:
        title = columns[6:]
      else:
        title = columns[7:]
      title = ' '.join(title)
      title = title.replace(',', '.')
      info[run_number]['Title'] = title
      if 'START' in columns[5]:
        start_time = f'{year}/{date} {hms}'
        info[run_number]['StartTime'] = start_time
        start_dt = datetime.datetime.strptime(
          start_time, '%Y/%m/%d %H:%M:%S')
      if 'STOP' in columns[5]:
        stop_time = f'{year}/{date} {hms}'
        info[run_number]['StopTime'] = stop_time
        stop_dt = datetime.datetime.strptime(
          stop_time, '%Y/%m/%d %H:%M:%S')
        elapsed_time = str(stop_dt - start_dt)
        info[run_number]['ElapsedTime'] = elapsed_time
        info[run_number]['StopTimeDT'] = stop_dt
        logger.debug(f'{run_number} {start_dt} - {stop_dt} ({elapsed_time}) {title}')
  logger.debug(info)
  return info

#______________________________________________________________________________
def recorder_info():
  info = dict()
  with open(os.path.join(g.data_path, 'recorder.log'), 'r') as f:
    lines = f.readlines()
    for line in lines:
      columns = line.split()
      if len(columns) == 20:
        n = int(columns[1])
        info[n] = dict()
        info[n]['EventNumber'] = int(columns[15])
        info[n]['Bytes'] = int(columns[18])
  logger.debug(info)
  return info

#______________________________________________________________________________
def scaler(run_number):
  info = dict()
  scaler_keys = [
  'Beam/Spill',
  'K-Beam/Spill',
  'Pi-Beam/Spill',
  'Beam',
  'K-Beam',
  'Pi-Beam',
  'Spill',
  'DAQ-Eff',
  'BeamxDAQEff',
  'Duty-Factor',
  ]
  for k in scaler_keys:
    info[k] = str()
  scaler_txt = os.path.join(g.subdata_path, 'scaler_2025apr',
                            f'scaler_{run_number:05d}.txt')
  rec_info = recorder_info()
  if run_number in rec_info:
    evnum = rec_info[run_number]['EventNumber']
  else:
    return info.values()
  if evnum == 0:
    return info.values()
  if evnum > 0 and not os.path.isfile(scaler_txt):
    # logger.warning(f'cannot find {scaler_txt}')
    # return info.values()
    return False
  scaler_dict = dict()
  with open(scaler_txt, 'r') as f:
    lines = f.readlines()
    for line in lines:
      columns = line.split()
      if len(columns) == 2 and columns[0] in scaler_keys:
        if '/' in columns[0] or 'Eff' in columns[0] or 'Factor' in columns[0]:
          info[columns[0]] = float(columns[1])
        else:
          info[columns[0]] = int(columns[1])
  try:
    info['BeamxDAQEff'] = info['Beam'] * info['DAQ-Eff']
    if info['Duty-Factor'] < 0.:
      info['Duty-Factor'] = 0.
  except:
    info['BeamxDAQEff'] = 0
    info['Duty-Factor'] = 0
  logger.debug(info)
  return info.values()

#______________________________________________________________________________
def trigger(run_number=None):
  if run_number is not None:
    trigger_log = os.path.join(
      g.subdata_path, f'trigger_2025apr/trigger_{run_number:05d}.log')
  if run_number is None or not os.path.isfile(trigger_log):
    logger.debug(f'cannot find {trigger_log}')
    return ['' for i in range(30)]
    # trigger_log = '/misc/subdata/HUL_Trigger/last.log'
  command = [os.path.join(g.subdata_path, 'HUL_Trigger/script/display.py'),
             '-n',
             trigger_log]
  proc = subprocess.run(command, capture_output=True, text=True)
  param = None
  tof_01_08 = None
  tof_09_16 = None
  tof_17_24 = None
  trig_on = [None for i in range(6)]
  trig_ps = [None for i in range(6)]
  trig_gate = [None for i in range(6)]
  trig = [None for i in range(6)]
  i = 0
  clock_on = None
  clock_gate = None
  rsv2_on = None
  rsv2_gate = None
  for line in proc.stdout.splitlines():
    columns = line.split()
    if len(columns) == 0:
      continue
    if param is None:
      param = os.path.basename(columns[0])
      continue
    if tof_01_08 is None:
      tof_01_08 = columns[3]
      continue
    if tof_09_16 is None:
      tof_09_16 = columns[3]
      continue
    if tof_17_24 is None:
      tof_17_24 = columns[3]
      continue
    if i != 6 and trig_on[i] is None:
      trig_on[i] = columns[1]
      trig_ps[i] = columns[2]
      trig_gate[i] = columns[3]
      continue
    if i != 6 and trig[i] is None:
      trig[i] = columns[0]
      i = i + 1
      continue
    if clock_on is None:
      clock_on = columns[1]
      clock_gate = columns[3]
      continue
    if rsv2_on is None:
      rsv2_on = columns[1]
      rsv2_gate = columns[3]
      continue
    print(line)
  tof_sel = tof_17_24 + tof_09_16 + tof_01_08
  if tof_sel == '!!!!!!!!!!!!!!!!!!!!!!!!':
    tof_sel = 'ALL'
  info = (# param,
          tof_sel,
          trig_on[0], trig_ps[0], trig_gate[0], trig[0],
          trig_on[1], trig_ps[1], trig_gate[1], trig[1],
          trig_on[2], trig_ps[2], trig_gate[2], trig[2],
          trig_on[3], trig_ps[3], trig_gate[3], trig[3],
          trig_on[4], trig_ps[4], trig_gate[4], trig[4],
          trig_on[5], trig_ps[5], trig_gate[5], trig[5],
          # clock_on, clock_gate,
          # rsv2_on, rsv2_gate
          )
  logger.debug(info)
  return info
