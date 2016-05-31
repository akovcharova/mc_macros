#!/usr/bin/env python

### Retrieve progress information for lists of McM requests
### Author: Dustin Anderson

import sys
import csv

#load McM interface
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import *

#For each sample name, provide a number indicating the number of copies of the request
#(2 if there is an extension to the dataset, otherwise 1)
SAMPLES_TTJETS = [
    ("TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 2), 
    ("TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 2),
    ("TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 2),
    ("TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 2),
    ("TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 2),
    ("TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 2),
    ("TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 2),
    ]

SAMPLES_TTX = [
    ("TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8", 1),
    ("TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8", 1),
    ("TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8", 1),
    ("TTZToLLNuNu_M-1to10_TuneCUETP8M1_13TeV-amcatnlo-pythia8", 1),
    ("TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8", 1),
    ("TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8", 1),
    ("TTWW_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 1),
    ("TTTT_TuneCUETP8M1_13TeV-amcatnlo-pythia8", 1),
    ]

SAMPLES_DIBOSON = [
    ("WGJets_MonoPhoton_PtG-130_TuneCUETP8M1_13TeV-madgraph", 1),
    ("WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8", 1),
    ("ZNuNuGJets_MonoPhoton_PtG-40To130_TuneCUETP8M1_13TeV-madgraph", 1),
    ("ZNuNuGJets_MonoPhoton_PtG-130_TuneCUETP8M1_13TeV-madgraph", 1),
    ("ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8", 1),
    ("VHToNonbb_M125_13TeV_amcatnloFXFX_madspin_pythia8", 1),
    ("VVTo2L2Nu_13TeV_amcatnloFXFX_madspin_pythia8", 1),
    ("WWTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8", 1),
    ("WWTo2L2Nu_13TeV-powheg", 1),
    ("WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8", 1),
    ("WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8", 1),
    ("WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8", 1),
    ("ZZTo4L_13TeV_powheg_pythia8", 1),
    ("ZZTo2L2Nu_13TeV_powheg_pythia8", 1),
    ("ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8", 1),
    ("WW_DoubleScattering_13TeV-pythia8", 1),
    ("WpWpJJ_EWK-QCD_TuneCUETP8M1_13TeV-madgraph-pythia8", 1),
    ]

SAMPLES = [SAMPLES_TTJETS,SAMPLES_TTX,SAMPLES_DIBOSON]
campaigns = ['RunIISummer15GS', 'RunIISpring16DR80', 'RunIISpring16MiniAODv2']

def requestInfo(r):
    percComplete = r['completed_events']*100.0/r['total_events']
    outString = r['member_of_campaign']+' '+r['dataset_name']+' ('+r['pwg']+'): \n'+r['status']+' (%.0f%%, %d of %d)'%(percComplete,r['completed_events'],r['total_events']) 
    return outString

def requestInfoShort(r):
    percComplete = r['completed_events']*100.0/r['total_events']
    outString = r['status']+' (%.0f%%)'%percComplete
    return outString

if __name__ == '__main__':

    print "Connecting to McM..."
    mcm = restful(dev=False)
    print "done."

    #open CSV file for writing
    with open('requests.csv', 'wb') as outfile:
        writer = csv.writer(outfile)

        for group in SAMPLES:
            for (sample,reps) in group:
                for irep in range(reps): #when we have more than one request with the same name
                    reqcells = []
                    for campaign in campaigns:
                        query='member_of_campaign=%s&dataset_name=%s'%(campaign,sample)
                        reqs = mcm.getA('requests', query=query)
                        if irep > len(reqs)-1:
                            print "Didn't find enough requests with dataset name",sample
                            reqcells.append('')
                            continue
                        req = reqs[irep]
                        print requestInfo(req)
                        reqcells.append(requestInfoShort(req)) 
                    writer.writerow(reqcells)
            #write blank row
            writer.writerow(['' for c in campaigns])
