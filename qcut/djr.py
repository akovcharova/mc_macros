import os
from ROOT import *

gSystem.Load("libFWCoreFWLite.so")
AutoLibraryLoader.enable()
gSystem.Load("libDataFormatsFWLite.so")
gSystem.Load("libDataFormatsPatCandidates.so")
gROOT.LoadMacro("plotdjr.C")

gROOT.SetBatch(kTRUE)

infile_path = os.getcwd()

procs = []
procs.append("tt01j_5f_ckm_LO_MLM")
procs.append("tt012j_5f_ckm_LO_MLM")
qcuts = [20+2*x for x in range(1,31)]


f = open("plots.tex",'w')
for proc in procs:
  print "Plotting", proc
  f.write("\\begin{frame} \n")
  f.write("\\begin{center} \n")
  f.write(proc.replace("_"," ") +" \n")
  f.write("\\end{center} \n")
  f.write("\\end{frame} \n")
  for iqcut in qcuts:
    qcut = str(iqcut)
    fin = infile_path+"/GEN_"+proc+"_"+qcut+".root"
    fout = proc+"_"+qcut
    plotdjr(fin, fout)

    f.write("\\begin{frame} \n")
    f.write("\\frametitle{"+proc.replace("_"," ") +" qCut = "+ qcut+"} \n")
    f.write("\\includegraphics[width=0.5\\textwidth]{"+proc+"_"+qcut+"_djr0.pdf} \n")
    f.write("\\includegraphics[width=0.5\\textwidth]{"+proc+"_"+qcut+"_djr1.pdf}\\\\ \n")
    f.write("\\includegraphics[width=0.5\\textwidth]{"+proc+"_"+qcut+"_djr2.pdf} \n")
    f.write("\\includegraphics[width=0.5\\textwidth]{"+proc+"_"+qcut+"_djr3.pdf}\\\\ \n")
    f.write("\\end{frame} \n")

f.close()
