#include <iostream>
#include <stddef.h>
#include <stdlib.h>
#include <stdio.h>
#include <string>

#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>

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

struct device_private
{
  short dbrType;
  long  nelem;
  int   channel;
};

static long read_ai(aiRecord *rec)
{
  device_private *pdev = (device_private *)rec->dpvt;

  int ch = pdev->channel;

  long nelem;
  dbGetNelements(&rec->inp, &nelem);
  pdev->nelem = nelem;

  if( 1<= ch && ch <= nelem ){
    float buf[200];
    long status = dbGetLink(&rec->inp, dbGetLinkDBFtype(&rec->inp), buf, NULL, &pdev->nelem);
    rec->rval = buf[ch-1];
  }else{
    rec->rval = -9999;
  }

  rec->udf = FALSE;
  return 0;
}

static long init_record(aiRecord *rec, int pass)
{
  struct device_private *pdev;
  pdev = (struct device_private *)malloc(sizeof(struct device_private));

  pdev->dbrType = (short)dbGetLinkDBFtype(&rec->inp);

  long nRequest=0;
  dbGetNelements(&rec->inp, &nRequest);
  if(nRequest>100) nRequest=100;
  pdev->nelem = nRequest;

  int ch=0;

  sscanf(rec->desc,"ZRRX40@%d",&ch);
  if(1<=ch && ch<= nRequest) pdev->channel = ch;
  else pdev->channel = 0;

  rec->dpvt = pdev;
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

struct IOC devAiZRRX40={
  6,
  NULL,
  NULL,
  (DEVSUPFUN) init_record,
  NULL,
  (DEVSUPFUN) read_ai,
  NULL
};
epicsExportAddress(dset,devAiZRRX40);
