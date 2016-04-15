#!/usr/bin/env python
import sys
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import *


print "Connecting to McM..."
mcm = restful(dev=False) 
print "done."

pwg = 'SUS'
chain = 'RunIISpring16DR80PU2016MiniAODv1'

prepids = ["SUS-RunIISummer15GS-00031",
"SUS-RunIISummer15GS-00045",
"SUS-RunIISummer15GS-00030",
"SUS-RunIISummer15GS-00046",
"SUS-RunIISummer15GS-00036",
"SUS-RunIISummer15GS-00052",
"SUS-RunIISummer15GS-00120",
"SUS-RunIISummer15GS-00119",
"SUS-RunIISummer15GS-00130",
"SUS-RunIISummer15GS-00049",
"SUS-RunIISummer15GS-00037",
"SUS-RunIISummer15GS-00038",
"SUS-RunIISummer15GS-00039",
"SUS-RunIISummer15GS-00044",
"SUS-RunIISummer15GS-00043",
# DYJets other
"SUS-RunIISummer15GS-00040",
"SUS-RunIISummer15GS-00058",
# DYJets high-mll
"SUS-RunIISummer15GS-00118",
"SUS-RunIISummer15GS-00141",
"SUS-RunIISummer15GS-00114",
# DYJets low-mll
"SUS-RunIISummer15GS-00117",
"SUS-RunIISummer15GS-00124",
"SUS-RunIISummer15GS-00145",
"SUS-RunIISummer15GS-00126",
# ZJets 
"SUS-RunIISummer15GS-00143",
"SUS-RunIISummer15GS-00123",
"SUS-RunIISummer15GS-00137",
# old GJets
"SUS-RunIISummer15GS-00016",
"SUS-RunIISummer15GS-00017",
"SUS-RunIISummer15GS-00018",
"SUS-RunIISummer15GS-00015",
"SUS-RunIISummer15GS-00024",
# new GJets
"SUS-RunIISummer15GS-00142",
"SUS-RunIISummer15GS-00138",
"SUS-RunIISummer15GS-00147",
"SUS-RunIISummer15GS-00153",
"SUS-RunIISummer15GS-00172",
# WJets HT bins
"SUS-RunIISummer15GS-00009",
"SUS-RunIISummer15GS-00011",
"SUS-RunIISummer15GS-00020",
"SUS-RunIISummer15GS-00021",
"SUS-RunIISummer15GS-00022",
"SUS-RunIISummer15GS-00023",
"SUS-RunIISummer15GS-00134",
"SUS-RunIISummer15GS-00132",
"SUS-RunIISummer15GS-00121",
"SUS-RunIISummer15GS-00136",
"SUS-RunIISummer15GS-00122",
"SUS-RunIISummer15GS-00128",
"SUS-RunIISummer15GS-00135",
"SUS-RunIISummer15GS-00026",
#VHTononbb
"SUS-RunIISummer15GS-00050",
# Di-/Tri boson
"SUS-RunIISummer15GS-00053",
"SUS-RunIISummer15GS-00054",
"SUS-RunIISummer15GS-00047",
"SUS-RunIISummer15GS-00151",
"SUS-RunIISummer15GS-00113",
"SUS-RunIISummer15GS-00055",
"SUS-RunIISummer15GS-00112",
# QCD HT_bins
"SUS-RunIISummer15GS-00001",
"SUS-RunIISummer15GS-00129",
"SUS-RunIISummer15GS-00005",
"SUS-RunIISummer15GS-00139",
"SUS-RunIISummer15GS-00002",
"SUS-RunIISummer15GS-00116",
"SUS-RunIISummer15GS-00003",
"SUS-RunIISummer15GS-00140",
"SUS-RunIISummer15GS-00006",
"SUS-RunIISummer15GS-00146",
"SUS-RunIISummer15GS-00004",
"SUS-RunIISummer15GS-00131",
"SUS-RunIISummer15GS-00007",
"SUS-RunIISummer15GS-00127",
"SUS-RunIISummer15GS-00154",
"SUS-RunIISummer15GS-00158",
"SUS-RunIISummer15GS-00159",
"SUS-RunIISummer15GS-00156",
"SUS-RunIISummer15GS-00155",
"SUS-RunIISummer15GS-00157",
# Benchmark points
"SUS-RunIISummer15GS-00060",
"SUS-RunIISummer15GS-00061",
"SUS-RunIISummer15GS-00062",
"SUS-RunIISummer15GS-00063",
"SUS-RunIISummer15GS-00064",
"SUS-RunIISummer15GS-00065",
"SUS-RunIISummer15GS-00162",
"SUS-RunIISummer15GS-00111",
"SUS-RunIISummer15GS-00110"
]

mccm_ticket = { 'prepid' : pwg, ## this is how one passes it in the first place
                'pwg' : pwg,
                'requests'  : prepids,
                'notes' : "SUS tranche-1 requests",
                'chains' : [chain],
                'repetitions' : 1,
                'block' : 2
              } 
print mccm_ticket

mcm.putA('mccms', mccm_ticket) 
