#!/usr/bin/env python
import sys
from math import pow
from pprint import pprint
import string
import time
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import *
from collections import namedtuple

class col:
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    endc = '\033[0m'
    bold = '\033[1m'
    uline = '\033[4m'

def preq(r):
  tot = r['total_events'] 
  cmpl = r['completed_events'] 
  pct_done = float(cmpl)/float(tot)*100. 
  cols = '{:<35}'.format(r['prepid'])
  cols += '{:<12}'.format(r['status'])
  cols += '{:<100}'.format(r['dataset_name'])
  cols += '{:<10.1f}'.format(pct_done)
  cols += '{:<12,}'.format(r['completed_events'])
  cols += '{:<12,}'.format(r['total_events'])
  cols += '{:<12,}'.format(r['priority'])  
  print cols

def fneg(sample):
  if "ttHJetTobb_M125_13TeV_amcatnloFXFX" in sample:  frac = 0.3515
  elif "TTZToQQ" in sample:                             frac = 0.2657
  elif "TTZToLLNuNu_M-10" in sample:                    frac = 0.2676
  elif "TTWJetsToQQ" in sample:                         frac = 0.2412
  elif "TTWJetsToLNu" in sample:                        frac = 0.2433
  elif "TTG" in sample:                                 frac = 0.342
  elif "TTTT_TuneCUETP8M1_13TeV-amcatnlo" in sample:    frac = 0.41
  elif "VVTo2L2Nu_13TeV_amcatnloFXFX" in sample:        frac = 0.20
  elif "WZTo1L3Nu_13TeV_amcatnloFXFX" in sample:        frac = 0.222
  elif "VHToNonbb_M125_13TeV_amcatnloFXFX" in sample:   frac = 0.269
  elif "WWTo1L1Nu2Q_13TeV_amcatnloFXFX" in sample:      frac = 0.192
  elif "WZZ_TuneCUETP8M1_13TeV-amcatnlo" in sample:     frac = 0.0614
  elif "ZZZ_TuneCUETP8M1_13TeV-amcatnlo" in sample:     frac = 0.0726
  elif "WWZ_TuneCUETP8M1_13TeV-amcatnlo" in sample:     frac = 0.0579
  else: frac = 0.
  return frac

