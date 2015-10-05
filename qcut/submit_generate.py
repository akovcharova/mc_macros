import os

procs = ["BJets_HT-250To500"]
# procs = ["DYJets_HT-low_mll_200to400"]
# procs = ["WJetsToLNu_HT-100to200","WJetsToLNu_HT-200to400","WJetsToLNu_HT-600toInf"]
nevents = 20000
njobs = 1
queue = "1nw"

for proc in procs:
  for j in range(0,njobs):
    rseed = 100+j
    cmd = "bsub -q " + queue + " \"generate.sh " + proc + " " + str(nevents) + " "+ str(rseed) + "\""
    print cmd
    os.system(cmd)
    