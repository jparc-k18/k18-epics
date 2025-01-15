#include <iostream>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <iomanip>
#include <unistd.h>

#define escape_clr              printf("\033[2J")
#define escape_clr_right        printf("\033[0K")
#define escape_location(x,y)    printf("\033[%d;%dH" ,x,y)


int main(int argc, char* argv[]){

  std::cout << "aaa" << std::endl;

  time_t timer;
  struct tm *t_st;
  //time(&timer);
  int hour = 0;
  int min  = 0;
  int sec  = 0;
  int status = 0;
  int count = 0;

  while(1){

    time(&timer);
    t_st = localtime(&timer);
    hour = t_st->tm_hour;
    min  = t_st->tm_min;
    sec  = t_st->tm_sec;

    // clear display //------------------
    for(int n=0;n<20;n++){
      escape_location(n,1);
      escape_clr_right;
    }
    escape_location(1,1);
    //-----------------------------------

    std::cout << "\x1b[1;37;42m"
	      << " Go Home Caller "
	      << "\x1b[0m" << (char)7 << std::endl;
    std::cout << "Present time :  "
	      << std::setfill('0') << std::setw(2) << hour << ":"
	      << std::setfill('0') << std::setw(2) << min << ":"
	      << std::setfill('0') << std::setw(2) << sec
	      << std::endl;

    if( (hour==22 && min>=55 && min<=57) ){
      if (count<1){
	status = system("sh hotaru-long.sh");
	  count++;
      }
    } else if( (hour==17 && min>=30 && min<=32) ){
      if (count<1){
	//	status = system("sh hotaru-short.sh");
	status = system("sh FromTheNewWorld.sh");
	  count++;
      }
    } else{
      count = 0;
    }

    sleep(5);
  }

  return 0;
}