def xsec(sample):
  if "SMS-T1tttt_mGluino-1200_mLSP-800" in sample: xs = 0.0856418
  elif "SMS-T1tttt_mGluino-1500_mLSP-100" in sample: xs = 0.0141903
  elif "SMS-T1bbbb_mGluino-1500_mLSP-100" in sample: xs = 0.0141903
  elif "SMS-T1bbbb_mGluino-1000_mLSP-900" in sample: xs = 0.325388
  elif "SMS-T1qqqq_mGluino-1400_mLSP-100" in sample: xs = 0.0252977
  elif "SMS-T1qqqq_mGluino-1000_mLSP-800" in sample: xs = 0.325388
  elif "SMS-T1qqqq_mGluino-1000_mLSP-800" in sample: xs = 0.325388

  elif "SMS-T2tt_mStop-500_mLSP-325" in sample: xs = 0.51848
  elif "SMS-T2tt_mStop-850_mLSP-100" in sample: xs = 0.0189612
  elif "SMS-T2tt_mStop-425_mLSP-325" in sample: xs = 1.31169

  elif ("TTJets_Tune" in sample) or ("TT_" in sample) or ('TTJets_13TeV-amcatnloFXFX-pythia8' in sample):  xs = 815.96
  elif "TTJets_DiLept" in sample: xs = 85.66
  elif "TTJets_SingleLept" in sample: xs = 178.7

  elif "TTJets_HT-2500toInf" in sample: xs = 0.0023234211
  elif "TTJets_HT-1200to2500" in sample: xs = 0.194972521
  elif "TTJets_HT-800to1200" in sample: xs = 1.07722318
  elif "TTJets_HT-600to800" in sample: xs = 2.61537118

  elif "TTZToQQ" in sample:                xs = 0.5297
  elif "TTZToLLNuNu_M-10" in sample:       xs = 0.2529
  elif "TTWJetsToQQ" in sample:            xs = 0.4062
  elif "TTWJetsToLNu" in sample:           xs = 0.2043   
  elif "TTG" in sample: xs = 3.697                
  elif "TTTT_TuneCUETP8M1_13TeV-amcatnlo" in sample: xs = 0.009103
  elif "WJetsToQQ_HT-600ToInf" in sample: xs = 95.14
  elif "ZJetsToQQ_HT600toInf" in sample: xs = 5.67
  
  elif "WJetsToLNu_HT-100To200" in sample:  xs = 1347.*1.21
  elif "WJetsToLNu_HT-200To400" in sample:  xs = 360.*1.21
  elif "WJetsToLNu_HT-400To600" in sample:  xs = 48.98*1.21
  elif "WJetsToLNu_HT-600ToInf" in sample:  xs = 18.77*1.21
  elif "WJetsToLNu_HT-600To800" in sample:  xs = 12.05*1.21
  elif "WJetsToLNu_HT-800To1200" in sample:  xs = 5.501*1.21
  elif "WJetsToLNu_HT-1200To2500" in sample:  xs = 1.33*1.21
  elif "WJetsToLNu_HT-2500ToInf" in sample:  xs = 0.032*1.21

  elif "QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" in sample: xs = 27990000
  elif "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" in sample:   xs = 1717000
  elif "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" in sample:   xs = 351300
  elif "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" in sample:   xs = 31630
  elif "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" in sample:  xs = 6802
  elif "QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" in sample: xs = 1206
  elif "QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" in sample: xs = 120.4
  elif "QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" in sample:  xs = 25.25

  elif "QCD_HT300to500_GenJets5" in sample: xs = 72410
  elif "QCD_HT1500to2000_GenJets5" in sample: xs = 73.7
  elif "QCD_HT1000to1500_GenJets5" in sample: xs = 630
  elif "QCD_HT2000toInf_GenJets5" in sample: xs = 15.52
  elif "QCD_HT500to700_GenJets5" in sample: xs = 11300
  elif "QCD_HT700to1000_GenJets5" in sample: xs = 2965

  elif "QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8" in sample: xs = 557600000

  elif "DYJetsToLL_M-5to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" in sample: xs = 7160*1.23
  elif "DYJetsToLL_M-50_TuneCUETP8M1_13TeV" in sample:     xs = 4895*1.23

  elif "DYJetsToLL_M-50_HT-100to200" in sample:    xs = 139.4*1.23
  elif "DYJetsToLL_M-50_HT-200to400" in sample:    xs = 42.75*1.23
  elif "DYJetsToLL_M-50_HT-400to600" in sample:    xs = 5.497*1.23
  elif "DYJetsToLL_M-50_HT-600toInf" in sample:    xs = 2.21*1.23

  elif "ZJetsToNuNu_HT-100To200" in sample:  xs = 280.35*1.23
  elif "ZJetsToNuNu_HT-200To400" in sample:  xs = 77.67*1.23
  elif "ZJetsToNuNu_HT-400To600" in sample:  xs = 10.73*1.23
  elif "ZJetsToNuNu_HT-600ToInf" in sample:  xs = 4.116*1.23

  elif "VVTo2L2Nu_13TeV_amcatnloFXFX" in sample:   xs = 11.95

  elif "DYBBJetsToLL_M-50" in sample: xs = 11.37

  elif "DYJetsToLL_M-50_Zpt-150toInf" in sample: xs = 19.53

  elif "DYJetsToLL_M-5to50_HT-100to200" in sample: xs = 224.2*1.23
  elif "DYJetsToLL_M-5to50_HT-200to400" in sample: xs = 37.19*1.23
  elif "DYJetsToLL_M-5to50_HT-400to600" in sample: xs = 3.581*1.23
  elif "DYJetsToLL_M-5to50_HT-600toInf" in sample: xs = 1.124*1.23

  elif "GJets_DR-0p4_HT-40To100" in sample: xs = 22760.*1.23
  elif "GJets_DR-0p4_HT-100To200" in sample: xs = 4703.*1.23
  elif "GJets_DR-0p4_HT-200To400" in sample: xs = 836.4*1.23
  elif "GJets_DR-0p4_HT-400To600" in sample: xs = 83.51*1.23
  elif "GJets_DR-0p4_HT-600ToInf" in sample: xs = 24.21*1.23

  elif "GJets_HT-40To100" in sample: xs = 20790.*1.23
  elif "GJets_HT-100To200" in sample: xs = 9238.*1.23
  elif "GJets_HT-200To400" in sample: xs = 2305*1.23
  elif "GJets_HT-400To600" in sample: xs = 274.4*1.23
  elif "GJets_HT-600ToInf" in sample: xs = 93.46*1.23

  elif "VHToNonbb_M125_13TeV_amcatnloFXFX" in sample: xs = 2.171

  elif "WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM" in sample: xs = 50690
  elif "WWTo1L1Nu2Q_13TeV_amcatnloFXFX" in sample: xs = 45.85
  elif "WWZ_TuneCUETP8M1_13TeV-amcatnlo" in sample: xs = 0.1651
  elif "WZTo1L3Nu_13TeV_amcatnloFXFX" in sample: xs = 3.05
  elif "WZZ_TuneCUETP8M1_13TeV-amcatnlo" in sample: xs = 0.05565
  elif "ZZZ_TuneCUETP8M1_13TeV-amcatnlo" in sample: xs = 0.01398
  elif "WWG_TuneCUETP8M1_13TeV-amcatnlo" in sample: xs = 0.2147
  elif "WWW_4F_TuneCUETP8M1_13TeV-amcatnlo" in sample: xs = 0.2086
  else:
    print "Missing xsec for: ", sample   
    xs = 99999999999
  return xs

