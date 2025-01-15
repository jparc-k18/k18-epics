#!/usr/bin/env python3

import datetime
import numpy
import time
import logging
import os

import epics
import ROOT

logging.basicConfig(
  # level=logging.DEBUG,
  level=logging.INFO,
  format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

logging_interval = 30
newfile_interval = 14400 # 14400

val_dict = dict()
graph_dict = dict()
tree = ROOT.TTree('epics', 'K1.8 EPICS Data')

#______________________________________________________________________________
def update_connection(pvname=None, conn=None, **kws):
  state = "connect" if conn else "disconnect"
  logger.info(f'{state} {pvname}')

#______________________________________________________________________________
def update_value(pvname=None, value=None, timestamp=None, **kws):
  logger.debug(f'update value {pvname:20} {value}')
  if pvname is None or value is None or timestamp is None:
    return
  if pvname in graph_dict:
    try:
      graph_dict[pvname].AddPoint(timestamp, value)
    except TypeError as e:
      logger.error(e)
      logger.error(f'{timestamp} {pvname} {value}')

#______________________________________________________________________________
def run():
  pv_list = list()
  unix_time = numpy.zeros(1, dtype=float)
  tree.Branch('UnixTime', unix_time, 'UnixTime/D')
  with open('param/channel_list.txt') as f:
    for line in f.readlines():
      vals = line.split()
      if len(vals) == 0 or vals[0] == '#':
        continue
      pvname = vals[0]
      pv = epics.PV(pvname,
                    callback=update_value,
                    connection_callback=update_connection,
                    connection_timeout=0.1)
      pv_list.append(pv)
      branch_name = pvname.replace('::', '_').replace(':', '_')
      g = ROOT.TGraph()
      graph_dict[pvname] = g
      g.SetNameTitle(branch_name, f'{branch_name}; ; {pv.units}')
      g.SetLineColor(ROOT.kBlack)
      g.SetMarkerStyle(8)
      ax = g.GetXaxis()
      ax.SetTimeDisplay(1)
      ax.SetTimeFormat('#splitline{%Y/%m/%d}{  %H:%M:%S}')
      ax.SetLabelOffset(0.04)
      ax.SetNdivisions(-506)
      val_dict[pvname] = numpy.zeros(2, dtype=float)
      tree.Branch(branch_name, val_dict[pvname], f'{branch_name}[2]/D')
      logger.info(f'add {pvname}')
  last = time.time()
  try:
    while True:
      unix_time[0] = time.time()
      for pv in pv_list:
        logger.debug(f'{pv.pvname} {pv.value} {pv.timestamp}')
        try:
          val_dict[pv.pvname][0] = pv.value
        except:
          logger.error(f'{pv.pvname} {pv.value} {pv.timestamp}')
#          val_dict[pv.pvname][0] = numpy.NAN
          val_dict[pv.pvname][0] = numpy.nan
        val_dict[pv.pvname][1] = pv.timestamp
      logger.debug(f'tree.Fill()')
      tree.Fill()
      if unix_time[0] - last > newfile_interval:
        write()
        last = unix_time[0]
      while time.time() - unix_time[0] < logging_interval:
        time.sleep(0.01)
  except KeyboardInterrupt:
    logger.info('detect signal')
    write()

#______________________________________________________________________________
def write():
  now = datetime.datetime.now()
  file_path = f'data/k18epics_{now.strftime("%Y%m%d_%H%M%S")}.root'
  f = ROOT.TFile.Open(file_path, 'recreate')
  for g in graph_dict.values():
    g.Write()
    g.Set(0)
  tree.Write()
  f.Write()
  f.Close()
  tree.Reset()
  logger.info(f'write {file_path}')

#______________________________________________________________________________
if __name__ == '__main__':
  os.environ['EPICS_CA_ADDR_LIST'] = '192.168.30.255 192.153.109.232'
  run()
