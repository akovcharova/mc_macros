#!/usr/bin/env python
import sys
import pprint
import string
import time
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import *
import operator
import pickle
from collections import OrderedDict as odict


#------------------------------------------------
#        Query string
#------------------------------------------------
reqQuery = 'member_of_campaign=RunIISpring15FSPremix&pwg=SUS&dataset_name=*SMS*'

#------------------------------------------------
#        Dataset to exclude
#------------------------------------------------
excludeByDataset = ['T5tttt_degen','T5Wg','T2bW']



fsStatusList = ['run','ok','off','dodgy']


def checkPLHE(lhe_list):
  lhe_done = []
  for lhe in lhe_list:
#     if lhe['status'] == 'done' and int(lhe['completed_events'])==int(lhe['total_events']): lhe_done.append(lhe)
    if lhe['status'] == 'done': lhe_done.append(lhe)

  if len(lhe_done)!=1: return None
  else: return lhe_done[0]
  

def getFSStatus(fs_req):

  status = ''
  # Get corresponding pLHE request
  lhe_reqs = mcm.getA('requests',query=reqQuery.replace('RunIISpring15FSPremix','RunIIWinter15pLHE')+'&dataset_name={0}'.format(fs_req['dataset_name']))

  # Get numbers
  nFS_tot = int(fs_req['total_events'])
  nFS_compl = int(fs_req['completed_events'])
  percFS_compl = 100.*float(nFS_compl)/float(nFS_tot)
  nPLHE_compl = 0.
  comment = ''
  lhePrepid = ''


  if not fs_req['status'] == 'done':
    status = 'run'
    if checkPLHE(lhe_reqs):
      nPLHE_compl = int(lhe_reqs[0]['completed_events'])
      lhePrepid = str(lhe_reqs[0]['prepid'])
  else:
    if not checkPLHE(lhe_reqs):
      status = 'dodgy'
      comment = "{0} pLHE requests: {1}".format(len(lhe_reqs),str([str(i['prepid']) for i in lhe_reqs]))    
    elif "Test" in fs_req['dataset_name'] or "duplicate" in fs_req['dataset_name']:
      status = 'dodgy'
      comment = 'Dataset name is suspicious'    
    else:
      nPLHE_compl = int(lhe_reqs[0]['completed_events'])
      lhePrepid = str(lhe_reqs[0]['prepid'])
      if percFS_compl > 95.: status = 'ok'
      else: status = 'off'
      
  return (status,lhePrepid,[fs_req['prepid'],fs_req['status'],fs_req['dataset_name'],'N.A.',str(nFS_tot),str(nFS_compl),str(int(percFS_compl)),comment])


# -------------------------------------------------------------------
#    OK, now we start actually talking to McM...
# -------------------------------------------------------------------

mcm = restful(dev=False) 

fs_list = mcm.getA('requests',query=reqQuery)
fs_list.sort(key=operator.itemgetter('prepid')) # Sort by prepid



# Output
fsReqDict = odict()
for status in fsStatusList:
  fsReqDict[status] = []

# Here we store the prepid of the requests which are marked as ok
req_ok = [ ]

for iReq,fs_req in enumerate(fs_list):
#   # Debug
#   if iReq > 10: break

  (status,lhePrepid,outList) = getFSStatus(fs_req)
  fsReqDict[status].append(",".join(outList))

  dsName = outList[2]

  # Here we decide what we want to keep
  statusOk, dsOk = False, True

  # Check status
  if (status == 'ok' or status == 'off'): statusOk = True

  # Check dataset
  for excl in excludeByDataset:
    if excl in dsName: 
      dsOk = False
      break

  if statusOk and dsOk: req_ok.append(lhePrepid)


for status,outStrList in fsReqDict.iteritems():

  # Write CSV for spreadsheet
  with open("out_{0}.csv".format(status),"wb") as f:
    f.write(",".join(['prepid','status','dataset_name','pLHE compl. evts','FS tot. evts','FS compl. evts','% FS compl.','Comments'])+"\n")
    for outStr in outStrList: f.write(outStr+"\n")


# Dump list to pickle
pickle.dump(req_ok,open('SUS_pLHE_2015.pkl','wb'))
