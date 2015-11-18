#!/usr/bin/env python
import sys
import pprint
import string
import time
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import *
from collections import namedtuple


#------------------------------------------------
#        Options
#------------------------------------------------
create_lhe_requests = False 
update_fs_requests = True
if (create_lhe_requests and update_fs_requests):
  sys.exit("ERROR: If the LHE request is being created now, then the FastSim request does not exist yet!")

#------------------------------------------------
#        Submitter info
#------------------------------------------------
author_email = "Ana.Ovcharova@cern.ch"
author_name = "Ana Ovcharova"
author_username = "ana"

#--------------------------------------------------------------
# New pLHE requests will be created by cloning the request 
# specified by the following prep_id
#--------------------------------------------------------------
lhe_ref = 'SUS-RunIIWinter15pLHE-00012'

#--------------------------------------------------------------
#        pLHE request defaults applying to all requests
#--------------------------------------------------------------
lhe_time_event = 0.01 # time per lhe event in sec
lhe_size_event = 2. # size per lhe event in kB
generator = 'madgraph'


#--------------------------------------------------------------
#       FastSim request defaults applying to all requests
#--------------------------------------------------------------
match_eff_err = 0.01
fs_time_event = 2. # time per sim event in sec
fs_size_event = 230. # size per sim event in kB

#--------------------------------------------------------------
#       Fill in per-dataset level info for each request
#--------------------------------------------------------------
dataset = namedtuple("dataset","name mcdbid nevt_lhe match_eff qcut notes")

dslist = [
dataset(name = "SMS-T2tt_mStop-100-125_mLSP-1to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        mcdbid = 15372, 
        nevt_lhe = 20000000, 
        match_eff = 0.25, 
        qcut = 57,
        notes = ""),
dataset(name = "SMS-T2tt_mStop-150-175_mLSP-1to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        mcdbid = 15376, 
        nevt_lhe = 36000000, 
        match_eff = 0.25, 
        qcut = 57,
        notes = ""),
dataset(name = "SMS-T2tt_mStop-200_mLSP-1to125_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        mcdbid = 15375, 
        nevt_lhe = 24000000, 
        match_eff = 0.25, 
        qcut = 57,
        notes = ""),
dataset(name = "SMS-T2tt_mStop-225_mLSP-25to150_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        mcdbid = 15374, 
        nevt_lhe = 24000000, 
        match_eff = 0.25, 
        qcut = 57,
        notes = ""),
dataset(name = "SMS-T2tt_mStop-250_mLSP-1to175_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        mcdbid = 15370, 
        nevt_lhe = 25000000, 
        match_eff = 0.25, 
        qcut = 57,
        notes = ""),
dataset(name = "SMS-T2tt_mStop-275_mLSP-75to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        mcdbid = 15373, 
        nevt_lhe = 16200000, 
        match_eff = 0.25, 
        qcut = 57,
        notes = ""),
dataset(name = "SMS-T2tt_mStop-300to375_mLSP-1to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        mcdbid = 15378, 
        nevt_lhe = 28900000, 
        match_eff = 0.25, 
        qcut = 57,
        notes = "Full tag did not fit in N_chars limit: mStop-300-325-350-375_mLSP-1to225-125to250-1to275-175to300"),
dataset(name = "SMS-T2tt_mStop-400to475_mLSP-1to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        mcdbid = 15371, 
        nevt_lhe = 17000000, 
        match_eff = 0.25, 
        qcut = 57,
        notes = "Full tag did not fit in N_chars limit: mStop-400-425-450-475_mLSP-1to325-225to350-1to375-275to400"),
dataset(name = "SMS-T2tt_mStop-500-525-550_mLSP-1to425-325to450-1to475_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        mcdbid = 15377, 
        nevt_lhe = 13400000, 
        match_eff = 0.25, 
        qcut = 57,
        notes = ""),
dataset(name = "SMS-T2tt_mStop-600-950_mLSP-1to450_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
        mcdbid = 15369, 
        nevt_lhe = 32000000, 
        match_eff = 0.25, 
        qcut = 59,
        notes = "")
]

