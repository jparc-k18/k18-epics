#!/usr/bin/env python3

import ROOT

f = ROOT.TFile('../epics-recorder/k18epics_20230622_102356.root')
t = f.Get('epics')
