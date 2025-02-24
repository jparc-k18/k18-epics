#!/usr/bin/env python3

import array
import datetime
# import epics
import logging
import numpy
import os
import ROOT

import global_variables as g
import csv_writer
import trigger

logger = logging.getLogger('__main__').getChild(__name__)

comment_info = None
epics_dir = os.path.join(g.subdata_path, 'epics-recorder')
epics_dict = dict()
trigger_dict = dict()

channel_list = [
  # 'HDSYS_MR_POWER',
  # 'HDMON_SYIM_POWER',
  'MRMON_DCCT_073_1_VAL_MRPWR',
  'MRSLW_SXOPR_D2_VAL_DUTY',
  'HDPS_AK18D1_CSET',
  'HDPS_K18D4_CSET',
  'HDPS_K18D4S_CSET',
  'HDPS_S2SQ1_CSET',
  'HDPS_S2SQ2_CSET',
  'HDPS_S2SD1_CSET',
  'HDPS_BSM1_CSET',
  'HDESS_K18_ESS1_NEG_VSET',
  'HDESS_K18_ESS1_POS_VSET',
  'HDESS_K18_ESS2_NEG_VSET',
  'HDESS_K18_ESS2_POS_VSET',
  'K18MAG_D4_FLD',
  'K18MAG_S2SD1_FLD',
]

#______________________________________________________________________________
# def caget(pvname):
#   return epics.caget(pvname)

#______________________________________________________________________________
def calculate_mean(info):
  stddev = dict()
  for n, i in info.items():
    stddev[n] = dict()
    for k, d in i.items():
      if len(d) == 0:
        d = 0.
        s = 0.
      else:
        s = numpy.std(d)
        d = numpy.mean(d)
      i[k] = d
      stddev[n][k] = s
  return info, stddev

#______________________________________________________________________________
def null_dict():
  info = dict()
  info['BeamMom'] = list()
  for c in channel_list:
    info[c] = list()
  # for r in trigger.registers:
  #   c = 'HULTRG_' + r.replace('::', '_')
  #   info[c] = list()
  return info

#______________________________________________________________________________
def epics_info(run_number):
  if run_number in epics_dict:
    return epics_dict[run_number].values()
  else:
    ret = null_dict()
    for k, v in ret.items():
      ret[k] = None
    return ret.values()

