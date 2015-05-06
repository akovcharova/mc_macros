import os

procs = [
"GJets_HT-100to200",
"GJets_HT-200to400",
"GJets_HT-400to600",
"GJets_HT-40to100",
"GJets_HT-600toInf",
"WJetsToLNu_HT-1200to2500",
"WJetsToLNu_HT-2500toInf",
"WJetsToLNu_HT-600to800",
"WJetsToLNu_HT-800to1200",
"WJetsToQQ_HT-600toInf"
]


njet_max=4
flav_scheme="5"
queue = "1nw"

# qcuts = [10, 12, 14, 16, 18]
qcuts = [19]

for proc in procs:
  for qcut in qcuts:
    cmd = "bsub -q " + queue + " \"shower.sh " + " ".join([proc, str(qcut), str(njet_max), str(flav_scheme)]) + "\""
    print cmd
    os.system(cmd)