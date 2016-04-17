#!/usr/bin/env python
import subprocess
import shlex
import shutil
import os, sys
import glob
import optparse



def processCmd(cmd):

    args = shlex.split(cmd)
    sp = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = sp.communicate()
    if sp.returncode != 0: print out, err

    return out, err


def parse_args():
    parser = optparse.OptionParser()
    parser.add_option('-i','--inDir', default=None, help="Input directory with mlfit.root files.")
    parser.add_option('--zip',action="store_true", default=False, help = 'Use this if lhe are zipped.')
    parser.add_option('-o','--outReport',default = "countLHEs.txt",help = "Output file with report.")

    options,args = parser.parse_args()

    if not options.inDir or not os.path.exists(options.inDir):
        raise RuntimeError, "You must specify an existing input directory {0}".format(options.inDir)

    return options 



if __name__ == "__main__":

    opt = parse_args()

    lheList = glob.glob(os.path.join(opt.inDir,"*.lhe*"))

    outFile = open(opt.outReport,"wb")
    totCounter = 0
    for lhe in lheList:
        print lhe
        if opt.zip: out, err = processCmd("xzgrep -c \"</event>\" {0}".format(lhe))
        else: out, err = processCmd("grep -c \"</event>\" {0}".format(lhe))
        nEvts = int(out.strip())
        totCounter += nEvts
        outFile.write("File {0} has {1} events\n".format(lhe,nEvts))

    outFile.write("\n**************\nDirectory {0} contains {1} events\n".format(opt.inDir,totCounter))

    outFile.close()

        




