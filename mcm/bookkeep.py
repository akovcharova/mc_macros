#!/usr/bin/env python

# This script should be run on LXPLUS in a clean shell as follows:
# 1. Get an McM cookie:
# [] source /afs/cern.ch/cms/PPD/PdmV/tools/McM/getCookie.sh
# 2. Setup any CMSSW release (needed for python utils)
# 3. Download script:
# [] 
# 4. Run script:
# [] python bookkeep.py

import sys
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import *
from collections import OrderedDict

datasets = OrderedDict([
("TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",[0]),
("TTJets_SingleLeptFromT_Tune",[0,1]),
("TTJets_SingleLeptFromTbar_Tune",[0,1]),
("TTJets_DiLept_Tune",[0,1]),
("TTJets_HT-600to800",[1]),
("TTJets_HT-800to1200",[1]),
("TTJets_HT-1200to2500",[1]),
("TTJets_HT-2500toInf",[1]),
# ("QCD_HT100to200_Tun",[0]),
("QCD_HT200to300_Tun",[0,1]),
("QCD_HT300to500_Tun",[0,1]),
("QCD_HT500to700_Tun",[0,1]),
("QCD_HT700to1000_Tun",[0,1]),
("QCD_HT1000to1500_Tun",[0,1]),
("QCD_HT1500to2000_Tun",[0,1]),
("QCD_HT2000toInf_Tun",[0,1]),
("ZJetsToNuNu_HT-100To200",[0,1]),
("ZJetsToNuNu_HT-200To400",[0,1]),
("ZJetsToNuNu_HT-400To600",[0,1]),
("ZJetsToNuNu_HT-600To800",[0]),
("ZJetsToNuNu_HT-800To1200",[0]),
("ZJetsToNuNu_HT-1200To2500",[0,1]),
("ZJetsToNuNu_HT-2500ToInf",[0]),
# ("WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",[0]),
("WJetsToLNu_HT-100To200",[0,1,2]),
("WJetsToLNu_HT-200To400",[0,1,2]),
("WJetsToLNu_HT-400To600",[0,1]),
("WJetsToLNu_HT-600To800",[0,1]),
("WJetsToLNu_HT-800To1200",[0,1]),
("WJetsToLNu_HT-1200To2500",[0,1]),
("WJetsToLNu_HT-2500ToInf",[0,1]),
("ST_s-channel_4f_leptonDecays",[0]),
("ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1",[0]),
("ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1",[0]),
("ST_tW_antitop_5f_NoFullyHadronicDecays",[0,2]),
("ST_tW_top_5f_NoFullyHadronicDecays",[0,2]),
("TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo",[1,2]),
("TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo",[0]),
("TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX",[1,2]),
("TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX",[0]),
("WWTo1L1Nu2Q_13TeV_amcatnloFXFX",[0]),
("WWTo2L2Nu_13TeV-powheg",[0]),
("WZTo1L1Nu2Q_13TeV_amcatnloFXFX",[0]),
("WZTo1L3Nu_13TeV_amcatnloFXFX",[0]),
("ZZTo2Q2Nu_13TeV_amcatnloFXFX",[0]),
("ZZTo2L2Q_13TeV_amcatnloFXFX",[0]),
("TTTT_TuneCUETP8M1_13TeV-amcatnlo",[0]),
("WWZ_TuneCUETP8M1_13TeV-amcatnlo",[0]),
("WZZ_TuneCUETP8M1_13TeV-amcatnlo",[0]),
("ZZZ_TuneCUETP8M1_13TeV-amcatnlo",[0]),
# ("DYJetsToLL_M-50_Tune*madgraphMLM-pythia8",[1]),
("DYJetsToLL_M-50_HT-100to200",[0,1]),
("DYJetsToLL_M-50_HT-200to400",[0,1]),
("DYJetsToLL_M-50_HT-400to600",[0,1]),
("DYJetsToLL_M-50_HT-600to800",[0,1]),
("DYJetsToLL_M-50_HT-800to1200",[0]),
("DYJetsToLL_M-50_HT-1200to2500",[0]),
("DYJetsToLL_M-50_HT-2500toInf",[0]),
("GJets_HT-100To200",[0,1]),
("GJets_HT-200To400",[0,1]),
("GJets_HT-400To600",[0,1]),
("GJets_HT-600ToInf",[0,1]),
("GJets_DR-0p4_HT-100To200",[0]),
("GJets_DR-0p4_HT-200To400",[0]),
("GJets_DR-0p4_HT-400To600",[0]),
("GJets_DR-0p4_HT-600ToInf",[0])
])

class col:
    magenta = '\033[96m'
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    endc = '\033[0m'
    bold = '\033[1m'
    uline = '\033[4m'

def preq(req,comment=''):
  tot = req['total_events'] 
  cmpl = req['completed_events']
  pct_done = float(cmpl)/float(tot)*100. 
  if pct_done<0: pct_done = 0
  type = 'None'
  if ('MiniAOD' in req['member_of_campaign']): type = 'MiniAOD '
  elif ('DR80' in req['member_of_campaign']): type = 'DIG-REC '
  elif ('GS' in req['member_of_campaign']): type = 'GEN-SIM '
  cols = '{:<10}'.format(req['extension'])
  cols += '{:<72}'.format(req['dataset_name'][0:68])
  cols += type+'{:<15}'.format(req['status'])
  cols += '{:>12.0f}'.format(pct_done)
  cols += '{:>12,}'.format(req['total_events'])
  cols += '  '+comment
  return cols


print "Connecting to McM..."
mcm = restful(dev=False) 
print "done."

cols = '{:<10}'.format('Extension')
cols += '{:<72}'.format('Dataset name')
cols += '{:<23}'.format('Latest status')
cols += '{:>12}'.format('Completed [%]')
cols += '{:>12}'.format('# Events')
print cols

for ds in datasets.keys():
  req_mini = mcm.getA('requests',query='dataset_name='+ds+'*&member_of_campaign=RunIISummer16MiniAODv2')
  for ext in datasets[ds]:
    found_mini = False
    if req_mini:
      for ireq in req_mini:
        if ireq['extension']==ext:
          found_mini = True
          hlight = col.red
          if ireq['status']=='done': hlight = col.green
          elif ireq['status']=='submitted': hlight = ''
          print hlight+preq(ireq)+col.endc
    if not found_mini:
      found_dr = False
      qry = 'dataset_name='+ds+'*&extension='+str(ext)+'&member_of_campaign=RunIISummer16DR80*'
      req_dr = mcm.getA('requests',query=qry)
      if req_dr:
        for ireq in req_dr:
          print col.blue+preq(ireq)+"No MiniAOD request yet."+col.endc
      else:
        qry='dataset_name='+ds+'*&extension='+str(ext)+'&member_of_campaign=RunIISummer15*GS*'
        req_gs = mcm.getA('requests',query=qry)
        if req_gs:
          for ireq in req_gs:
            if '0T' in ireq['flown_with']: continue
            if 'GJets_DR-0p4_HT-400To600' in ireq['dataset_name'] and ireq['version']!=1: continue
            print col.red+preq(ireq,'Missing MiniAOD and DIGIRECO')+col.endc



    






