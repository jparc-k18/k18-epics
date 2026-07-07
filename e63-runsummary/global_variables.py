#!/usr/bin/env python3

import os

# data_path = '/group/had/sks/E70/JPARC2023May/e70_2023may'
# subdata_path = '/group/had/sks/E70/JPARC2023May/subdata'

# data_path = '/misc/raid/e70_2024may'
# subdata_path = '/misc/hdd4/old/E70SubData2023May'

# data_path = '/misc/raid/e70_2025jan'
# subdata_path = '/misc/subdata'

# data_path = '/misc/raid/e70_2025apr'
# subdata_path = '/misc/subdata'

# data_path = '/misc/raid/e63_2025nov'
# subdata_path = '/misc/subdata'

data_path = '/misc/raid/e63_2026apr'
subdata_path = '/misc/subdata'

#run_summary = 'tmp.csv'
run_summary = os.path.join(subdata_path, 'E63RunSummary2026Apr.csv')

labels = [
  'RunNumber',
  'StartTime',
  'StopTime',
  'RunTime',
  'RunTitle',
  'EventNumber',
  'Recorder',
  'Bytes',
  # 'TrigParam',
  'Beam/Spill',
  'K-Beam/Spill',
  'Pi-Beam/Spill',
  'Beam',
  'K-Beam',
  'Pi-Beam',
  'SpillNumber',
  'DAQ-Eff',
  'BeamxDAQEff',
  'DAQ-Duty',
  'BeamMom',
  'MR-Power',
  'SX-Duty',
  'K1.8D1',
  'K1.8D4',
  'K1.8D4s',
  'S2SQ1',
  'S2SQ2',
  'S2SD1',
  'BLineSM1',
  'ESS1_POS',
  'ESS1_NEG',
  'ESS2_POS',
  'ESS2_NEG',
  'K18D4_Field',
  'S2SD1_Field',
  'TOFSelector',
  # 'TrigA-ON',
  'TrigA',
  'TrigA-PS',
  'TrigA-Gate',
  # 'TrigB-ON',
  'TrigB',
  'TrigB-PS',
  'TrigB-Gate',
  # 'TrigC-ON',
  'TrigC',
  'TrigC-PS',
  'TrigC-Gate',
  # 'TrigD-ON',
  'TrigD',
  'TrigD-PS',
  'TrigD-Gate',
  # 'TrigE-ON',
  'TrigE',
  'TrigE-PS',
  'TrigE-Gate',
  # 'TrigF-ON',
  'TrigF',
  'TrigF-PS',
  'TrigF-Gate',
]
