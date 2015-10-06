#!/usr/bin/env python

import sys
import pprint
import string, time
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import *
from collections import namedtuple

dataset = namedtuple("dataset","gs_pid name ngs xsec xsec_err xsec_match xsec_match_err eff eff_err")

dslist = [
# dataset('SUS-RunIIWinter15GS-00151', 'GJets_DR-0p4_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', 15., 9.371e+04, 1.289e+02,   2.276e+04, 2.561e+02 , 24.3, 0.3),
dataset('SUS-RunIIWinter15GS-00148', 'GJets_DR-0p4_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', 15., 4.148e+04, 4.980e+01,   4.703e+03, 8.337e+01 , 11.3, 0.2),
dataset('SUS-RunIIWinter15GS-00150', 'GJets_DR-0p4_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', 50., 1.148e+04, 1.421e+01,   8.364e+02,  1.890e+01,  7.3, 0.2),
dataset('SUS-RunIIWinter15GS-00149', 'GJets_DR-0p4_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', 12.5, 1.531e+03, 2.164e+00,   8.351e+01,  2.202e+00,  5.5, 0.1),
dataset('SUS-RunIIWinter15GS-00152', 'GJets_DR-0p4_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8', 12.5, 5.614e+02, 7.534e-01,   2.421e+01,  7.219e-01,  4.3, 0.1)
]

ref_pid = 'SUS-RunIIWinter15GS-00018'

print "Connecting to McM..."
mcm = restful(dev=False)
print "done."

for ds in dslist:
  print "Working on dataset", ds.name
  # print "requesting ", ds.ngs
  # print "with before cross_section", ds.xsec,"+-", ds.xsec_err
  # print "with after cross_section", ds.xsec_match,"+-", ds.xsec_match_err
  # print "with efficiency", ds.eff,"+-", ds.eff_err
  
  # get the template fragment
  req_frag = mcm.getA('requests',ref_pid)

  req = mcm.getA('requests',ds.gs_pid)
  req['validation']['valid'] = True
  req['validation']['nEvents'] = 30
  req['total_events'] = ds.ngs*1e6
  req['size_event'] = 800
  req['time_event'] = 10
  req['extension'] = 0
  req['validation']['valid'] = True
  req['validation']['nEvents'] = 30
  req['generator_parameters'] = [{
                                 "submission_details": {
                                    "author_email": "Ana.Ovcharova@cern.ch", 
                                    "submission_date": time.strftime("%Y-%m-%d-%H-%M", time.gmtime()),
                                    "author_username": "ana", 
                                    "author_name": "Ana Krasimirova Ovcharova"
                                  }, 
                                  "match_efficiency_error": ds.eff_err/100., 
                                  "match_efficiency": ds.eff/100., 
                                  "filter_efficiency": 1., 
                                  "cross_section": ds.xsec_match, 
                                  "filter_efficiency_error": 0.
                                }]

  req['fragment'] = string.replace(req_frag['fragment'], 'qCut = 19.', 'qCut = 11.')
  req['notes'] = "Gamma+Jets with minimum distance between jet and photon = 0.4.\nCross-section after matching: "+'{0:.0f}'.format(ds.xsec_match)+" +- "+'{0:.0f}'.format(ds.xsec_match_err)+" pb"

  answer = mcm.updateA('requests', req)

