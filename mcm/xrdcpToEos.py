import os, sys
import stat
import subprocess
import shlex

# batch1: 15927
# batch2: 15928
# batch3: 15929
# batch4: 15930

whichBatch = "Batch1"

checkAndResubmit = True

batchDict = {
    "Batch1":15927,
    "Batch2":15928,
    "Batch3":15929,
    "Batch4":15930,
}

fileList="filelist"+whichBatch+"_m1.txt"
articleId=str(batchDict[whichBatch])

eosPath = "root://eoscms//eos/cms/store/lhe/{0}/{1}"
tmpeosPath = "/afs/cern.ch/work/s/scasasso/private/SUSY_MC/mc_macros/mcm/tmpeos/cms/store/lhe/{0}/{1}"

common = "#!/bin/sh\ncd /afs/cern.ch/work/s/scasasso/private/SUSY_MC/LHE_generation/CMSSW_7_1_20_patch3/src\neval `scramv1 runtime -sh`\ncd -\n"
copyStrTempl = "xrdcp root://cmsxrootd.fnal.gov//store/user/sbein/pMSSM13TeV/LHE/"+whichBatch+"/{0} {1}\n"
checkRet = "ret_code=$?\nif [ $ret_code != 0 ]; then\n  echo \"{0}\" >> failed{1}\nfi\n\n"
endStr = "cp failed{0} /afs/cern.ch/work/s/scasasso/private/SUSY_MC/mc_macros/mcm/xrdcp_pMSSM/failedXrdCopy/\n"

def processCmd(cmd):

    args = shlex.split(cmd)
    sp = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = sp.communicate()
    if sp.returncode != 0: print out, err

    return out, err


# Count the total
totLines = 0
with open( fileList, "rb ") as inFile: totLines = inFile.readlines()

if totLines == 0:
    print "Something wrong!"
    sys.exit()


counter = 0
counterSub = 0
copyStr = ""
outFileRes = open( "resubmit.sh","wb" )
for l in open( fileList, "rb "):

    counter+=1    

    fileName = l.strip()
    eosPathFile = eosPath.format(articleId,fileName)
    tmpeosPathFile = tmpeosPath.format(articleId,fileName)

    xrdCmdStr = copyStrTempl.format(fileName,eosPathFile).strip()
    
    if checkAndResubmit:        
        # print tmpeosPathFile,os.path.getsize(tmpeosPathFile)/1000000.
        if not os.path.exists(tmpeosPathFile) or os.path.getsize(tmpeosPathFile)/1000000. < 1.: outFileRes.write(xrdCmdStr+"\n")

    else:
            
        copyStr += xrdCmdStr
        copyStr += "\n"+checkRet.format(xrdCmdStr,counterSub)

        if counter%20==0 or counter==totLines:        

            with open("submit{0}.sh".format(counterSub),"wb") as f:
                f.write(common)
                f.write(copyStr)
                f.write(endStr.format(counterSub))
            st = os.stat("submit{0}.sh".format(counterSub))
            os.chmod("submit{0}.sh".format(counterSub), st.st_mode | stat.S_IEXEC)
            out, err = processCmd("bsub -q 1nh submit{0}.sh".format(counterSub))
            print out, err
            counterSub += 1
            copyStr = ""
        


outFileRes.close()
    
