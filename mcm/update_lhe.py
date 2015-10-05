#!/usr/bin/env python

import sys
import pprint
import string
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import *
from collections import namedtuple

dataset = namedtuple("dataset","lhe_pid name ngs xsec xsec_err xsec_match xsec_match_err eff eff_err")

dslist = [
dataset('SUS-RunIIWinter15wmLHE-00074', 'GJets_DR-0p4_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', 15., 9.371e+04, 1.289e+02,   2.276e+04, 2.561e+02 , 24.3, 0.3),
dataset('SUS-RunIIWinter15wmLHE-00071', 'GJets_DR-0p4_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', 15., 4.148e+04, 4.980e+01,   4.703e+03, 8.337e+01 , 11.3, 0.2),
dataset('SUS-RunIIWinter15wmLHE-00072', 'GJets_DR-0p4_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', 50., 1.148e+04, 1.421e+01,   8.364e+02,  1.890e+01,  7.3, 0.2),
dataset('SUS-RunIIWinter15wmLHE-00073', 'GJets_DR-0p4_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', 12.5, 1.531e+03, 2.164e+00,   8.351e+01,  2.202e+00,  5.5, 0.1),
dataset('SUS-RunIIWinter15wmLHE-00075', 'GJets_DR-0p4_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', 12.5, 5.614e+02, 7.534e-01,   2.421e+01,  7.219e-01,  4.3, 0.1)
]
   
github_slha = '3d2a622681660309670944c91e095403ddcb069c'

print "Connecting to McM..."
mcm = restful(dev=False)
print "done."

dotwiki = False
if dotwiki: 
  twiki = open("table_gjets.txt","w")
  twiki.write("Please chain the following requests to BOTH *RunIIWinter15GS+RunIISpring15DR74* and *RunIISummer15GS*:\n")
  twiki.write("| *row* | *prepid* | *Dataset* | *N_events* | *Comments* | *RM's comments* | *RM responsible* |\n")

for ds in dslist:
  print "Working on dataset", ds.name
  print "requesting ", ds.ngs
  print "with before cross_section", ds.xsec,"+-", ds.xsec_err
  print "with after cross_section", ds.xsec_match,"+-", ds.xsec_match_err
  print "with efficiency", ds.eff,"+-", ds.eff_err

  req = mcm.getA('requests',ds.lhe_pid)
  print "Got requests: ", req['prepid']

  req['total_events'] = 1.0e6*ds.ngs/(ds.eff-ds.eff_err)*100.
  req['fragment'] = string.replace(string.replace(req['fragment'], "9599bc7c1606c89a883506411f5189fbda5c61c3", github_slha),"GJets_","GJets_DR-0p4_")
  req['notes'] = "Gamma+Jets with minimum distance between jet and photon = 0.4.\nCross-section before matching: "+'{0:.0f}'.format(ds.xsec)+" +- "+'{0:.0f}'.format(ds.xsec_err)+" pb"
  req['dataset_name'] = ds.name
  req['validation']['valid'] = True
  req['validation']['nEvents'] = 30

  answer = mcm.updateA('requests', req)
  print "Updated."

  
  if dotwiki: 
    twiki.write("|"+"|".join([str(ind), ds.lhe_pid,ds.name, str(ds.ngs),'','',''])+"|\n")

if dotwiki: twiki.close()