#______________________________________________________________________________
def make_magnet_param():
  global epics_dict
  epics_dict = dict()
  magnet_list = [
    'PK18',
    'K18MAG_D4_FLD',
    'K18MAG_S2SD1_FLD',

    # 'HDPS_AK18D1_CSET',
    # 'HDPS_AK11D1_CSET',
    # 'HDPS_BSM1_CSET',
    # 'HDPS_K18Q1_SETD_MON',
    # 'HDPS_K18Q2_SETD_MON',
    # 'HDPS_K18D2_SETD_MON',
    # 'HDPS_K18Q3_SETD_MON',
    # 'HDPS_K18O1_SETD_MON',
    # 'HDPS_K18Q4_SETD_MON',
    # 'HDPS_K18S1_SETD_MON',
    # 'HDPS_K18CM1_SETD_MON',
    # 'HDESS_K18_ESS1_NEG_VSET',
    # 'HDESS_K18_ESS1_POS_VSET',
    # 'HDPS_K18CM2_SETD_MON',
    # 'HDPS_K18S2_SETD_MON',
    # 'HDPS_K18Q5_SETD_MON',
    # 'HDPS_K18Q6_SETD_MON',
    # 'HDPS_K18D3_SETD_MON',
    # 'HDPS_K18Q7_SETD_MON',
    # 'HDPS_K18O2_SETD_MON',
    # 'HDPS_K18S3_SETD_MON',
    # 'HDPS_K18CM3_SETD_MON',
    # 'HDESS_K18_ESS2_NEG_VSET',
    # 'HDESS_K18_ESS2_POS_VSET',
    # 'HDPS_K18CM4_SETD_MON',
    # 'HDPS_K18S4_SETD_MON',
    # 'HDPS_K18Q8_SETD_MON',
    # 'HDPS_K18O3_SETD_MON',
    # 'HDPS_K18Q9_SETD_MON',
    # 'HDPS_K18Q10_SETD_MON',
    # 'HDPS_K18Q11_SETD_MON',
    # 'HDPS_K18D4_SETD_MON',
    # 'HDPS_K18D4S_SETD_MON',
    # 'HDPS_K18Q12_SETD_MON',
    # 'HDPS_K18Q13_SETD_MON',
    # 'HDPS_S2SQ1_CSET',
    # 'HDPS_S2SQ2_CSET',
    # 'HDPS_S2SD1_CSET',

    'HDPS_AK18D1_CMON',
    'HDPS_AK11D1_CMON',
    'HDPS_BSM1_CMON',
    'HDPS_K18Q1_CMON',
    'HDPS_K18Q2_CMON',
    'HDPS_K18D2_CMON',
    'HDPS_K18Q3_CMON',
    'HDPS_K18O1_CMON',
    'HDPS_K18Q4_CMON',
    'HDPS_K18S1_CMON',
    'HDPS_K18CM1_CMON',
    'HDESS_K18_ESS1_NEG_VMON',
    'HDESS_K18_ESS1_POS_VMON',
    'HDPS_K18CM2_CMON',
    'HDPS_K18S2_CMON',
    'HDPS_K18Q5_CMON',
    'HDPS_K18Q6_CMON',
    'HDPS_K18D3_CMON',
    'HDPS_K18Q7_CMON',
    'HDPS_K18O2_CMON',
    'HDPS_K18S3_CMON',
    'HDPS_K18CM3_CMON',
    'HDESS_K18_ESS2_NEG_VMON',
    'HDESS_K18_ESS2_POS_VMON',
    'HDPS_K18CM4_CMON',
    'HDPS_K18S4_CMON',
    'HDPS_K18Q8_CMON',
    'HDPS_K18O3_CMON',
    'HDPS_K18Q9_CMON',
    'HDPS_K18Q10_CMON',
    'HDPS_K18Q11_CMON',
    'HDPS_K18D4_CMON',
    'HDPS_K18D4S_CMON',
    'HDPS_K18Q12_CMON',
    'HDPS_K18Q13_CMON',
    'HDPS_S2SQ1_CMON',
    'HDPS_S2SQ2_CMON',
    'HDPS_S2SD1_CMON',
  ]
  for r in sorted(os.listdir(epics_dir)):
    r = os.path.join(epics_dir, r)
    if '.root' not in r:
      continue
    stop_dt = datetime.datetime.strptime(
      os.path.basename(r), 'k18epics_%Y%m%d_%H%M%S.root')
    if stop_dt < datetime.datetime(2025, 1, 1):
      continue
    f = ROOT.TFile(r)
    t = f.Get('epics')
    logger.debug(f'{r}')
    try:
      t.SetBranchStatus('*', 0)
      t.SetBranchStatus('UnixTime', 1)
      event = dict()
      for c in magnet_list:
        if c in t.GetListOfBranches():
          t.SetBranchStatus(c, 1)
          event[c] = numpy.ndarray(2, dtype='float64')
          t.SetBranchAddress(c, event[c])
      for i in range(t.GetEntriesFast()):
        t.GetEntry(i)
        dt = datetime.datetime.fromtimestamp(t.UnixTime)
        for n, v in comment_info.items():
          if ('StartTime' in v and 'StopTime' in v and
              dt >= v['StartTime'] and dt <= v['StopTime']):
            break
          n = None
        if n is None:
          continue
        if n not in epics_dict:
          epics_dict[n] = dict()
          for c in magnet_list:
            epics_dict[n][c] = list()
        for k, v in event.items():
          if k == 'K18MAG_S2SD1_FLD' and v[0] == 0:
            pass
          else:
            epics_dict[n][k].append(v[0])
            if k == 'K18MAG_D4_FLD':
              mom = v[0]*0.299792*4.
              epics_dict[n]['PK18'].append(mom)
        # logger.info(event)
        # logger.info(epics_dict[n])
        # logger.info(f'{n} {dt} {t.UnixTime} {subinfo}')
    except:
      pass
  i, s = calculate_mean(epics_dict)
  # logger.info(i)
  # logger.info(s)
  # logger.debug(epics_dict)
  # logger.debug(trigger_dict)
  csv_writer.make_magnet_param(i, s)

