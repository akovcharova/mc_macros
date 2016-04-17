#### !/usr/local/bin/bash

PROCESS=$1
NEVENTS=$2
RANDOM_SEED=$3
QCUT=$4
NJET_MAX=$5
FLAV_SCHEME=$6

echo "Process"
echo $PROCESS


WORKDIR=$(pwd)
echo "Working directory: "
echo $WORKDIR

echo "Output directory set to: "
OUTDIR='/hadoop/cms/store/user/ana/wjets_proc'
echo $OUTDIR

source /code/osgcode/cmssoft/cmsset_default.sh  
export SCRAM_ARCH=slc6_amd64_gcc481
echo $SCRAM_ARCH
echo $HOSTNAME
echo "Setting up a CMSSW release..."
eval `scramv1 project CMSSW CMSSW_7_1_14`
cd CMSSW_7_1_14/src
eval `scramv1 runtime -sh`


echo "Prepare fragment..."
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
cat Configuration/GenProduction/python/genfragment.py

echo "-----------> Let's begin...EVENT GENERATION"

echo "Unpacking gridpack tarball..."
tar -xaf $WORKDIR/${PROCESS}_tarball.tar.xz                                                    

echo "Running event generation..."
./runcmsgrid.sh $NEVENTS $RANDOM_SEED $(getconf _NPROCESSORS_ONLN)

echo "Generation finished. Copy output..."
lcg-cp -b -D srmv2 --vo cms -t 2400 --verbose file:cmsgrid_final.lhe srm://bsrm-3.t2.ucsd.edu:8443/srm/v2/server?SFN=${OUTDIR}/${PROCESS}_${RANDOM_SEED}.lhe

#             SHOWER
#--------------------------------
GENFILE='GEN_'${PROCESS}'_'${QCUT}'_'${RANDOM_SEED}'.root'

echo "--------------> Let's begin... SHOWER"
cmsDriver.py \
  Configuration/GenProduction/python/genfragment.py \
  --mc \
  --eventcontent RAWSIM \
  --datatier GEN-SIM \
  --conditions auto:mc \
  --step GEN \
  --filein file:cmsgrid_final.lhe \
  --fileout file:${GENFILE} \
  -n -1


echo "Hadronization finished. Copy output..."
lcg-cp -b -D srmv2 --vo cms -t 2400 --verbose file:`pwd`/${GENFILE} srm://bsrm-3.t2.ucsd.edu:8443/srm/v2/server?SFN=${OUTDIR}/${GENFILE}

echo "ls in cmssw src dir"
ls

#cleanup
cd $WORKDIR
echo "ls in workdir"
ls
rm -rf CMSSW_7_1_14

echo "Bye."
