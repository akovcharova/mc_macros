#### !/usr/local/bin/bash

PROCESS=$1
QCUT=$2
NJET_MAX=$3
FLAV_SCHEME=$4

echo "Process"
echo $PROCESS

export SCRAM_ARCH=slc6_amd64_gcc481
echo $SCRAM_ARCH
echo $HOSTNAME
eval `scramv1 project CMSSW CMSSW_7_1_14`
cd CMSSW_7_1_14/src
eval `scramv1 runtime -sh`

echo "Gathering inputs"
# cp /afs/cern.ch/work/a/ana/hadronized/${PROCESS}/comb.lhe .
cp /afs/cern.ch/work/a/ana/alexis_lhes/${PROCESS}.lhe .
mkdir -p Configuration/GenProduction/python

echo \
"import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *

generator = cms.EDFilter(\"Pythia8HadronizerFilter\",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CUEP8M1SettingsBlock,
        processParameters = cms.vstring(
            'JetMatching:setMad = off',
            'JetMatching:scheme = 1',
            'JetMatching:merge = on',
            'JetMatching:jetAlgorithm = 2',
            'JetMatching:etaJetMax = 5.',
            'JetMatching:coneRadius = 1.',
            'JetMatching:slowJetPower = 1',
            'JetMatching:qCut = $QCUT.', #this is the actual merging scale                                                               
            'JetMatching:nQmatch = $FLAV_SCHEME', #4 corresponds to 4-flavour scheme (no matching of b-quarks), 5 for 5-flavour scheme           
            'JetMatching:nJetMax = $NJET_MAX', #number of partons in born matrix element for highest multiplicity                             
            'JetMatching:doShowerKt = off', #off for MLM matching, turn on for shower-kT matching                                     
        ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CUEP8M1Settings',
                                    'processParameters',
                                    )
    )
)" > Configuration/GenProduction/python/genfragment.py

eval "scramv1 build clean"
eval "scramv1 build"

echo "Fragment:"
cat genfragment.py

echo "Let's begin..."
cmsDriver.py \
  Configuration/GenProduction/python/genfragment.py \
  --mc \
  --eventcontent RAWSIM \
  --datatier GEN-SIM \
  --conditions auto:mc \
  --step GEN \
  --filein file:${PROCESS}.lhe \
  --fileout file:GEN_${PROCESS}_${QCUT}.root \
  -n 10000


echo "Hadronization finished. Cleaning..."
# cp GEN.root /afs/cern.ch/work/a/ana/hadronized/${PROCESS}/GEN_${QCUT}.root

#cleanup
cd ../../
rm -rf CMSSW_7_1_14

echo "Bye."
