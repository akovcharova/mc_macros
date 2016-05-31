#!/usr/bin/env python
import sys
import pprint
import string
import time
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import *
import operator
from collections import namedtuple
from collections import OrderedDict as odict


#------------------------------------------------
#        Datasets
#------------------------------------------------

datasets = [
  "GJets_DR-0p4_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
  "GJets_DR-0p4_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
  "GJets_DR-0p4_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
  "GJets_DR-0p4_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
  "GJets_DR-0p4_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
  "QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
  "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
  "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
  "QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
  "QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
  "QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
  "QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
  "QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
  "QCD_HT300to500_GenJets5_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
  "QCD_HT500to700_GenJets5_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
  "QCD_HT700to1000_GenJets5_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
  "QCD_HT1000to1500_GenJets5_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
  "QCD_HT1500to2000_GenJets5_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
  "QCD_HT2000toInf_GenJets5_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
  "QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8",
  "SMS-T1bbbb_mGluino-1000_mLSP-900_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
  "SMS-T1bbbb_mGluino-1500_mLSP-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
  "SMS-T1qqqq_mGluino-1000_mLSP-800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
  "SMS-T1qqqq_mGluino-1400_mLSP-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
  "SMS-T1tttt_mGluino-1200_mLSP-800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
  "SMS-T1tttt_mGluino-1500_mLSP-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
  "SMS-T2tt_mStop-425_mLSP-325_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
  "SMS-T2tt_mStop-500_mLSP-325_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
  "SMS-T2tt_mStop-850_mLSP-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"
]


#------------------------------------------------
#        Campaigns
#------------------------------------------------

Campaign = namedtuple('Campaign','name abbr dataset_type')

GS = Campaign(name="RunIISummer15GS",abbr="GS",dataset_type="GEN-SIM")
DR = Campaign(name="RunIISpring16DR80",abbr="DR",dataset_type="AODSIM")
MA = Campaign(name="RunIISpring16MiniAODv2",abbr="MA",dataset_type="MINIAODSIM")

campaigns = [GS,DR,MA]


# -------------------------------------------------------------------
#    OK, now we start actually talking to McM...
# -------------------------------------------------------------------

mcm = restful(dev=False) 

# dataset_name,ext,campaign,completion
datasetDict = odict()

# This loop will fill the dictionary with the information 
# on the extensions of each dataset and the completion for each campaign
for ds in datasets:

  datasetDict[ds] = odict()
  print "Chasing dataset ",ds

  for iCamp,campaign in enumerate(campaigns):

    requests = mcm.getA('requests',query='member_of_campaign={0}&dataset_name={1}'.format(campaign.name,ds))
    # print "  campaign: {0} has {1} requests".format(campaign.name,len(requests))

    # It means we don't have "extensions"
    if len(requests) == 1:
      req = requests[0]
      outDs, condition = None, None
      ext = "ext0"
      nCom,nTot = int(req["completed_events"]),int(req["total_events"])
      compl = float(nCom)/float(nTot)
      status = req['status']
      for out_ds in req['output_dataset']:
        out_ds_type = str(out_ds).split("/")[-1].strip()        
        condition = str(out_ds).split("/")[2]
        if out_ds_type == campaign.dataset_type: 
          outDs = str(out_ds)          
          break

      if iCamp == 0: datasetDict[ds][ext] = odict()
      datasetDict[ds]["ext0"][campaign] = (status,compl)

              
    # It means we have "extensions"
    elif len(requests) > 1:
      for req in requests:    
        outDs,condition = None,None
        nCom,nTot = int(req["completed_events"]),int(req["total_events"])
        compl = float(nCom)/float(nTot)
        status = req['status']
        for out_ds in req['output_dataset']:
          out_ds_type = str(out_ds).split("/")[-1].strip()        
          condition = str(out_ds).split("/")[2]
          if out_ds_type == campaign.dataset_type: 
            outDs = str(out_ds)            
            break

        # Find the ext number
        if "ext" in condition: ext = "ext"+condition[condition.find("ext")+3]
        else: ext = "ext0"

        if iCamp == 0: datasetDict[ds][ext] = odict()
        datasetDict[ds][ext][campaign] = (status,compl)


    else: pass




# This loop will print the status with pretty formatting
for ds,dsDict in datasetDict.iteritems():
  for ext,campDict in dsDict.iteritems():
    
    outStr = ""

    campCounter = 0
    for campaign,(status,compl) in campDict.iteritems():

      if campCounter==0: outStr += "    {0} {1}/{2} ({3}%)".format(ds+" "+ext,campaign.abbr,status,int(round(100*compl)))
      else: outStr += " {0}/{1} ({2}%)".format(campaign.abbr,status,int(round(100*compl)))
      
      campCounter += 1

    print outStr
    