def equiv_lumi(sample, nevt):
  return nevt/1000./xsec(sample)*pow(1-2*fneg(sample),2)

qry  = 'member_of_campaign=' + 'RunIIWinter15GS'
qry += '&pwg=' + 'SUS'
# qry += '&dataset_name=' + 'SMS*'
# qry += '&approval=' + 'new'

print "Connecting to McM..."
mcm = restful(dev=False) 
print "done."


cols = '{:<100}'.format('Dataset name (McM link)')
cols += '${:<12}'.format('GENSIM status')
cols += '${:<12}'.format('N events')
cols += '${:<12}'.format('Equiv. lumi')
print cols

# old campaigns
reqgs = mcm.getA('requests',query='pwg=SUS&member_of_campaign=RunIISummer15GS')

# ----------- Find requests to be validated in the new campaign
total = 0
for rgs in reqgs:
  if 'sus_delete' in rgs['tags']: continue
  if rgs['flown_with']== "flowLHE2Summer15GS0T": continue
  ds = rgs['dataset_name']
  if ('SMS-T1bbbb' in ds) and (rgs['status']=='new'): continue

  cols ='=HYPERLINK("https://cms-pdmv.cern.ch/mcm/requests?page=0&prepid='+rgs['prepid']+'&shown=138513041465","'+str(rgs['dataset_name'])+'")'
  cols +=' ${:<15}'.format(rgs['status'])
  if (rgs['status']=="done"): 
    cols +=' ${:<15.2f}'.format(rgs['completed_events']/1.0e6)
    cols +=' ${:<15.2f}'.format(equiv_lumi(rgs['dataset_name'],rgs['completed_events']))
  else: 
    cols +=' ${:<15.2f}'.format(rgs['total_events']/1.0e6)
    cols +=' ${:<15.2f}'.format(equiv_lumi(rgs['dataset_name'],rgs['total_events']))

  print cols