# ====================================================================================================================
# For the generic case, nothing should change below this line, but of course there are exceptions so read on... 
# e.g. maybe some model is generated with more/less than 2 extra jets in the ME => fragment needs to be modified
# ====================================================================================================================

# ---------------------------------------------------------------------------------
# Generic generator parameters dictionaries, when looping  through the datasets
# match_eff_err will be replaced with the value for the particular dataset
# ---------------------------------------------------------------------------------
lhe_gen_params = [{"submission_details": {
                      "author_email": author_email, 
                      "submission_date": time.strftime("%Y-%m-%d-%H-%M", time.gmtime()),
                      "author_username": author_username, 
                      "author_name": author_name
                    }, 
                    "version": 0,
                    "cross_section": 1., 
                    "filter_efficiency": 1., 
                    "filter_efficiency_error": 0.,
                    "match_efficiency": 1., 
                    "match_efficiency_error": 0.
                  }]
fs_gen_params = [{"submission_details": {
                    "author_email": author_email, 
                    "submission_date": time.strftime("%Y-%m-%d-%H-%M", time.gmtime()),
                    "author_username": author_username, 
                    "author_name": author_name
                  }, 
                  "version": 0,
                  "cross_section": 1., 
                  "filter_efficiency": 1., 
                  "filter_efficiency_error": 0.,
                  "match_efficiency": 999., # this will be replaced with value from dictionary
                  "match_efficiency_error": match_eff_err
                }]

# -----------------------------------------------------------------------------------
# Generic fragment for the fastsim request, when looping through the datasets
# the qcut will be replaced with the value for the particular dataset
# -----------------------------------------------------------------------------------
fs_fragment = "import FWCore.ParameterSet.Config as cms\n\
from Configuration.Generator.Pythia8CommonSettings_cfi import *\n\
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *\n\
generator = cms.EDFilter(\"Pythia8HadronizerFilter\",\n\
  maxEventsToPrint = cms.untracked.int32(1),\n\
  pythiaPylistVerbosity = cms.untracked.int32(1),\n\
  filterEfficiency = cms.untracked.double(1.0),\n\
  pythiaHepMCVerbosity = cms.untracked.bool(False),\n\
  comEnergy = cms.double(13000.),\n\
  PythiaParameters = cms.PSet(\n\
    pythia8CommonSettingsBlock,\n\
    pythia8CUEP8M1SettingsBlock,\n\
    JetMatchingParameters = cms.vstring(\n\
      \'JetMatching:setMad = off\',\n\
      \'JetMatching:scheme = 1\',\n\
      \'JetMatching:merge = on\',\n\
      \'JetMatching:jetAlgorithm = 2\',\n\
      \'JetMatching:etaJetMax = 5.\',\n\
      \'JetMatching:coneRadius = 1.\',\n\
      \'JetMatching:slowJetPower = 1\',\n\
      \'JetMatching:qCut = 999.\', #this is the actual merging scale\n\
      \'JetMatching:nQmatch = 5\', #4 corresponds to 4-flavour scheme (no matching of b-quarks), 5 for 5-flavour scheme\n\
      \'JetMatching:nJetMax = 2\', #number of partons in born matrix element for highest multiplicity\n\
      \'JetMatching:doShowerKt = off\', #off for MLM matching, turn on for shower-kT matching\n\
    ), \n\
    parameterSets = cms.vstring(\'pythia8CommonSettings\',\n\
      \'pythia8CUEP8M1Settings\',\n\
      \'JetMatchingParameters\'\n\
    )\n\
  )\n\
)\n\
ProductionFilterSequence = cms.Sequence(generator)\n"


# -------------------------------------------------------------------
#    OK, now we start actually talking to McM...
# -------------------------------------------------------------------

print "Connecting to McM..."
mcm = restful(dev=False) 
print "done."

