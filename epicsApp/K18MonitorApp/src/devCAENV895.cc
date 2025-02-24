#include <cstddef>
#include <cstdlib>
#include <cstdio>
#include <string>
#include <sstream>
#include <cstring>
#include <iostream>
#include <iterator>
#include <fstream>

#include <unistd.h>
#include <sys/resource.h>

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
using namespace std;

static long read_wf(waveformRecord *rec)
{
  float* ptr = (float*)rec->bptr;

  char host[100];
  if(std::sscanf(rec->desc, "CAENV895 %s", host) != 1){
    std::cerr << "CAENV895: DESC format error" << std::endl;
    return 0;
  }

  std::string command = "ssh ";
  // command += " -o HostKeyAlgolithms=+ssh-rsa";
  // command += " -o PublicKeyAcceptedTypes=+ssh-rsa ";
  command += host;
  command += " cat CaenV895/last_param.log";
  FILE *pipe = ::popen(command.c_str(), "r");
  if(!pipe){
    std::cerr << "CAENV895: command error: " << command << std::endl;
    return 0;
  }
  char buf[256];
  bool threshold_start = false;
  int ndata = 0;
  std::cout << "===== " << host << " =====" << std::endl;
  while(!feof(pipe)){
    ::fgets(buf, sizeof(buf), pipe);
    std::string line(buf);
    std::istringstream iss(line);
    std::istream_iterator<std::string> begin(iss);
    std::istream_iterator<std::string> end;
    std::vector<std::string> v(begin, end);
    if(v.empty()) continue;
    if(v[0].find("=====") != std::string::npos){
      threshold_start = false;
    }
    if(ndata%16 == 0){
      threshold_start = false;
    }
    if(v[0].find("threshold") != std::string::npos){
      threshold_start = true;
      v.erase(v.begin());
    }
    if(threshold_start){
      for(const auto& val: v){
	std::cout << ndata << "\t" << std::atof(val.c_str()) << std::endl;
	ptr[ndata++] = (float)std::atof(val.c_str());
      }
    }
  }

  ::pclose(pipe);
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

struct IOC devCAENV895={
  6,
  NULL,
  NULL,
  (DEVSUPFUN) init_record,
  NULL,
  (DEVSUPFUN) read_wf,
  NULL
};
epicsExportAddress(dset,devCAENV895);
