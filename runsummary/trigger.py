#!/usr/bin/env python3

import logging
import os

import global_variables as g

logger = logging.getLogger('__main__').getChild(__name__)

NumOfRegion2 = 6
BeamDetectors = ['BH1', 'BH2', 'BAC', 'HTOF', 'Other1', 'SSAND']
ScatDetectors = ['BEAM', 'HTOF-Mp2', 'Other3', 'TOF', 'AC1', 'WC',
                 'M2D1', 'BVH', # 'M2D2',
                 'M3D', 'HTOF-Mp4', 'SSOR']

registers = [
  'RGN1::SEL_TOF',
  'RGN2A::DELAY_BH1_BEAM',
  'RGN2A::DELAY_BH2_BEAM',
  'RGN2A::DELAY_BAC_BEAM',
  'RGN2A::DELAY_HTOF_BEAM',
  'RGN2A::DELAY_OTHER1_BEAM',
  'RGN2A::DELAY_OTHER2_BEAM',
  'RGN2A::WIDTH_BH1_BEAM',
  'RGN2A::WIDTH_BH2_BEAM',
  'RGN2A::WIDTH_BAC_BEAM',
  'RGN2A::WIDTH_HTOF_BEAM',
  'RGN2A::WIDTH_OTHER1_BEAM',
  'RGN2A::WIDTH_OTHER2_BEAM',
  'RGN2A::BPS_CTRL_BEAM',
  'RGN2A::BPS_COIN_BEAM',
  'RGN2A::DELAY_BEAM_SCAT',
  'RGN2A::DELAY_PVAC_SCAT',
  'RGN2A::DELAY_FAC_SCAT',
  'RGN2A::DELAY_TOF_SCAT',
  'RGN2A::DELAY_LAC_SCAT',
  'RGN2A::DELAY_WC_SCAT',
  'RGN2A::DELAY_M2D1_SCAT',
  'RGN2A::DELAY_M2D2_SCAT',
  'RGN2A::DELAY_M3D_SCAT',
  'RGN2A::DELAY_OTHER3_SCAT',
  'RGN2A::DELAY_OTHER4_SCAT',
  'RGN2A::WIDTH_BEAM_SCAT',
  'RGN2A::WIDTH_PVAC_SCAT',
  'RGN2A::WIDTH_FAC_SCAT',
  'RGN2A::WIDTH_TOF_SCAT',
  'RGN2A::WIDTH_LAC_SCAT',
  'RGN2A::WIDTH_WC_SCAT',
  'RGN2A::WIDTH_M2D1_SCAT',
  'RGN2A::WIDTH_M2D2_SCAT',
  'RGN2A::WIDTH_M3D_SCAT',
  'RGN2A::WIDTH_OTHER3_SCAT',
  'RGN2A::WIDTH_OTHER4_SCAT',
  'RGN2A::BPS_CTRL_SCAT',
  'RGN2A::BPS_COIN_SCAT',
  'RGN2B::DELAY_BH1_BEAM',
  'RGN2B::DELAY_BH2_BEAM',
  'RGN2B::DELAY_BAC_BEAM',
  'RGN2B::DELAY_HTOF_BEAM',
  'RGN2B::DELAY_OTHER1_BEAM',
  'RGN2B::DELAY_OTHER2_BEAM',
  'RGN2B::WIDTH_BH1_BEAM',
  'RGN2B::WIDTH_BH2_BEAM',
  'RGN2B::WIDTH_BAC_BEAM',
  'RGN2B::WIDTH_HTOF_BEAM',
  'RGN2B::WIDTH_OTHER1_BEAM',
  'RGN2B::WIDTH_OTHER2_BEAM',
  'RGN2B::BPS_CTRL_BEAM',
  'RGN2B::BPS_COIN_BEAM',
  'RGN2B::DELAY_BEAM_SCAT',
  'RGN2B::DELAY_PVAC_SCAT',
  'RGN2B::DELAY_FAC_SCAT',
  'RGN2B::DELAY_TOF_SCAT',
  'RGN2B::DELAY_LAC_SCAT',
  'RGN2B::DELAY_WC_SCAT',
  'RGN2B::DELAY_M2D1_SCAT',
  'RGN2B::DELAY_M2D2_SCAT',
  'RGN2B::DELAY_M3D_SCAT',
  'RGN2B::DELAY_OTHER3_SCAT',
  'RGN2B::DELAY_OTHER4_SCAT',
  'RGN2B::WIDTH_BEAM_SCAT',
  'RGN2B::WIDTH_PVAC_SCAT',
  'RGN2B::WIDTH_FAC_SCAT',
  'RGN2B::WIDTH_TOF_SCAT',
  'RGN2B::WIDTH_LAC_SCAT',
  'RGN2B::WIDTH_WC_SCAT',
  'RGN2B::WIDTH_M2D1_SCAT',
  'RGN2B::WIDTH_M2D2_SCAT',
  'RGN2B::WIDTH_M3D_SCAT',
  'RGN2B::WIDTH_OTHER3_SCAT',
  'RGN2B::WIDTH_OTHER4_SCAT',
  'RGN2B::BPS_CTRL_SCAT',
  'RGN2B::BPS_COIN_SCAT',
  'RGN2C::DELAY_BH1_BEAM',
  'RGN2C::DELAY_BH2_BEAM',
  'RGN2C::DELAY_BAC_BEAM',
  'RGN2C::DELAY_HTOF_BEAM',
  'RGN2C::DELAY_OTHER1_BEAM',
  'RGN2C::DELAY_OTHER2_BEAM',
  'RGN2C::WIDTH_BH1_BEAM',
  'RGN2C::WIDTH_BH2_BEAM',
  'RGN2C::WIDTH_BAC_BEAM',
  'RGN2C::WIDTH_HTOF_BEAM',
  'RGN2C::WIDTH_OTHER1_BEAM',
  'RGN2C::WIDTH_OTHER2_BEAM',
  'RGN2C::BPS_CTRL_BEAM',
  'RGN2C::BPS_COIN_BEAM',
  'RGN2C::DELAY_BEAM_SCAT',
  'RGN2C::DELAY_PVAC_SCAT',
  'RGN2C::DELAY_FAC_SCAT',
  'RGN2C::DELAY_TOF_SCAT',
  'RGN2C::DELAY_LAC_SCAT',
  'RGN2C::DELAY_WC_SCAT',
  'RGN2C::DELAY_M2D1_SCAT',
  'RGN2C::DELAY_M2D2_SCAT',
  'RGN2C::DELAY_M3D_SCAT',
  'RGN2C::DELAY_OTHER3_SCAT',
  'RGN2C::DELAY_OTHER4_SCAT',
  'RGN2C::WIDTH_BEAM_SCAT',
  'RGN2C::WIDTH_PVAC_SCAT',
  'RGN2C::WIDTH_FAC_SCAT',
  'RGN2C::WIDTH_TOF_SCAT',
  'RGN2C::WIDTH_LAC_SCAT',
  'RGN2C::WIDTH_WC_SCAT',
  'RGN2C::WIDTH_M2D1_SCAT',
  'RGN2C::WIDTH_M2D2_SCAT',
  'RGN2C::WIDTH_M3D_SCAT',
  'RGN2C::WIDTH_OTHER3_SCAT',
  'RGN2C::WIDTH_OTHER4_SCAT',
  'RGN2C::BPS_CTRL_SCAT',
  'RGN2C::BPS_COIN_SCAT',
  'RGN2D::DELAY_BH1_BEAM',
  'RGN2D::DELAY_BH2_BEAM',
  'RGN2D::DELAY_BAC_BEAM',
  'RGN2D::DELAY_HTOF_BEAM',
  'RGN2D::DELAY_OTHER1_BEAM',
  'RGN2D::DELAY_OTHER2_BEAM',
  'RGN2D::WIDTH_BH1_BEAM',
  'RGN2D::WIDTH_BH2_BEAM',
  'RGN2D::WIDTH_BAC_BEAM',
  'RGN2D::WIDTH_HTOF_BEAM',
  'RGN2D::WIDTH_OTHER1_BEAM',
  'RGN2D::WIDTH_OTHER2_BEAM',
  'RGN2D::BPS_CTRL_BEAM',
  'RGN2D::BPS_COIN_BEAM',
  'RGN2D::DELAY_BEAM_SCAT',
  'RGN2D::DELAY_PVAC_SCAT',
  'RGN2D::DELAY_FAC_SCAT',
  'RGN2D::DELAY_TOF_SCAT',
  'RGN2D::DELAY_LAC_SCAT',
  'RGN2D::DELAY_WC_SCAT',
  'RGN2D::DELAY_M2D1_SCAT',
  'RGN2D::DELAY_M2D2_SCAT',
  'RGN2D::DELAY_M3D_SCAT',
  'RGN2D::DELAY_OTHER3_SCAT',
  'RGN2D::DELAY_OTHER4_SCAT',
  'RGN2D::WIDTH_BEAM_SCAT',
  'RGN2D::WIDTH_PVAC_SCAT',
  'RGN2D::WIDTH_FAC_SCAT',
  'RGN2D::WIDTH_TOF_SCAT',
  'RGN2D::WIDTH_LAC_SCAT',
  'RGN2D::WIDTH_WC_SCAT',
  'RGN2D::WIDTH_M2D1_SCAT',
  'RGN2D::WIDTH_M2D2_SCAT',
  'RGN2D::WIDTH_M3D_SCAT',
  'RGN2D::WIDTH_OTHER3_SCAT',
  'RGN2D::WIDTH_OTHER4_SCAT',
  'RGN2D::BPS_CTRL_SCAT',
  'RGN2D::BPS_COIN_SCAT',
  'RGN2E::DELAY_BH1_BEAM',
  'RGN2E::DELAY_BH2_BEAM',
  'RGN2E::DELAY_BAC_BEAM',
  'RGN2E::DELAY_HTOF_BEAM',
  'RGN2E::DELAY_OTHER1_BEAM',
  'RGN2E::DELAY_OTHER2_BEAM',
  'RGN2E::WIDTH_BH1_BEAM',
  'RGN2E::WIDTH_BH2_BEAM',
  'RGN2E::WIDTH_BAC_BEAM',
  'RGN2E::WIDTH_HTOF_BEAM',
  'RGN2E::WIDTH_OTHER1_BEAM',
  'RGN2E::WIDTH_OTHER2_BEAM',
  'RGN2E::BPS_CTRL_BEAM',
  'RGN2E::BPS_COIN_BEAM',
  'RGN2E::DELAY_BEAM_SCAT',
  'RGN2E::DELAY_PVAC_SCAT',
  'RGN2E::DELAY_FAC_SCAT',
  'RGN2E::DELAY_TOF_SCAT',
  'RGN2E::DELAY_LAC_SCAT',
  'RGN2E::DELAY_WC_SCAT',
  'RGN2E::DELAY_M2D1_SCAT',
  'RGN2E::DELAY_M2D2_SCAT',
  'RGN2E::DELAY_M3D_SCAT',
  'RGN2E::DELAY_OTHER3_SCAT',
  'RGN2E::DELAY_OTHER4_SCAT',
  'RGN2E::WIDTH_BEAM_SCAT',
  'RGN2E::WIDTH_PVAC_SCAT',
  'RGN2E::WIDTH_FAC_SCAT',
  'RGN2E::WIDTH_TOF_SCAT',
  'RGN2E::WIDTH_LAC_SCAT',
  'RGN2E::WIDTH_WC_SCAT',
  'RGN2E::WIDTH_M2D1_SCAT',
  'RGN2E::WIDTH_M2D2_SCAT',
  'RGN2E::WIDTH_M3D_SCAT',
  'RGN2E::WIDTH_OTHER3_SCAT',
  'RGN2E::WIDTH_OTHER4_SCAT',
  'RGN2E::BPS_CTRL_SCAT',
  'RGN2E::BPS_COIN_SCAT',
  'RGN2F::DELAY_BH1_BEAM',
  'RGN2F::DELAY_BH2_BEAM',
  'RGN2F::DELAY_BAC_BEAM',
  'RGN2F::DELAY_HTOF_BEAM',
  'RGN2F::DELAY_OTHER1_BEAM',
  'RGN2F::DELAY_OTHER2_BEAM',
  'RGN2F::WIDTH_BH1_BEAM',
  'RGN2F::WIDTH_BH2_BEAM',
  'RGN2F::WIDTH_BAC_BEAM',
  'RGN2F::WIDTH_HTOF_BEAM',
  'RGN2F::WIDTH_OTHER1_BEAM',
  'RGN2F::WIDTH_OTHER2_BEAM',
  'RGN2F::BPS_CTRL_BEAM',
  'RGN2F::BPS_COIN_BEAM',
  'RGN2F::DELAY_BEAM_SCAT',
  'RGN2F::DELAY_PVAC_SCAT',
  'RGN2F::DELAY_FAC_SCAT',
  'RGN2F::DELAY_TOF_SCAT',
  'RGN2F::DELAY_LAC_SCAT',
  'RGN2F::DELAY_WC_SCAT',
  'RGN2F::DELAY_M2D1_SCAT',
  'RGN2F::DELAY_M2D2_SCAT',
  'RGN2F::DELAY_M3D_SCAT',
  'RGN2F::DELAY_OTHER3_SCAT',
  'RGN2F::DELAY_OTHER4_SCAT',
  'RGN2F::WIDTH_BEAM_SCAT',
  'RGN2F::WIDTH_PVAC_SCAT',
  'RGN2F::WIDTH_FAC_SCAT',
  'RGN2F::WIDTH_TOF_SCAT',
  'RGN2F::WIDTH_LAC_SCAT',
  'RGN2F::WIDTH_WC_SCAT',
  'RGN2F::WIDTH_M2D1_SCAT',
  'RGN2F::WIDTH_M2D2_SCAT',
  'RGN2F::WIDTH_M3D_SCAT',
  'RGN2F::WIDTH_OTHER3_SCAT',
  'RGN2F::WIDTH_OTHER4_SCAT',
  'RGN2F::BPS_CTRL_SCAT',
  'RGN2F::BPS_COIN_SCAT',
  'RGN3::PS_R2A',
  'RGN3::GATE_R2A',
  'RGN3::PS_R2B',
  'RGN3::GATE_R2B',
  'RGN3::PS_R2C',
  'RGN3::GATE_R2C',
  'RGN3::PS_R2D',
  'RGN3::GATE_R2D',
  'RGN3::PS_R2E',
  'RGN3::GATE_R2E',
  'RGN3::PS_R2F',
  'RGN3::GATE_R2F',
  'RGN3::SEL_PSOR',
  'RGN3::RST_PSCNT',
  'RGN4::SEL_EXTCLK',
  'RGN4::SEL_RSV2',
  'RGN4::SEL_CLK10M',
  'RGN4::SEL_CLK1M',
  'RGN4::SEL_CLK100k',
  'RGN4::SEL_CLK10k',
  'RGN4::SEL_CLK1k',
  'RGN4::GATE',
]