for ds in dslist:
  print "Working on dataset", ds.name

  if (create_lhe_requests):
    # get the dictionary from the reference request
    ref_lhe_dict = mcm.getA('requests',lhe_ref)  # returns either dictionary or None 
    if not ref_lhe_dict: sys.exit("*** ERROR: Failed retrieving reference LHE request")

    # make modifications to the dictionary
    ref_lhe_dict['total_events'] = ds.nevt_lhe
    ref_lhe_dict['mcdb_id'] = ds.mcdbid
    ref_lhe_dict['generators'] = [generator]
    ref_lhe_dict['dataset_name'] = ds.name
    ref_lhe_dict['generator_parameters'] = lhe_gen_params
    ref_lhe_dict['size_event'] = lhe_size_event
    ref_lhe_dict['time_event'] = lhe_time_event
    ref_lhe_dict['notes'] = ds.notes

    # create the clone with the modified dictionary 
    new_lhe_request = mcm.clone(ref_lhe_dict['prepid'], ref_lhe_dict)
    if new_lhe_request['results']: print "%s Prepid of the new LHE request." % (new_lhe_request['prepid'])
    else: sys.exit("*** ERROR: %s: Cloning failed with msg:%s" % (ds.name,answer['message']))

    # Issue option reset on the new LHE request
    answer = mcm.option_reset(new_lhe_request['prepid'])
    if answer['results']: print "%s Issued option_reset" % new_lhe_request['prepid']
    else: sys.exit("*** ERROR: %s: Option_reset failed with msg:%s" % (ds.name,answer['message']))

  if (update_fs_requests):
    # find the fastsim request, which was automatically created when the pLHE was "chained" to the FastSim campaign
    print "%s: Searching McM for FastSim prep-id..." % ds.name
    reqs = mcm.getA('requests',query='dataset_name='+ds.name)
    fs_dict = {}
    found = False
    for r in reqs:    
      if r['member_of_campaign']=='RunIISpring15FSPremix': 
        if found:
          sys.exit("*** ERROR: %s: Found multiple FastSim requests for this dataset name" %(ds.name))
        else:
          found = True
          if r['status']=='new': fs_dict = r
          else: sys.exit("*** ERROR: %s: FastSim request is not in status new! If you really want to edit, reset it first." %(ds.name))
    if not found: sys.exit("*** ERROR: %s: FastSim request not found." %(ds.name))

    # make modifications to the dictionary
    fs_dict['total_events'] = ds.nevt_lhe*ds.match_eff
    fs_dict['generator_parameters'] = fs_gen_params
    fs_dict['generator_parameters'][0]['match_efficiency'] = ds.match_eff
    fs_dict['size_event'] = fs_size_event
    fs_dict['time_event'] = fs_time_event
    if ('qCut = 999.' not in fs_fragment): sys.exit("*** ERROR: Cannot find where to write the qCut in the generic fragment.")
    fs_dict['fragment'] = fs_fragment.replace('qCut = 999.', 'qCut = '+str(ds.qcut))

    # Update the request
    answer = mcm.updateA('requests', fs_dict)
    if answer['results']: print "%s: Updated GS request for " % fs_dict['prepid']
    else: sys.exit("*** ERROR: %s: GS request update failed with msg:%s" %(fs_dict['prepid'], answer['message']))

    # Issue option reset on the fastSim request
    answer = mcm.option_reset(fs_dict['prepid'])
    if answer['results']: print "%s Issued option_reset" % fs_dict['prepid']
    else: sys.exit("*** ERROR: %s: Option_reset failed with msg:%s" % (ds.name,answer['message']))

    # start validation in lxbatch
    prepid = fs_dict['prepid']
    cmd = "wget https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_test/"+prepid+" && "
    cmd +="mv "+prepid+" "+prepid+".sh && "
    cmd +="chmod a+x "+prepid+".sh && "
    cmd +="bsub -q 1nw -J j"+prepid[-3:len(prepid)+1]+" "+prepid+".sh"
    os.system(cmd)
