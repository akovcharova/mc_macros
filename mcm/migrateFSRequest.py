#!/usr/bin/env python

import sys
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import *
import time

# This will be written in the "submission_details" key
author_email = "stefano.casasso@cern.ch"
author_username = "scasasso"
author_name = "Stefano Casasso"

# Connect to McM
mcm = restful(dev=True) 

# Prepids of the ref and the new FS request (this is just a test, in the proper script you will get the ref from the dataset name)
ref_prepid = "SUS-RunIISpring15FSPremix-00066"
new_prepid = "SUS-RunIISpring15FSPremix-00355"

# Get ref request
ref_fs_dict = mcm.getA('requests',ref_prepid)

# Get the new request
new_fs_dict = mcm.getA('requests',new_prepid)

# Update the new FS request
new_fs_dict["tags"] = ["74Xcopy"]
new_fs_dict["total_events"] = ref_fs_dict["total_events"]
new_fs_dict["mcdb_id"] = ref_fs_dict["mcdb_id"]
new_fs_dict["time_event"] = ref_fs_dict["time_event"]
new_fs_dict["size_event"] = ref_fs_dict["size_event"]
genPars = ref_fs_dict["generator_parameters"]

fs_sub_details = {
    "author_email": author_email, 
    "submission_date": time.strftime("%Y-%m-%d-%H-%M", time.gmtime()),
    "author_username": author_username, 
    "author_name": author_name
    }

genPars[0]["submission_details"] = fs_sub_details
new_fs_dict["generator_parameters"] = genPars

topMassStr = "'6:m0 = 172.5', # use this as top mass"
fragment = str(ref_fs_dict["fragment"])
lines = fragment.split("\n")
index = -1
for i,line in enumerate(lines):
    if "JetMatching:doShowerKt =" in line: 
        index = i
        break

newLines = lines[:index+1] + [topMassStr] + lines[index+1:]
newFragment = "\n".join(newLines)
new_fs_dict["fragment"] = newFragment


# Update request
mcm.updateA("requests",new_fs_dict)
