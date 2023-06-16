
// -*- C++ -*-

#include <cstddef>
#include <cstdlib>
#include <cstdio>
#include <cstring>
#include <iostream>
#include <sstream>
#include <string>

#include "alarm.h"
#include "cvtTable.h"
#include "dbDefs.h"
#include "dbAccess.h"
#include "recGbl.h"
#include "recSup.h"
#include "devSup.h"
#include "link.h"
#include "waveformRecord.h"
#include "epicsExport.h"

#include <CAENHVWrapper.h>

enum E_CAEN_STATUS
  {
    kOn                   = 0,
    kRampingUp            = 1,
    kRampingDown          = 2,
    kOverCurrent          = 3,
    kOverVoltage          = 4,
    kUnderVoltage         = 5,
    kExternalTrip         = 6,
    kMaxV                 = 7,
    kExternalDisable      = 8,
    kInternalTrip         = 9,
    kUnplugged            = 10,
    kReserved             = 11,
    kOverVolageProtection = 12,
    kPowerFail            = 13,
    kTemperatureError     = 14,
    N_CAEN_STATUS         = 15
  };

static long read_wf(waveformRecord *rec)
{
  float* ptr = (float*)rec->bptr;
  int ndata=0;
  // ptr[ndata++] = -9999.;
  // for( int i=0, n=rec->nelm-1; i<n; ++i ){
  //   ptr[ndata++] = -9999.;
  //   ptr[ndata++] = -9999.;
  //   ptr[ndata++] = -9999.;
  //   ptr[ndata++] = -9999.;
  //   ptr[ndata++] = -9999.;
  //   ptr[ndata++] = -9999.;
  // }

  // rec->nord = ndata;

  char board[16] = {};
  char host[256] = {};
  unsigned int slot_buf   = 0;
  unsigned int ch_max_buf = 0;
  if( sscanf(rec->desc, "%s %s %d %d",
	     board, host, &slot_buf, &ch_max_buf) != 4 ){
    printf("CAEN HV: DESC format error\n");
    return 0;
  }

  const unsigned short slot = slot_buf;
  const int ch_max = ch_max_buf>24 ? 24 : ch_max_buf;

  CAENHV_SYSTEM_TYPE_t sysType;
  int link = LINKTYPE_TCPIP;
  char UserName[] = "admin";
  char Passwd[] = "admin";
  static int sysHndl=-1;

  if(!strcmp(board,"SY1527")) sysType = SY1527;
  else if(!strcmp(board,"SY2527")) sysType = SY2527;
  else if(!strcmp(board,"SY4527")) sysType = SY4527;
  else if(!strcmp(board,"SY5527")) sysType = SY5527;
  else{
    printf("CAEN HV: unknown borad type %s\n",board);
    return 0;
  }

  if(sysHndl==-1){
    int ret = CAENHV_InitSystem(sysType, link, host, UserName, Passwd, &sysHndl);
    if(ret != CAENHV_OK){
      printf("\nCAENHV_InitSystem: %s (num. %d)\n\n", CAENHV_GetError(sysHndl), ret);
      return 0;
    }
  }

  unsigned short slotList[1] = { slot };
  unsigned short ChList[24] = {
    0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23
  };
  float V0Set[24] = {};
  float I0Set[24] = {};
  float VMon[24]  = {};
  float IMon[24]  = {};
  unsigned int Pw[24] = {};
  unsigned int Status[24] = {};
  unsigned int BdStatus = 0;

  CAENHV_GetBdParam(sysHndl, slot, slotList, "BdStatus", &BdStatus);
  CAENHV_GetChParam(sysHndl, slot, "V0Set", ch_max, ChList, V0Set);
  CAENHV_GetChParam(sysHndl, slot, "I0Set", ch_max, ChList, I0Set);
  CAENHV_GetChParam(sysHndl, slot, "VMon", ch_max, ChList, VMon);
  CAENHV_GetChParam(sysHndl, slot, "IMon", ch_max, ChList, IMon);
  CAENHV_GetChParam(sysHndl, slot, "Pw", ch_max, ChList, Pw);
  CAENHV_GetChParam(sysHndl, slot, "Status", ch_max, ChList, Status);

  // if (sysType == SY5527) {
  //   int ret = CAENHV_DeinitSystem(sysHndl);
  //   if( ret != CAENHV_OK ){
  //     printf("CAENHV_DeinitSystem: %s (num. %d)\n\n",
  // 	     CAENHV_GetError(sysHndl), ret);
  //     return 0;
  //   }
  // }

  ndata=0;
  ptr[ndata++] = BdStatus;

  double val = 0.;
  for(int i=0;i<ch_max;i++){
    printf("CH:%3d  V0Set:%7.1f  I0Set:%6.1f  VMon:%7.1f  IMon:%6.1f  Pw:%s\n",
    	   i, V0Set[i], I0Set[i], VMon[i], IMon[i], Pw[i]? "ON":"OFF");
    ptr[ndata++] = V0Set[i];
    ptr[ndata++] = I0Set[i];
    ptr[ndata++] = VMon[i];
    ptr[ndata++] = IMon[i];
    ptr[ndata++] = (float)Pw[i];
    ptr[ndata++] = (float)Status[i];
    val += V0Set[i] + I0Set[i] + VMon[i] + IMon[i];
  }
  if (// sysType == SY5527 &&
      val == 0.) {
    std::exit(1);
  }

  rec->nord = ndata;

  return 0;
}

static long init_record(waveformRecord *rec, int pass)
{
  return 0;
}

struct IOC{
  long      number;
  DEVSUPFUN report;
  DEVSUPFUN init;
  DEVSUPFUN init_record;
  DEVSUPFUN get_ioint_info;
  DEVSUPFUN read_wf;
  DEVSUPFUN special_linconv;
};

struct IOC devCAENHV={
  6,
  NULL,
  NULL,
  (DEVSUPFUN) init_record,
  NULL,
  (DEVSUPFUN) read_wf,
  NULL
};
epicsExportAddress(dset,devCAENHV);