#______________________________________________________________________________
def read_all():
  global epics_dict
  global trigger_dict
  trigger_dict = dict()
  epics_dict = dict()
  for r in sorted(os.listdir(epics_dir)):
    r = os.path.join(epics_dir, r)
    stop_dt = datetime.datetime.strptime(
      os.path.basename(r), 'k18epics_%Y%m%d_%H%M%S.root')
    if stop_dt < datetime.datetime(2025, 1, 1):
      continue
    logger.debug(stop_dt)
    if '.root' not in r:
      continue
    f = ROOT.TFile(r)
    t = f.Get('epics')
    logger.debug(f'{r}')
    try:
      t.SetBranchStatus('*', 0)
      t.SetBranchStatus('UnixTime', 1)
      event = dict()
      for c in channel_list:
        if c in t.GetListOfBranches():
          t.SetBranchStatus(c, 1)
          event[c] = numpy.ndarray(2, dtype='float64')
          t.SetBranchAddress(c, event[c])
      for r in trigger.registers:
        c = 'HULTRG_' + r.replace('::', '_')
        if c in t.GetListOfBranches():
          t.SetBranchStatus(c, 1)
          event[c] = numpy.ndarray(2, dtype='float64')
          t.SetBranchAddress(c, event[c])
      # for b in t.GetListOfBranches():
      #   logger.info(f'{os.path.basename(r)} {b}')
      for i in range(t.GetEntriesFast()):
        t.GetEntry(i)
        dt = datetime.datetime.fromtimestamp(t.UnixTime)
        for n, v in comment_info.items():
          if ('StartTime' in v and 'StopTime' in v and
              dt >= v['StartTime'] and dt <= v['StopTime']):
            break
          n = None
        if n is None:
          continue
        if (v['StopTime'] - dt).total_seconds() <= 60:
          continue
        # if (ROOT.TMath.IsNaN(t.HDDAQ_RUN_NUMBER[0]) or
        #     t.HDDAQ_RUN_NUMBER[0] < 70000):
        #   continue
        # if t.HDDAQ_RUN_NUMBER[0] not in epics_dict:
        #   epics_dict[t.HDDAQ_RUN_NUMBER[0]] = null_dict()
        # subinfo = epics_dict[t.HDDAQ_RUN_NUMBER[0]]
        if n not in epics_dict:
          epics_dict[n] = null_dict()
        if n not in trigger_dict:
          trigger_dict[n] = dict()
        for k, v in event.items():
          if 'HULTRG' in k:
            # if k in trigger_dict[n]:
            # if n == 72584 and ('RGN3' in k or 'RGN4' in k):
            #   logger.info(f'{dt} {n} {k} = {v[0]}?')
            trigger_dict[n][k] = int(v[0])
          elif k == 'K18MAG_S2SD1_FLD' and v[0] == 0:
            pass
          else:
            epics_dict[n][k].append(v[0])
            if k == 'K18MAG_D4_FLD':
              mom = v[0]*0.299792*4.
              epics_dict[n]['BeamMom'].append(mom)
        # logger.info(event)
        # logger.info(epics_dict[n])
        # logger.info(f'{n} {dt} {t.UnixTime} {subinfo}')
    except AttributeError as e:
      logger.debug(f'{e}')
  calculate_mean(epics_dict)
  logger.debug(epics_dict)
  logger.debug(trigger_dict)

#______________________________________________________________________________
def set_comment_info(comment):
  global comment_info
  comment_info = dict()
  for n, v in comment.items():
    comment_info[n] = dict()
    for tag in ['StartTime', 'StopTime']:
      if tag in v:
        comment_info[n][tag] = datetime.datetime.strptime(v[tag], '%Y/%m/%d %H:%M:%S')
  logger.debug(comment_info)

#______________________________________________________________________________
def trigger_info(run_number):
  if run_number in trigger_dict:
    return trigger.parse(trigger_dict[run_number])
  else:
    return dict()

#______________________________________________________________________________
if __name__ == '__main__':
  import logging.config
  import yaml
  top_dir = os.path.dirname(os.path.abspath(__file__))
  log_conf = os.path.join(top_dir, 'logging_config.yml')
  # make_magnet_param()
  # with open(log_conf, 'r') as f:
  #   logging.config.dictConfig(yaml.safe_load(f))
  # for r in sorted(os.listdir(epics_dir)):
  #   r = os.path.join(epics_dir, r)
  #   if '.root' not in r:
  #     continue
  #   i = null_dict()
  #   f = ROOT.TFile(r)
  #   t = f.Get('epics')
  #   for b in t.GetListOfBranches():
  #     logger.info(f'{os.path.basename(r)} {b}')
  #     b.Print()
  #   logger.info('UnixTime' in t.GetListOfBranches())
  #   try:
  #     for iev in range(t.GetEntriesFast()):
  #       t.GetEntry(iev)
  #       # logger.info(t.HDDAQ_RUN_NUMBER[0])
  #       # i['HDDAQ_RUN_NUMBER'].append(t.HDDAQ_RUN_NUMBER[0])
  #       # i['K18MAG_D4_FLD'].append(t.K18MAG_D4_FLD[0])
  #       # if t.K18MAG_S2SD1_FLD[0] > 0.5:
  #       #   i['K18MAG_S2SD1_FLD'].append(t.K18MAG_S2SD1_FLD[0])
  #   except AttributeError as e:
  #     logger.error(e)
  #   except TypeError as e:
  #     logger.error(e)
  #   except KeyError as e:
  #     logger.error(e)
  #   logger.info(f'{r} {i}')
