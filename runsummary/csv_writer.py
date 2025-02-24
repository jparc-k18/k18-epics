#!/usr/bin/env python3

import csv
import logging
import os

import global_variables as g

logger = logging.getLogger('__main__').getChild(__name__)

#______________________________________________________________________________
def make_title(force=False):
  if os.path.isfile(g.run_summary) and not force:
    with open(g.run_summary, 'r') as f:
      lines = f.readlines()
      for line in lines:
        titles = line.strip().split(',')
        if titles == g.labels:
          return
  logger.info(f'make title : {g.labels}')
  with open(g.run_summary, 'w') as f:
    w = csv.writer(f, delimiter=',')
    w.writerow(g.labels)

#______________________________________________________________________________
def is_listed(run_number):
  if not os.path.isfile(g.run_summary):
    return False
  with open(g.run_summary, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
      if g.labels[0] == row[0]:
        continue
      if run_number == int(row[0]):
        return True
  return False

#______________________________________________________________________________
def write(values):
  with open(g.run_summary, 'a') as f:
    w = csv.writer(f, delimiter=',')
    logger.info(values)
    w.writerow(values)

#______________________________________________________________________________
def make_magnet_param(info, stddev):
  # output_dir = 'magnet'
  output_dir = '/misc/subdata/K18MagnetParam'
  for n, i in info.items():
    with open(os.path.join(output_dir, f'K18MagnetParam_{n:05d}'), 'w') as f:
      w = csv.writer(f, delimiter='\t')
      for k, v in i.items():
        t = k
        t = t.replace('HDPS_', '')
        t = t.replace('HDESS_', '')
        t = t.replace('SETD_MON', 'CSET')
        t = t.replace('_CMON', '')
        t = t.replace('_VMON', '')
        t = t.replace('K18MAG_', '')
        t = t.replace('K18_', '')
        t += ' ' * (20 - len(t))
        # t = t.replace('K18' '')
        values = [t, v, stddev[n][k]]
        # logger.info(values)
        w.writerow(values)
