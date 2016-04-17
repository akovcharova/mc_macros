import os
import time
procs = []
#procs.append("BBJets_HT-250To500")                                                                                                                             
#procs.append("BBJets_HT-500To1000")                                                                                                                            
#procs.append("BBJets_HT-1000ToInf")                                                                                                                            
#procs.append("BBJets_HT-0ToInf")                                                                                                                               
#procs.append("WJetsToLNu_HT-100to200_pdfwgt")                                                                                                                  
# procs.append("WJetsToLNu_HT-0toInf_pdfwgt")
# procs.append("WJetsToLNu_HT-100toInf_old")
# procs.append("DYJets_012j_LO_MLM-incl")
procs.append("DYJets_HT200_012j_LO_MLM")

nevents = 10000
njobs = 100
qcut = str(19)
njet_max = str(2)
flav_scheme = str(5)

for proc in procs:
  for j in range(0,njobs):
    seed = 300+j
    # if seed in good_list: continue
    rseed = str(500+j)
    subfile = "genshr_"+proc +"_"+rseed+".cmd"
    f = open(subfile,"w")
    f.write("Universe = grid\n")
    f.write("Grid_Resource = condor cmssubmit-r1.t2.ucsd.edu glidein-collector.t2.ucsd.edu\n")
    f.write("x509userproxy=/tmp/x509up_u31582\n")
    f.write("+DESIRED_Sites=\"T2_US_UCSD\"\n")
    f.write("Executable = /home/users/ana/generated/genshr.sh\n")
    f.write("arguments =  "+' '.join([proc, str(nevents), rseed, qcut, njet_max, flav_scheme])+"\n")
    f.write("Transfer_Executable = True\n")
    f.write("should_transfer_files = YES\n")
    f.write("transfer_input_files = /home/users/ana/gridpacks/"+proc+"_tarball.tar.xz,../babymaker.tar.xz\n")
    # everything in the base directory on the execute machine gets transfered so no need to specify files, unless I want only particular ones
    # f.write("transfer_Output_files = GEN_"+proc+"_"+qcut+".root\n")
    # f.write("WhenToTransferOutput  = ON_EXIT\n")
    f.write("Notification = Never\n")
    f.write("Log=gen_"+proc+"_"+rseed+".log.$(Cluster).$(Process)\n")
    f.write("output=gen_"+proc+"_"+rseed+".out.$(Cluster).$(Process)\n")
    f.write("error=gen_"+proc+"_"+rseed+".err.$(Cluster).$(Process)\n")
    f.write("queue 1\n")
    f.close()

    cmd = "condor_submit " + subfile
    print cmd
    os.system(cmd)
