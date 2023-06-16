#include <stddef.h>
#include <stdlib.h>
#include <stdio.h>
#include <string>
#include <cstring>
#include <iostream>
#include <sstream>

#include <unistd.h>
#include <arpa/inet.h>

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

#include "UserSocket.hh"

static long read_wf(waveformRecord *rec)
{
  float* ptr = (float*)rec->bptr;

  ptr[0] = 0.;
  ptr[1] = 0.;
  rec->nord = 2;

  //connect socket
  char host[256];
  if( sscanf(rec->desc,"HTTP@%s",host) != 1 ){
    printf("TR700W no host ip address\n");
    return 0;
  }
  // printf("IP : %s\n", host);


  UserSocket sock( host, 80 );
  if( !sock.IsOpen() )
    return 0;

  // send HTTP request

  //  char cmdline[] = "GET /cdata.inc HTTP/1.0\r\nUser-Agent: Wget/1.12 (linux-gnu)\r\nAccept: */*\r\nHost: 192.168.30.31\r\nConnection: Keep-Alive\r\n\r\n ";

  char cmdline[] = "GET /cdata.inc HTTP/1.0\r\nUser-Agent: Wget/1.12 (linux-gnu)\r\nAccept: */*\r\n Connection: Keep-Alive\r\n\r\n ";
  sock.Write( cmdline, strlen(cmdline) );

  // receive
  std::string buf;
  int total_len=0;
  char c;

  while ( sock.Read( &c, 1 ) > 0 ) {
    if(0x20 < c && c <0x7f){
      buf += c;
      total_len++;
    }
    if(total_len > 65535) break;
  }


  int offset = 271 - total_len;

  std::cout << host << " " << buf << " " << total_len << " " << offset << std::endl;

  if(offset != 0 && offset != 1 && offset != -2){
    time_t t;
    t = time(NULL);
    std::string date(ctime(&t));
    date = date.substr(0, date.length()-1);
<<<<<<< HEAD

=======
>>>>>>> f39bf39 (major change)
    printf("%s | %s TR700W comunication error\n", host, date.c_str());
    return 0;
  }

  // printf("total len = %d\n%s\n", total_len, buf.c_str());

  if(std::string(host).find("30.31") != std::string::npos){
    std::string sub1 =  buf.substr(125, 4);
    // printf("sub1: %s\n",sub1.c_str());
    std::string sub2 =  buf.substr(155, 3);
    // printf("sub2: %s\n",sub2.c_str());
    ptr[0] = (float)( atof(sub1.c_str()) );
    ptr[1] = (float)( atof(sub2.c_str()) ) * 0.1;
  }
  else if(std::string(host).find("30.33") != std::string::npos){
    std::string sub1 =  buf.substr(125, 4);
    // printf("sub1: %s\n",sub1.c_str());
    std::string sub2 =  buf.substr(155, 3);
    // printf("sub2: %s\n",sub2.c_str());
    ptr[0] = (float)( atof(sub1.c_str()) );
    ptr[1] = (float)( atof(sub2.c_str()) ) * 0.1;
  }
  else if(std::string(host).find("30.37") != std::string::npos){
    std::string sub1 =  buf.substr(125, 4);
    // printf("sub1: %s\n",sub1.c_str());
    std::string sub2 =  buf.substr(155, 4);
    // printf("sub2: %s\n",sub2.c_str());
    ptr[0] = (float)( atof(sub1.c_str()) );
    ptr[1] = (float)( atof(sub2.c_str()) );
  }

  std::cout << " temp : " << ptr[0]
	    << " humi : " << ptr[1] << std::endl;

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

struct IOC devTR700W={
  6,
  NULL,
  NULL,
  (DEVSUPFUN) init_record,
  NULL,
  (DEVSUPFUN) read_wf,
  NULL
};
epicsExportAddress(dset,devTR700W);

char charconv(char c) {
  if (c >= 'A' && c <= 'Z') return (c - 'A');
  if (c >= 'a' && c <= 'z') return (c - 'a' + 26);
  if (c >= '0' && c <= '9') return (c - '0' + 52);
  if (c == '+') return 62;
  if (c == '/') return 63;
  return 0;
}