#______________________________________________________________________________
def beam_bps(ctrl, coin):
  buf = ''
  for i, d in enumerate(BeamDetectors):
    b = bps((ctrl>>(len(BeamDetectors)-1-i))&1,
            (coin>>(len(BeamDetectors)-1-i))&1)
    if 'OFF' in b:
      continue
    elif 'VETO' in b:
      buf += '/'
    buf += d + 'x'
  if buf[-1:] == 'x':
    buf = buf[:-1]
  if len(buf) == 0:
    buf = 'n/a'
  return buf

#______________________________________________________________________________
def bps(ctrl, coin):
  if ctrl == 0:
    return 'OFF'
  if coin == 0:
    return 'VETO'
  return 'ON'

#______________________________________________________________________________
def gate(val):
  if val == 1:
    return 'ON'
  elif val == 2:
    return 'OFF'
  elif val == 3:
    return 'ON/OFF'
  else:
    return '-'

#______________________________________________________________________________
def onoff(val, char=False):
  if val == 0:
    return '.' if char else 'OFF'
  elif val == 1:
    return '!' if char else 'ON'
  else:
    return str()

#______________________________________________________________________________
def parse(trigger_info):
  ret = dict()
  keys = ['HULTRG_' + r.replace('::', '_') for r in registers]
  ret['TOFSelector'] = str()
  ''' Region1 '''
  if trigger_info['HULTRG_RGN1_SEL_TOF'] == 2**24-1:
    ret['TOFSelector'] = 'ALL'
  else:
    for i in range(24):
      ret['TOFSelector'] += onoff(
        (trigger_info['HULTRG_RGN1_SEL_TOF'] >> i) & 1, True)
  ''' Region3 '''
  sel_psor = trigger_info['HULTRG_RGN3_SEL_PSOR']
  for i in range(6):
    sel = onoff((sel_psor >> i) & 1)
    ps = (trigger_info[f'HULTRG_RGN3_PS_R2{chr(65+i)}'] + 1
          if 'ON' in sel else '-')
    g = (gate(trigger_info[f'HULTRG_RGN3_GATE_R2{chr(65+i)}'])
         if 'ON' in sel else '-')
    # ret[f'Trig{chr(65+i)}-ON'] = sel
    ''' Region2 '''
    ctrl = trigger_info[f'HULTRG_RGN2{chr(65+i)}_BPS_CTRL_BEAM']
    coin = trigger_info[f'HULTRG_RGN2{chr(65+i)}_BPS_COIN_BEAM']
    beam = beam_bps(ctrl, coin)
    ctrl = trigger_info[f'HULTRG_RGN2{chr(65+i)}_BPS_CTRL_SCAT']
    coin = trigger_info[f'HULTRG_RGN2{chr(65+i)}_BPS_COIN_SCAT']
    scat = scat_bps(ctrl, coin, beam)
    ret[f'Trig{chr(65+i)}'] = scat
    ret[f'Trig{chr(65+i)}-PS'] = ps
    ret[f'Trig{chr(65+i)}-Gate'] = g
  logger.debug(ret)
  return ret.values()

#______________________________________________________________________________
def scat_bps(ctrl, coin, beam):
  buf = ''
  for i, d in enumerate(ScatDetectors):
    b = bps((ctrl>>(len(ScatDetectors)-1-i))&1,
            (coin>>(len(ScatDetectors)-1-i))&1)
    if 'OFF' in b:
      continue
    elif 'VETO' in b:
      buf += '/'
    if i == 0:
      buf += beam + 'x'
    else:
      buf += d + 'x'
  if buf[-1:] == 'x':
    buf = buf[:-1]
  if len(buf) == 0:
    buf = 'n/a'
  return buf
