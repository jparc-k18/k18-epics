#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sstream>
#include <iostream>
#include <iomanip>
#include <fstream>
#include "TFile.h"
#include <TH1.h>
#include <TH2.h>
#include <TGraph.h>
#include <TPad.h>
#include <TText.h>
#include <TTree.h>
#include <TLine.h>
#include <TROOT.h>
#include <TApplication.h>
#include <TCanvas.h>
#include <TStyle.h>

//#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <string.h>
//#include <unistd.h>

void sigint_handler(int sig);
volatile int stop_flag=0; 

int main()
{

  int cycle = 60; // 120 -> 2min. & 48h ->1440points

  signal(SIGINT, sigint_handler);

  double temp[10][1440];
  for(int i=0;i<10;i++){
    for(int j=0;j<1440;j++){
      temp[i][j] = 0;
    }
  }
  double data_temp[10];
  std::stringstream oss1;

  ///////////////////
  // Make histgram //
  ///////////////////
  gROOT->SetBatch(1);  // Don't use GUI
  TApplication *theApp = new TApplication("App",0,0);  // Use GUI (ROOT)
  gStyle->SetOptStat(0);

  TGraph *g3[10];
  for(int n=0;n<10;n++){
    g3[n] = new TGraph();
    g3[n]->SetPoint(0,0,0);
  }
  g3[0]->SetLineColor(1);
  g3[1]->SetLineColor(2);
  g3[2]->SetLineColor(3);
  g3[3]->SetLineColor(4);
  g3[4]->SetLineColor(1);
  g3[5]->SetLineColor(2);
  g3[6]->SetLineColor(3);
  g3[7]->SetLineColor(4);
  g3[8]->SetLineColor(1);
  g3[9]->SetLineColor(3);

  //g3[0]->SetLineWidth(3);
  //g3[4]->SetLineWidth(3);

  TCanvas *c1 = new TCanvas("c1","ESS Monitor",1000,1200);

  TPad *pad1 = new TPad("name", "title",0.0, 0.66, 0.82, 0.99, 0, 0, 0);
  pad1->Draw();
  pad1->SetNumber(1);
  TPad *pad2 = new TPad("name", "title",0.78, 0.66, 0.99, 0.99, 0, 0, 0);
  pad2->Draw();
  pad2->SetNumber(2);

  TPad *pad3 = new TPad("name", "title",0.0, 0.33, 0.82, 0.66, 0, 0, 0);
  pad3->Draw();
  pad3->SetNumber(3);
  TPad *pad4 = new TPad("name", "title",0.78, 0.33, 0.99, 0.66, 0, 0, 0);
  pad4->Draw();
  pad4->SetNumber(4);

  TPad *pad5 = new TPad("name", "title",0.0, 0.01, 0.82, 0.33, 0, 0, 0);
  pad5->Draw();
  pad5->SetNumber(5);
  TPad *pad6 = new TPad("name", "title",0.78, 0.01, 0.99, 0.33, 0, 0, 0);
  pad6->Draw();
  pad6->SetNumber(6);

  c1->GetPad(0)->SetFillColor(kWhite);
  c1->GetPad(0)->SetFrameLineColor(kBlack);


  c1->cd(1);
  c1->GetPad(1)->SetGridy(1);
  TH1F *h1 = new TH1F("","Voltage [kV]",100,-24,0);
  h1->GetYaxis()->SetRangeUser(0,270);
  h1->GetXaxis()->SetTitle("Time [h]");
  h1->GetYaxis()->SetTitle("Voltage [kV]");
  h1->GetXaxis()->SetNdivisions(4,6,0,0);
  h1->Draw();

  c1->GetPad(1)->SetFillColor(kWhite);
  c1->GetPad(1)->SetFrameLineColor(kBlack);
  c1->GetPad(1)->SetGridx(1);
  for(int i=0;i<4;i++){
    g3[i]->Draw("samel");
  }

  c1->cd(2);
  char text_v1[100];
  sprintf(text_v1,"ESS1 pos: N/C");
  TText *tv1 = new TText(0.0,0.85,text_v1);
  tv1->SetNDC(1);
  tv1->SetTextSize(0.09);
  tv1->SetTextColor(1);
  tv1->Draw();
  char text_v2[100];
  sprintf(text_v2,"ESS1 neg: N/C");
  TText *tv2 = new TText(0.0,0.75,text_v2);
  tv2->SetNDC(1);
  tv2->SetTextSize(0.09);
  tv2->SetTextColor(2);
  tv2->Draw();
  char text_v3[100];
  sprintf(text_v3,"ESS2 pos: N/C");
  TText *tv3 = new TText(0.0,0.65,text_v3);
  tv3->SetNDC(1);
  tv3->SetTextSize(0.09);
  tv3->SetTextColor(3);
  tv3->Draw();
  char text_v4[100];
  sprintf(text_v4,"ESS2 neg: N/C");
  TText *tv4 = new TText(0.0,0.55,text_v4);
  tv4->SetNDC(1);
  tv4->SetTextSize(0.09);
  tv4->SetTextColor(4);
  tv4->Draw();
 


  c1->cd(3);
  c1->GetPad(3)->SetGridy(1);
  TH1F *h2 = new TH1F("","Current [uA]",100,-24,0);
  h2->GetYaxis()->SetRangeUser(0,150);
  h2->GetXaxis()->SetTitle("Time [h]");
  h2->GetYaxis()->SetTitle("Current [uA]");
  h2->GetXaxis()->SetNdivisions(4,6,0,0);
  h2->Draw();

  c1->GetPad(3)->SetFillColor(kWhite);
  c1->GetPad(3)->SetFrameLineColor(kBlack);
  c1->GetPad(3)->SetGridx(1);
  for(int i=0;i<4;i++){
    g3[i+4]->Draw("samel");
  }

  c1->cd(4);
  char text_c1[100];
  sprintf(text_c1,"ESS1 pos: N/C");
  TText *tc1 = new TText(0.0,0.85,text_c1);
  tc1->SetNDC(1);
  tc1->SetTextSize(0.09);
  tc1->SetTextColor(1);
  tc1->Draw();
  char text_c2[100];
  sprintf(text_c2,"ESS1 neg: N/C");
  TText *tc2 = new TText(0.0,0.75,text_c2);
  tc2->SetNDC(1);
  tc2->SetTextSize(0.09);
  tc2->SetTextColor(2);
  tc2->Draw();
  char text_c3[100];
  sprintf(text_c3,"ESS2 pos: N/C");
  TText *tc3 = new TText(0.0,0.65,text_c3);
  tc3->SetNDC(1);
  tc3->SetTextSize(0.09);
  tc3->SetTextColor(3);
  tc3->Draw();
  char text_c4[100];
  sprintf(text_c4,"ESS2 neg: N/C");
  TText *tc4 = new TText(0.0,0.55,text_c4);
  tc4->SetNDC(1);
  tc4->SetTextSize(0.09);
  tc4->SetTextColor(4);
  tc4->Draw();


  c1->cd(5);
  c1->GetPad(5)->SetGridy(1);
  TH1F *h3 = new TH1F("","Vacuum [Pa]",100,-24,0);
  h3->GetYaxis()->SetRangeUser(1e-5,1e+1);
  h3->GetXaxis()->SetTitle("Time [h]");
  h3->GetYaxis()->SetTitle("Vacuum [Pa]");
  h3->GetXaxis()->SetNdivisions(4,6,0,0);
  h3->Draw();

  c1->GetPad(5)->SetFillColor(kWhite);
  c1->GetPad(5)->SetFrameLineColor(kBlack);
  c1->GetPad(5)->SetGridx(1);
  c1->GetPad(5)->SetLogy(1);
  for(int i=0;i<2;i++){
    g3[i+8]->Draw("samel");
  }

  c1->cd(6);
  char text_vac1[100];
  sprintf(text_vac1,"ESS1: N/C");
  TText *tvac1 = new TText(0.0,0.85,text_vac1);
  tvac1->SetNDC(1);
  tvac1->SetTextSize(0.09);
  tvac1->SetTextColor(1);
  tvac1->Draw();
  char text_vac2[100];
  sprintf(text_vac2,"ESS2: N/C");
  TText *tvac2 = new TText(0.0,0.75,text_vac2);
  tvac2->SetNDC(1);
  tvac2->SetTextSize(0.09);
  tvac2->SetTextColor(3);
  tvac2->Draw();


  char text_ttime1[100];
  sprintf(text_ttime1,"Last update :");
  TText *ttime1 = new TText(0.0,0.12,text_ttime1);
  ttime1->SetNDC(1);
  ttime1->SetTextSize(0.07);
  ttime1->SetTextColor(1);
  ttime1->Draw();
  char text_ttime2[100];
  sprintf(text_ttime2," ");
  TText *ttime2 = new TText(0.05,0.05,text_ttime2);
  ttime2->SetNDC(1);
  ttime2->SetTextSize(0.07);
  ttime2->SetTextColor(1);
  ttime2->Draw();

  c1->Update();

  std::cout << std::fixed << std::setprecision(1);



  //////////
  // loop //
  //////////
  while(stop_flag==0){


    time_t t = time(NULL);
    std::cout << std::endl << "updated: " << ctime(&t);


    // read result.txt
    std::ifstream fin("../ReadValues.txt");
    fin >> data_temp[0]
	>> data_temp[1]
	>> data_temp[2]
	>> data_temp[3]
	>> data_temp[4]
	>> data_temp[5]
	>> data_temp[6]
	>> data_temp[7]
	>> data_temp[8]
	>> data_temp[9];
    fin.close();

    for(int n=0;n<1439;n++){
      for(int i=0;i<10;i++){
	temp[i][n] = temp[i][n+1];
      }
    }

    for(int i=0;i<10;i++){
      temp[i][1439] = data_temp[i];
      g3[i]->Set(0);
    }

    for(int n=0;n<1440;n++){
      for(int i=0;i<10;i++){
	g3[i]->SetPoint(n,n*(1./60.)-24,temp[i][n]);
      }
    }
    
    c1->cd(2);
    sprintf(text_v1,"ESS1 pos: %4.1f [kV]",data_temp[0]);
    tv1->SetText(0.0,0.85,text_v1);
    sprintf(text_v2,"ESS1 neg: %4.1f [kV]",data_temp[1]);
    tv2->SetText(0.0,0.75,text_v2);
    sprintf(text_v3,"ESS2 pos: %4.1f [kV]",data_temp[2]);
    tv3->SetText(0.0,0.65,text_v3);
    sprintf(text_v4,"ESS2 neg: %4.1f [kV]",data_temp[3]);
    tv4->SetText(0.0,0.55,text_v4);

    c1->cd(4);
    sprintf(text_c1,"ESS1 pos: %4.1f [uA]",data_temp[4]);
    tc1->SetText(0.0,0.85,text_c1);
    sprintf(text_c2,"ESS1 neg: %4.1f [uA]",data_temp[5]);
    tc2->SetText(0.0,0.75,text_c2);
    sprintf(text_c3,"ESS2 pos: %4.1f [uA]",data_temp[6]);
    tc3->SetText(0.0,0.65,text_c3);
    sprintf(text_c4,"ESS2 neg: %4.1f [uA]",data_temp[7]);
    tc4->SetText(0.0,0.55,text_c4);

    c1->cd(6);
    sprintf(text_vac1,"ESS1: %4.1e [Pa]",data_temp[8]);
    tvac1->SetText(0.0,0.85,text_vac1);
    sprintf(text_vac2,"ESS2: %4.1e [Pa]",data_temp[9]);
    tvac2->SetText(0.0,0.75,text_vac2);

    t = time(NULL);
    //ttime2->SetText(0.05,0.08,ctime(&t));
    char c_time[30];
    strftime(c_time, sizeof(c_time), "%Y/%m/%d %H:%M:%S", localtime(&t));
    ttime2->SetText(0.15,0.08,c_time);


    c1->GetPad(1)->Modified();
    c1->GetPad(3)->Modified();
    c1->GetPad(5)->Modified();
    c1->Modified();
    c1->Update();
    c1->Print("EssHistry.gif");

    // output
    std::ofstream fout("Log.txt",std::ios::app);
    fout << data_temp[0] << "\t";
    fout << data_temp[1] << "\t";
    fout << data_temp[2] << "\t";
    fout << data_temp[3] << "\t";
    fout << data_temp[4] << "\t";
    fout << data_temp[5] << "\t";
    fout << data_temp[6] << "\t";
    fout << data_temp[7] << "\t";
    fout << data_temp[8] << "\t";
    fout << data_temp[9] << "\t";
    fout << ctime(&t);
 
    sleep(1);
    while( time(NULL) % cycle != 0 ){
      usleep(500000);
      if(stop_flag==-1){
	return 0;
	theApp->Run(kTRUE);
	return 0;
      }
    } 

  }
  
  theApp->Run(kTRUE);
  
  return 0;
}


void sigint_handler(int sig)
{
  signal( SIGINT, SIG_IGN );
  printf("\n\nReceived SIGINT\n");
  stop_flag = -1;
  return;
}
