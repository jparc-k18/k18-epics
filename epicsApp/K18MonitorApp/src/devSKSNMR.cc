// -*- C++ -*-

#include <stddef.h>
#include <stdlib.h>
#include <stdio.h>
#include <string>

#include <unistd.h>
#include <arpa/inet.h>
#include <arpa/inet.h>
#include <iostream>

#include "alarm.h"
#include "cvtTable.h"
#include "dbDefs.h"
#include "dbAccess.h"
#include "recGbl.h"
#include "recSup.h"
#include "devSup.h"
#include "link.h"
#include "aiRecord.h"
#include "epicsExport.h"

#include "UserSocket.hh"

namespace
{
  UserSocket* sock = nullptr;
}

static long read_ai(aiRecord *rec)
{
  if (!sock->IsOpen())
    std::exit(1);

  //rehold?
  char sig_rehold[50];
  int flag_rehold = 0;
  FILE *f_sighold = fopen("/home/sks/k18epics/tools/k18mag/rehold_signal.txt","r");
  if(f_sighold){
    fgets(sig_rehold, 50, f_sighold);
    if( sig_rehold[0]=='a' || sig_rehold[0]=='b'|| sig_rehold[0]=='c' || sig_rehold[0]=='d' ){
      // detect re_hold signal
      flag_rehold = 1;
    }
    fclose(f_sighold);
    if( flag_rehold ){
      printf("SKS NMR send rehold command\n");
      FILE *f_sigout = fopen("/home/sks/k18epics/tools/k18mag/rehold_signal.txt","w");
      fprintf(f_sigout, "0");
      fclose(f_sigout);
      sock->Write(sig_rehold, 1); // seng range setting (force reset val to manual value)
      usleep(1000*100);
    }
  } else {
    std::cout << "rehold_signal.txt was not found" << std::endl;
  }
  //get value
  if(sock->Write("n",1) < 0)
    std::exit(1);

  char buf[64];
  sock->Read(buf,64);
  printf("SKS Field: %f [T]\n",atof(buf)*1E-6);

  rec->val = atof(buf)*1E-6;
  rec->udf = FALSE;

  return 2;
}

static long init_record(aiRecord *rec)
{
  sock = new UserSocket("192.168.30.20", 10001);
  if (!sock || !sock->IsOpen())
    std::exit(1);
  return 0;
}

struct IOC{
  long      number;
  DEVSUPFUN report;
  DEVSUPFUN init;
  DEVSUPFUN init_record;
  DEVSUPFUN get_ioint_info;
  DEVSUPFUN read_ai;
  DEVSUPFUN special_linconv;
};

struct IOC devSKSNMR={
  6,
  NULL,
  NULL,
  (DEVSUPFUN) init_record,
  NULL,
  (DEVSUPFUN) read_ai,
  NULL
};
epicsExportAddress(dset,devSKSNMR);
