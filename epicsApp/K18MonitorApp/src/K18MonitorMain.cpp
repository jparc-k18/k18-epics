/* K18MonitorMain.cpp */
/* Author:  Marty Kraimer Date:    17MAR2000 */

#include <stddef.h>
#include <stdlib.h>
#include <stddef.h>
#include <string.h>
#include <stdio.h>
#include <iostream> // for debug

#include "epicsExit.h"
#include "epicsThread.h"
#include "iocsh.h"

int main( int argc,char *argv[] )
{
  if(argc>=2) {
    std::cout << argv[1] << std::endl; // for debug
    iocsh(argv[1]);
    epicsThreadSleep(.2);
  }
  iocsh(NULL);
  epicsExit(0);

  return 0;
}
