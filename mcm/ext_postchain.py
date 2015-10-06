#!/usr/bin/env python

import sys
import pprint
import string, time
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import *

dsdict = {
'TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 15.,
'TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 10.5,
'TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 3.,
'TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 1.5,
'WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 400.,
'WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 30.,
'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 15.,
'WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 6.,
'WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 16.,
'WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 6.4,
'WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 7.25,
'WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 2.25,
'DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 7.8,
'DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 9.,
'DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 9.,
'DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 4.,
'DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 9.,
'DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 2.,
'DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 2.,
'DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 2.,
'ZJetsToNuNu_HT-100To200_13TeV-madgraph' : 20.,
'ZJetsToNuNu_HT-200To400_13TeV-madgraph' : 20.,
'ZJetsToNuNu_HT-400To600_13TeV-madgraph' : 9.,
'ZJetsToNuNu_HT-600ToInf_13TeV-madgraph' : 9.,
'QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 40.,
'QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 40.,
'QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 40.,
'QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 30.,
'QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 10.,
'QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 8.,
'QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 4.
}

print "Connecting to McM..."
mcm = restful(dev=False)
print "done."

for dsname in sorted(dsdict.keys()):
  print "%s: Searching McM..." % dsname
  reqs = mcm.getA('requests',query='dataset_name='+dsname)
  rgs, rlhe, refgs = {}, {}, {}
  nrgs, nrlhe, nrefgs = 0,0,0
  for r in reqs:    
    if r['status']=='done' and r['member_of_campaign']=='RunIIWinter15GS': 
      refgs = r
      nrefgs  = nrefgs + 1
    if r['status']=='new':
      if r['member_of_campaign']=='RunIIWinter15GS': 
        rgs = r
        nrgs = nrgs + 1
      if r['member_of_campaign']=='RunIIWinter15wmLHE': 
        rlhe = r
        nrlhe = nrlhe + 1

  # Info messages
  if nrgs==0: sys.exit('*** ERROR: %s: GS request not found.' % dsname)
  elif nrgs>1: sys.exit('*** ERROR: %s: Found more than one GS request.' % dsname)
  if nrlhe==0: sys.exit('*** ERROR: %s: LHE request not found.' % dsname)
  elif nrlhe>1: sys.exit('*** ERROR: %s: Found more than one LHE request.' % dsname)
  if nrefgs==0: sys.exit('*** ERROR: %s: Reference GS request not found.' % dsname)
  elif nrefgs>1: sys.exit('*** ERROR: %s: Found more than one reference GS request.' % dsname)

  # Issue option reset on LHE request
  answer = mcm.option_reset(rlhe['prepid'])
  if answer['results']: print "%s Issued option_reset" % rlhe['prepid']
  else: sys.exit("*** ERROR: %s: Option_reset failed with msg:%s" % (dsname,answer['message']))

  ref_gen_pars = refgs['generator_parameters'].pop()

  rgs['generator_parameters'] = [{
                                 "submission_details": {
                                    "author_email": "Ana.Ovcharova@cern.ch", 
                                    "submission_date": time.strftime("%Y-%m-%d-%H-%M", time.gmtime()),
                                    "author_username": "ana", 
                                    "author_name": "Ana Krasimirova Ovcharova"
                                  }, 
                                  "match_efficiency_error": ref_gen_pars["match_efficiency_error"],
                                  "match_efficiency": ref_gen_pars["match_efficiency"],
                                  "filter_efficiency": ref_gen_pars["filter_efficiency"],
                                  "cross_section": ref_gen_pars["cross_section"],
                                  "filter_efficiency_error": ref_gen_pars["filter_efficiency_error"]
                                }]
  rgs['validation']['valid'] = True
  rgs['validation']['nEvents'] = 30
  rgs['total_events'] = dsdict[dsname]*1e6
  rgs['size_event'] = refgs['size_event']
  rgs['time_event'] = refgs['time_event']
  rgs['extension'] = 1

  rgs['fragment'] = refgs['fragment']
  rgs['notes'] = refgs['notes']

  answer = mcm.updateA('requests', rgs)
  if answer['results']: print "%s: Updated GS request for " % rgs['prepid']
  else: sys.exit("*** ERROR: %s: GS request update failed with msg:%s" %(rgs['prepid'], answer['message']))

  chain_name = rlhe['member_of_chain'].pop()
  url = "restapi/chained_requests/test/%s" % chain_name
  answer = mcm.get(url)
  if answer['results']: print "%s: Started validation." % chain_name
  else: sys.exit("*** ERROR: %s: Validation command failed with msg:%s" %(chain_name, answer['message']))

  print '-'*80

