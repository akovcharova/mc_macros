/*

  Macro to make DJR plots. 
  Should run on EDM root file with GEN information, using FWLite. 

  Written by: Josh Bendavid
  Modified slighlty by: Nadja Strobbe
  Modified 05/2015 - Add ability to combine multiple files acc. to xsec. ~ Ana Ovcharova 

*/

#include <iostream>
#include <fstream>
#include <string>
#include <vector>

#include "TFile.h"
#include "TTree.h"
#include "TH1D.h"
#include "TCanvas.h"
#include "TCut.h"
#include "TROOT.h"
#include "TChain.h"

using namespace std;

double deltaPhiVal(double phi1, double phi2) {
 
  double dphival = phi2 - phi1;
  while (dphival>=M_PI) dphival -= 2.*M_PI;
  while (dphival<-M_PI) dphival += 2.*M_PI;
  
  return dphival;
  
}

double deltaRVal(double eta1,double phi1,double eta2,double phi2) {
 
  double detaval = eta2-eta1;
  double dphival = deltaPhiVal(phi1,phi2);
  return sqrt(detaval*detaval + dphival*dphival);
  
}

void makeplot(const char *name, vector<TChain*> &trees, vector<double> &xsecs, TCut weight, const char *drawstring, const char *xlabel, int nbins, double xlow, double xhigh) {
  
  //this is for LO with MLM
  TCut mult0 = "GenEvent.nMEPartons()==0";
  TCut mult1 = "GenEvent.nMEPartons()==1";
  TCut mult2 = "GenEvent.nMEPartons()==2";
  TCut mult3 = "GenEvent.nMEPartons()==3";

  TH1D* hall = new TH1D(TString::Format("hall_%s",name),"",nbins,xlow,xhigh);
  TH1D* hmult0 = new TH1D(TString::Format("hmult0_%s",name),"",nbins,xlow,xhigh);
  TH1D* hmult1 = new TH1D(TString::Format("hmult1_%s",name),"",nbins,xlow,xhigh);
  TH1D* hmult2 = new TH1D(TString::Format("hmult2_%s",name),"",nbins,xlow,xhigh);
  TH1D* hmult3 = new TH1D(TString::Format("hmult3_%s",name),"",nbins,xlow,xhigh);

  for (unsigned i(0); i<trees.size(); i++){
    TH1D* tmp_hall = new TH1D(TString::Format("hall_%s_%i",name,i),"",nbins,xlow,xhigh);
    TH1D* tmp_hmult0 = new TH1D(TString::Format("hmult0_%s_%i",name,i),"",nbins,xlow,xhigh);
    TH1D* tmp_hmult1 = new TH1D(TString::Format("hmult1_%s_%i",name,i),"",nbins,xlow,xhigh);
    TH1D* tmp_hmult2 = new TH1D(TString::Format("hmult2_%s_%i",name,i),"",nbins,xlow,xhigh);
    TH1D* tmp_hmult3 = new TH1D(TString::Format("hmult3_%s_%i",name,i),"",nbins,xlow,xhigh);
    
    trees[i]->Draw(TString::Format("%s>>%s",drawstring,tmp_hall->GetName()),weight,"goff");
    trees[i]->Draw(TString::Format("%s>>%s",drawstring,tmp_hmult0->GetName()),weight*mult0,"goff");
    trees[i]->Draw(TString::Format("%s>>%s",drawstring,tmp_hmult1->GetName()),weight*mult1,"goff");
    trees[i]->Draw(TString::Format("%s>>%s",drawstring,tmp_hmult2->GetName()),weight*mult2,"goff");
    trees[i]->Draw(TString::Format("%s>>%s",drawstring,tmp_hmult3->GetName()),weight*mult3,"goff");

    double tot = tmp_hall->Integral(0,tmp_hall->GetNbinsX());
    if (tot>0) {
      hall->Add(tmp_hall, xsecs[i]/tot);
      hmult0->Add(tmp_hmult0, xsecs[i]/tot);
      hmult1->Add(tmp_hmult1, xsecs[i]/tot);
      hmult2->Add(tmp_hmult2, xsecs[i]/tot);
      hmult3->Add(tmp_hmult3, xsecs[i]/tot);
    }
  }

  hmult0->SetLineColor(kBlue);
  hmult1->SetLineColor(kRed);
  hmult2->SetLineColor(kMagenta);
  hmult3->SetLineColor(kGreen+1);

  hall->GetXaxis()->SetTitle(xlabel);
  
  TCanvas* c = new TCanvas(name,name);
  c->cd();
  hall->SetLineWidth(2);
  hall->Draw("EHIST");
  hmult0->SetLineWidth(2);
  hmult0->Draw("EHISTSAME");
  hmult1->SetLineWidth(2);
  hmult1->Draw("EHISTSAME");
  hmult2->SetLineWidth(2);
  hmult2->Draw("EHISTSAME");
  hmult3->SetLineWidth(2);
  hmult3->Draw("EHISTSAME");
  c->SetLogy();
  c->SaveAs(TString::Format("%s.pdf",name));
}

