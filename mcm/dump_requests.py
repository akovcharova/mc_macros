#!/usr/bin/env python
import sys
import pprint
import string
import time
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import *
import operator


#------------------------------------------------
#        Query string
#------------------------------------------------
reqQuery = 'member_of_campaign=RunIISpring15FSPremix&pwg=SUS&dataset_name=*SMS*'


# -------------------------------------------------------------------
#    OK, now we start actually talking to McM...
# -------------------------------------------------------------------

# Keys of request dictionary
#[u'total_events', u'config_id', u'_rev', u'mcdb_id', u'sequences', u'block_black_list', u'block_white_list', u'process_string', u'fragment_tag', u'generator_parameters', u'cmssw_release', u'flown_with', u'priority', u'version', u'generators', u'memory', u'type', u'completed_events', u'status', u'keep_output', u'energy', u'tags', u'fragment', u'_id', u'input_dataset', u'pwg', u'member_of_chain', u'approval', u'name_of_fragment', u'pileup_dataset_name', u'analysis_id', u'time_event', u'reqmgr_name', u'prepid', u'extension', u'size_event', u'notes', u'output_dataset', u'member_of_campaign', u'validation', u'dataset_name', u'history']

mcm = restful(dev=False) 

fs_list = mcm.getA('requests',query=reqQuery)
fs_list.sort(key=operator.itemgetter('prepid')) # Sort by prepid

print "{0} requests match the query:\n{1}".format(len(fs_list),reqQuery)

# Output
outCsv_all = open("out_all.csv","wb")
outCsv_done = open("out_done.csv","wb")
outCsv_ok = open("out_ok.csv","wb")
outCsv_veryOk = open("out_veryOk.csv","wb")
outCsv_run = open("out_run.csv","wb")
outCsv_off = open("out_off.csv","wb")
outCsv_dodgy = open("out_dodgy.csv","wb")


for iReq,fs_req in enumerate(fs_list):
  # # Debug
  # if iReq > 10: break

  # Write header of the table
  if iReq == 0: 
    outCsv_all.write(",".join(['prepid','status','dataset_name','pLHE compl. evts','FS tot. evts','FS compl. evts','% FS compl.'])+"\n")
    outCsv_done.write(",".join(['prepid','status','dataset_name','pLHE compl. evts','FS tot. evts','FS compl. evts','% FS compl.'])+"\n")
    outCsv_ok.write(",".join(['prepid','status','dataset_name','pLHE compl. evts','FS tot. evts','FS compl. evts','% FS compl.'])+"\n")
    outCsv_veryOk.write(",".join(['prepid','status','dataset_name','pLHE compl. evts','FS tot. evts','FS compl. evts','% FS compl.'])+"\n")
    outCsv_run.write(",".join(['prepid','status','dataset_name','pLHE compl. evts','FS tot. evts','FS compl. evts','% FS compl.'])+"\n")
    outCsv_off.write(",".join(['prepid','status','dataset_name','pLHE compl. evts','FS tot. evts','FS compl. evts','% FS compl.'])+"\n")
    outCsv_dodgy.write(",".join(['prepid','status','dataset_name','pLHE compl. evts','FS tot. evts','FS compl. evts','% FS compl.'])+"\n")

  # Get corresponding pLHE request
  lhe_req = mcm.getA('requests',query='member_of_campaign=RunIIWinter15pLHE&pwg=SUS&dataset_name={0}'.format(fs_req['dataset_name']))

  # Get numbers
  nFS_tot = int(fs_req['total_events'])
  nFS_compl = int(fs_req['completed_events'])
  percFS_compl = 100.*float(nFS_compl)/float(nFS_tot)

  # Corresponding pLHE requests does NOT exist, or there are multiple ones
  if len(lhe_req)!=1: 
    outCsv_dodgy.write(",".join([fs_req['prepid'],fs_req['status'],fs_req['dataset_name'],'N.A.',str(nFS_tot),str(nFS_compl),str(int(percFS_compl))])+"\n")
    # All requests
    outCsv_all.write(",".join([fs_req['prepid'],fs_req['status'],fs_req['dataset_name'],'N.A.',str(nFS_tot),str(nFS_compl),str(int(percFS_compl))])+"\n")
    continue

  # Corresponding pLHE exists
  else:
    nPLHE_compl = int(lhe_req[0]['completed_events'])

    # All requests
    outCsv_all.write(",".join([fs_req['prepid'],fs_req['status'],fs_req['dataset_name'],str(nPLHE_compl),str(nFS_tot),str(nFS_compl),str(int(percFS_compl))])+"\n")
  
    # Requests in status 'done'
    if fs_req['status'] == 'done': 
      outCsv_done.write(",".join([fs_req['prepid'],fs_req['status'],fs_req['dataset_name'],str(nPLHE_compl),str(nFS_tot),str(nFS_compl),str(int(percFS_compl))])+"\n")

      # Requests with completed events matching the requested events
      if abs(percFS_compl-100.)<5 or nFS_compl == -1: outCsv_veryOk.write(",".join([fs_req['prepid'],fs_req['status'],fs_req['dataset_name'],str(nPLHE_compl),str(nFS_tot),str(nFS_compl),str(int(percFS_compl))])+"\n")

      # Requests with completed events NOT matching the requested events
      if percFS_compl < 95.: outCsv_off.write(",".join([fs_req['prepid'],fs_req['status'],fs_req['dataset_name'],str(nPLHE_compl),str(nFS_tot),str(nFS_compl),str(int(percFS_compl))])+"\n")
      # Requests with compl. evt > 95%
      else: outCsv_ok.write(",".join([fs_req['prepid'],fs_req['status'],fs_req['dataset_name'],str(nPLHE_compl),str(nFS_tot),str(nFS_compl),str(int(percFS_compl))])+"\n")

    # Requests NOT in status 'done'
    else: outCsv_run.write(",".join([fs_req['prepid'],fs_req['status'],fs_req['dataset_name'],str(nPLHE_compl),str(nFS_tot),str(nFS_compl),str(int(percFS_compl))])+"\n")

    continue



# Close files
outCsv_all.close()
outCsv_done.close()
outCsv_ok.close()
outCsv_veryOk.close()
outCsv_run.close()
outCsv_off.close()
outCsv_dodgy.close()
