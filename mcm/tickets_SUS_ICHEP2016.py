# This requires to a pickle file with a list of prepids as input
# For instance, such input is produce by dump_requests.py

#!/usr/bin/env python
import sys
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import *
import pickle


maxReqPerTicket = 80

mcm = restful(dev=False) 

pwg = 'SUS'
chain = 'RunIISpring16DR80PU2016MiniAODv1'

reqList = pickle.load(open('SUS_pLHE_2015.pkl','rb'))
reqList = sorted(reqList)

prepidsList = []

iList = 0
prepidsList_tmp = []
for i,lhe_req in enumerate(reqList):    
        
    if i/maxReqPerTicket != iList and i!=0: 
        iList = i/maxReqPerTicket
        prepidsList.append(prepidsList_tmp)
        prepidsList_tmp = []
    elif i==len(reqList)-1: prepidsList.append(prepidsList_tmp)

    prepidsList_tmp.append(lhe_req)


for iTicket,prepids in enumerate(prepidsList):
    

    mccm_ticket = { 'prepid' : pwg, ## this is how one passes it in the first place
                    'pwg' : pwg,
                    'requests'  : prepids,
                    'notes' : "SUS scan requests, bunch {0}".format(iTicket+1),
                    'chains' : [],
                    'repetitions' : 1,
                    'block' : 3
                    } 
    # print mccm_ticket

    mcm.putA('mccms', mccm_ticket) 