void plotdjr_comb(TString filenames, const char* outputbase) {
 
  TH1::SetDefaultSumw2();

  vector<TString> fnames;
  size_t pos(0);
  while (pos!=std::string::npos) { 
    pos = filenames.First(",");
    if (pos==std::string::npos) fnames.push_back(filenames(0,filenames.Length()));
    else fnames.push_back(filenames(0,pos));
    filenames = filenames(pos+1, filenames.Length()-pos-1);
  } 

  vector<double> xsecs;
  vector<TChain*> trees;
  for (unsigned i(0); i< fnames.size(); i++){
    cout<<"Including file:"<<fnames[i]<<"."<<endl;
    trees.push_back(new TChain("Events"));
    trees[i]->Add(fnames[i]);
    trees[i]->SetAlias("GenEvent","GenEventInfoProduct_generator__GEN.obj");

    TChain xsec_tree("Runs");
    xsec_tree.Add(fnames[i]);
    xsec_tree.Draw("GenRunInfoProduct_generator__GEN.obj.internalXSec_.value_");
    TH1D *htemp = (TH1D*)gPad->GetPrimitive("htemp");
    double xsec = htemp->GetMean();
    cout<<"Found xsec = "<<xsec<<endl;
    xsecs.push_back(xsec);
    if (htemp->GetRMS()>0) cout<<"ERROR: File contains Runs with different cross-sections"<<endl;
  }

  TCut weight = "GenEvent.weight()";
  int nbins = 50.;
  double djrmin = -0.5;
  double djrmax = 4.;
  
  
  makeplot(TString::Format("%s_%s",outputbase,"djr0"),trees,xsecs,weight,"log10(GenEvent.DJRValues_[0])","DJR 0->1",nbins,djrmin,djrmax);
  makeplot(TString::Format("%s_%s",outputbase,"djr1"),trees,xsecs,weight,"log10(GenEvent.DJRValues_[1])","DJR 1->2",nbins,djrmin,djrmax);
  makeplot(TString::Format("%s_%s",outputbase,"djr2"),trees,xsecs,weight,"log10(GenEvent.DJRValues_[2])","DJR 2->3",nbins,djrmin,djrmax);
  makeplot(TString::Format("%s_%s",outputbase,"djr3"),trees,xsecs,weight,"log10(GenEvent.DJRValues_[3])","DJR 3->4",nbins,djrmin,djrmax);
  return;  
}

void qcut_scan() {
  TString set = "DYJets_HT_LO";
  TString proc1 = "DYJets_HT-incl_low_mll";
  TString proc2 = "DYJets_HT-incl";
  uint qcut_min = 10;
  uint qcut_max = 30;

  ofstream f;
  f.open("plots_comb.tex");
  f<<"\\begin{frame} \n";
  f<<"\\begin{center} \n";
  f<<set.ReplaceAll("_"," ")<<" \n";
  f<<"\\end{center} \n";
  f<<"\\end{frame} \n";
  for (uint iqcut=qcut_min; iqcut<qcut_max+1; iqcut++){
    gROOT->Reset();
    TString qcut = TString::Format("%i",iqcut);
    cout<<qcut<<endl;
    TString fout = set+"_"+qcut;
    plotdjr_comb("../GENfiles/GEN_"+proc1+"_"+qcut+".root,../GENfiles/GEN_"+proc2+"_"+qcut+".root", fout);

    f<<"\\begin{frame} \n";
    f<<"\\frametitle{"+set.ReplaceAll("_"," ") +" qCut = "+ qcut+"} \n";
    f<<"\\includegraphics[width=0.5\\textwidth]{"+set+"_"+qcut+"_djr0.pdf} \n";
    f<<"\\includegraphics[width=0.5\\textwidth]{"+set+"_"+qcut+"_djr1.pdf}\\\\ \n";
    f<<"\\includegraphics[width=0.5\\textwidth]{"+set+"_"+qcut+"_djr2.pdf} \n";
    f<<"\\includegraphics[width=0.5\\textwidth]{"+set+"_"+qcut+"_djr3.pdf}\\\\ \n";
    f<<"\\end{frame} \n";
  }
  f.close();
}