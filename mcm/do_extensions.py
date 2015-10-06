import sys
import pprint
import string
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import *

dsdict = {
# 'TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 15.,
# 'TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 10.5,
# 'TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 3.,
# 'TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 1.5,
# 'WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 30.,
# 'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 15.,
# 'WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 6.,
'WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 16.,
'WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 6.4,
# 'WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 7.25,
# 'WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 2.25,
# 'DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 7.8,
# 'DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 9.,
# 'DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 9.,
# 'DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 4.,
# 'DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 9.,
# 'DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 2.,
# 'DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 2.,
# 'DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 2.,
'ZJetsToNuNu_HT-100To200_13TeV-madgraph' : 20.,
'ZJetsToNuNu_HT-200To400_13TeV-madgraph' : 20.,
'ZJetsToNuNu_HT-400To600_13TeV-madgraph' : 9.,
'ZJetsToNuNu_HT-600ToInf_13TeV-madgraph' : 9.,
# 'QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 40.,
# 'QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 40.,
# 'QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 40.,
# 'QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 30.,
# 'QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 10.,
# 'QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 8.,
# 'QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 4.,
# 'GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 10.,
# 'GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 10.,
# 'GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 40.,
# 'GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 10.,
# 'GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8' : 10.
}

print "Connecting to McM..."
mcm = restful(dev=False)
print "done."

dotwiki = True
if dotwiki: 
  twiki = open("table.txt","w")
  twiki.write("Please chain the following requests to BOTH *RunIIWinter15GS+RunIISpring15DR74* and *RunIISummer15GS*:\n")
  twiki.write("| *row* | *prepid* | *Dataset* | *N_events* | *Comments* | *RM's comments* | *RM responsible* |\n")

for ind,dsname in enumerate(sorted(dsdict.keys())):
  print "Working on dataset", dsname
  reqs = mcm.getA('requests',query='dataset_name='+dsname)
  rgs, rlhe = {}, {}
  for r in reqs:
    if r['approval']=='none': continue
    if r['member_of_campaign']=='RunIIWinter15GS': rgs = r
    if r['member_of_campaign']=='RunIIWinter15wmLHE': rlhe = r

  if len(rgs['prepid']) < 0: sys.exit('Dataset GS request not found%s' % dsname)
  if len(rlhe['prepid']) < 0: sys.exit('Dataset LHE request not found%s' % dsname)

  gen_pars = rgs['generator_parameters'].pop()
  eff = gen_pars['match_efficiency']
  eff_err = gen_pars['match_efficiency_error']

  # find number of events needed in the wmLHE extension
  ngs_ext = dsdict[dsname]
  nlhe_ext = 1.0e6*ngs_ext/(eff-eff_err)
  # print ('{0:<35}{1:<35}{2:<10.3f}{3:<10}{4:<10.3}{5:100}'.format(rlhe['prepid'], rgs['prepid'], eff-eff_err, ngs_ext, '{0:.1f}'.format(nlhe_ext/1e6), dsname))

  rlhe['total_events'] = nlhe_ext
  answer = mcm.clone(rlhe['prepid'],rlhe)
  if len(answer)==0: sys.exit("\n !!! Failed making a clone")

  new_rlhe = mcm.getA('requests',answer['prepid'])
  new_rlhe['extension'] = 1
  answer = mcm.updateA('requests', new_rlhe)

  print ('{0:<35}{1:100}{2:<10.1f}'.format(new_rlhe['prepid'],dsname, ngs_ext))
  
  if dotwiki: 
    twiki.write("|"+"|".join([str(ind), new_rlhe['prepid'],dsname, str(ngs_ext),'','',''])+"|\n")

if dotwiki: twiki.close()
