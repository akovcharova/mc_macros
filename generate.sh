#### !/usr/local/bin/bash

#set up some preliminaries
export SCRAM_ARCH=slc6_amd64_gcc481
echo $SCRAM_ARCH
echo $HOSTNAME
PROCESS=$1
NEVENTS=$2
RANDOM_SEED=$3
echo "Process"
echo $PROCESS

eval `scramv1 project CMSSW CMSSW_7_1_14`
cd CMSSW_7_1_14/src
eval `scramv1 runtime -sh`

echo "Unpacking gridpack tarball..."
tar -xaf /afs/cern.ch/work/a/ana/20150328-gen/genproductions/bin/MadGraph5_aMCatNLO/${PROCESS}_tarball.tar.xz
# tar -xaf /afs/cern.ch/work/a/ana/ttjets/genproductions/bin/MadGraph5_aMCatNLO/${PROCESS}_tarball.tar.xz
# tar -xaf /afs/cern.ch/work/a/ana/wjets/genproductions/bin/MadGraph5_aMCatNLO/${PROCESS}_tarball.tar.xz

echo "Running event generation..."
./runcmsgrid.sh $NEVENTS $RANDOM_SEED 4

echo "Generation finished. Packing output..."
outhtml=process/madevent/HTML/GridRun_${RANDOM_SEED}/results.html
cp ${outhtml} /afs/cern.ch/work/a/ana/hadronized/events/results_${PROCESS}_${RANDOM_SEED}.html
cp cmsgrid_final.lhe /afs/cern.ch/work/a/ana/hadronized/events/cmsgrid_final_${PROCESS}_${RANDOM_SEED}.lhe



#cleanup
cd ../../
rm -rf CMSSW_7_1_14
