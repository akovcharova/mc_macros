#! /usr/bin/env python

#---------------------------------------------------------------------------------------------------------------------
#   Script to upload lhe files to official EOS space from the original directory where we store the SMS scans:
#           /eos/cms/store/group/phys_susy/LHE/13TeV/
#   Why use it:
#      1. Copying many files at once makes it more likely that files get corrupted on tranfer
#      2. When uploading a lot of files, the official script first performs some checks on *all* of them and 
#         then uploads them which means that if it times out (which I've seen many times) or you loose connection 
#         you have lots of time wasted and 0 file uploaded
#   What it does:
#      Reads the list of lhe files to be uploaded to EOS from the orginal directory and copies 3 of them at a 
#      tiem to EOS given a particular model, dataset and an mcdbid. It would only try to upload files that are 
#      not already on EOS so it can be used at any time given the dataset already has an mcdb id assigned. The 
#      mcdbid for thw dataset must be in the dictionary "id_dict" below. If it is not just upload one file 
#      using the usual tool: 
#          cmsLHEtoEOSManager.py -n -f file_path_to_one_lhe_of_this_dataset
#      This will assign a new mcdb id which you can add to the dictionary "id_dict" below.
#   How to use it:
#      0. Get this script:
#           wget https://raw.githubusercontent.com/trandbea/mc_macros/master/mcm/cpeos.py
#      1. Set up some CMSSW release
#      2. Mount eos into some directory, e.g. tmpeos 
#           eosmount tmpeos
#      3. Make script executable
#           chmod u+x cpeos.py
#      4. Execute sctipt for a particular dataset, model and mcdb id, where 
#         "model" = directory where the model is stored inside /eos/cms/store/group/phys_susy/LHE/13TeV/, 
#                   e.g. T2tt_v2 or T5qqqqVV
#         "dataset" = the subdirectory for the particular set of mass points e.g. T5qqqqVV_ordered_600_700
#         Then to execute, e.g.:
#           ./cpeos.py -m T5qqqqVV -d T5qqqqVV_ordered_600_700 -e <directory_where_eos_was_mounted>
#---------------------------------------------------------------------------------------------------------------------

import os, glob, sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d","--dataset")
parser.add_argument("-m","--model") # this must be the name of the directory inside /eos/cms/store/group/phys_susy/LHE/13TeV/
parser.add_argument("-e","--eosdir")
args = parser.parse_args()

id_dict = {
  # --- Vince
  'T5qqqqVV_ordered_1000_1100': 15414,
  'T5qqqqVV_ordered_700_800': 15415,
  'T5qqqqVV_ordered_800_1000': 15416,
  'T5qqqqVV_ordered_1400_1600': 15417,
  'T5qqqqVV_ordered_1600_1800': 15418,
  # --- Ana
  # 'T5qqqqVV_ordered_600_700': 15419,
  # 'T5qqqqVV_ordered_1100_1200': 15420,
  # 'T5qqqqVV_ordered_1300_1400': 15421,
  # 'T5qqqqVV_ordered_1800_inf': 15422,
  # 'T5qqqqVV_ordered_1200_1300': 15423
}

if args.dataset not in id_dict.keys():
  print "Don't know mcdb id for", args.dataset
else:
  # put all the lhe file paths from this dataset in a txt file
  fnm = args.dataset + ".txt"
  # print os.getcwd()+"/"+args.eosdir+"/cms/store/group/phys_susy/LHE/13TeV/"+args.model+"/"+args.dataset+"/*.lhe.xz"
  lhelist = glob.glob(os.getcwd()+"/"+args.eosdir+"/cms/store/group/phys_susy/LHE/13TeV/"+args.model+"/"+args.dataset+"/*.lhe.xz")
  with open(fnm,'w') as fl:
    for i in lhelist:
      fl.write(i+"\n")

  while os.stat(fnm).st_size != 0:
    # see what is already uploaded
    eos_files = set([i.split("/").pop() for i in glob.glob(args.eosdir+"/cms/store/lhe/"+str(id_dict[args.dataset])+"/*")])
    # save the names of the first 3 files that are not already on EOS and copy the rest to a new file
    to_upload = []
    old_file = open(fnm)
    new_file = open("temp_" + fnm,"w")    
    ilhe = 0
    for line in old_file:
      lhe = line.split("/").pop().strip()
      if (lhe.split("/").pop() in eos_files): 
        continue
      if (ilhe<3):
        to_upload.append(line.strip())
      else:
        new_file.write(line)
      ilhe = ilhe + 1
    old_file.close()
    new_file.close()
    # replace the old file with the new file in which the 3 lhes we just uploaded have been removed
    os.rename("temp_"+fnm, fnm)

    cmd = "cmsLHEtoEOSManager.py -u " + str(id_dict[args.dataset]) +" -f " + ",".join(to_upload)
    print cmd
    os.system(cmd)
