#include <iostream>
#include <iomanip>
#include <sstream>
#include <stdio.h>
#include <stdlib.h>
#include <fstream>
#include <unistd.h>
#include <string.h>
#include <signal.h>

#define escape_clr		printf("\033[2J")
#define escape_clr_right	printf("\033[0K")
#define escape_location(x,y)	printf("\033[%d;%dH" ,x,y)


void sigint_handler(int sig);
volatile int stop_flag=0;
void sigint_handler(int sig){
  signal( SIGINT, SIG_IGN);
  std::cout << "end signal" << std::endl;
  stop_flag = -1;
  return;
}


int main(int argc,char* argv[]){

  if(argc!=2){
    std::cout << "userge: ./HtmlEss [current threshold]" << std::endl;
    return 0;
  }

  signal(SIGINT, sigint_handler);

  char read[2000];
  char title[6][100];
  char setv[6][100];
  char prev[6][100];
  char prec[6][100];
  double Svoltage[6];
  double voltage[6];
  double current[6];
  int flag=0;
  int kakko_flag=0;
  int start_point = 0;
  int end_length = 0;
  int status=0;
  time_t timer;
  std::stringstream oss;
  std::stringstream ossvacuum;
  char dummy1[100];
  char dummy2[100];

  //escape_clr;
  system("clear");
  std::cout << "Start data transition..." << std::endl;

  while(stop_flag==0){

    usleep(1000*5000);

    oss.str("");
    oss << "wget -q "
    	<< "-O ESS.html "
	<< "http://www-cont.j-parc.jp/HD/separator > /dev/null";
    //	<< "http://www-cont.j-parc.jp/HD/separator/ > /dev/null";
    // 	<< "http://www-cont.j-parc.jp/HD/hduser/k18brpc/ > /dev/null";
    // oss << "wget -b -q "
    // 	<< "-O BR.html "
    // 	<< "http://192.168.142.1/test/BR.html > /dev/null";
    status = system(oss.str().c_str());

    usleep(1000*5000);

    // while(1){
    //   usleep(1000*1000);
    //   char a[8]="";
    //   FILE *fp = popen("lsof -c wget","r");
    //   fgets(a,8,fp);
    //   pclose(fp);
    //   if(strcmp(a,"COMMAND")==0){
    // 	usleep(1000*1000);
    //   }
    //   else{
    // 	break;
    //   }
    // }

    if(stop_flag==0){

      // clear display //------------------
      for(int n=0;n<20;n++){
      	escape_location(n,1);
      	escape_clr_right;
      }
      escape_location(1,1);
      //-----------------------------------

      std::cout << "\x1b[1;37;42m"
  	      << " ESS discharge checker "
  	      << "\x1b[0m" << (char)7 << std::endl;
      time(&timer);
      std::cout << "Present time : " << ctime(&timer) << std::endl;

      std::ifstream fin("ESS.html");
      if(!fin){
  	std::cout << "error " << std::endl;
  	fin.close();
  	goto OUT_label;
      }
      int ch = -1;
      for(int n=0;n<90;n++){

  	memset( title, 0, sizeof(title) );
  	memset( setv, 0, sizeof(setv) );
  	memset( prev, 0, sizeof(prev) );
  	memset( prec, 0, sizeof(prec) );
  	flag=0;
  	while(flag==0){
  	  fin.getline(read,2000);
  	  if(strcmp(read,"<tr>")==0){
  	    flag=1;
  	    ch++;
  	  }
  	  if(strcmp(read,"</html>")==0){
  	    fin.close();
  	    std::cout <<"\n ** Ctl+C : exit this program **" << std::endl;
  	    goto OUT_label;
  	  }
  	  if(fin.eof()==1){
  	    fin.close();
  	    std::cout <<"\n ** Ctl+C : exit this program **" << std::endl;
  	    goto OUT_label;
  	  }
  	}

  	// title
  	fin.getline(read,500);
  	kakko_flag = 0;
  	start_point = 0;
  	while(kakko_flag==0){
  	  if( read[start_point] == '>' ){kakko_flag = 1;}
  	  start_point ++;
  	}
  	kakko_flag = 0;
  	end_length = 0;
  	while(kakko_flag==0){
  	  if( read[start_point+end_length] == '<' ){kakko_flag = 1;}
  	  end_length ++;
  	}
  	end_length = end_length -1;
  	strncpy(title[ch], read+start_point, end_length);

  	// set voltage
  	fin.getline(read,500);
  	kakko_flag = 0;
  	start_point = 0;
  	while(kakko_flag==0){
  	  if( read[start_point] == '>' ){kakko_flag = 1;}
  	  start_point ++;
  	}
  	kakko_flag = 0;
  	end_length = 0;
  	while(kakko_flag==0){
  	  if( read[start_point+end_length] == '<' ){kakko_flag = 1;}
  	  end_length ++;
  	}
  	end_length = end_length -1;
  	strncpy(setv[ch], read+start_point, end_length);

	if(ch<4){
	  // present voltage
	  fin.getline(read,500);
	  kakko_flag = 0;
	  start_point = 0;
	  while(kakko_flag==0){
	    if( read[start_point] == '>' ){kakko_flag = 1;}
	    start_point ++;
	  }
	  kakko_flag = 0;
	  end_length = 0;
	  while(kakko_flag==0){
	    if( read[start_point+end_length] == '<' ){kakko_flag = 1;}
	    end_length ++;
	  }
	  end_length = end_length -1;
	  strncpy(prev[ch], read+start_point, end_length);
	  
	  // present current
	  fin.getline(read,500);
	  kakko_flag = 0;
	  start_point = 0;
	  while(kakko_flag==0){
	    if( read[start_point] == '>' ){kakko_flag = 1;}
	    start_point ++;
	  }
	  kakko_flag = 0;
	  end_length = 0;
	  while(kakko_flag==0){
	    if( read[start_point+end_length] == '<' ){kakko_flag = 1;}
	    end_length ++;
	  }
	  end_length = end_length -1;
	  strncpy(prec[ch], read+start_point, end_length);
	}


  	//value = strtod(part,NULL);
	if(ch<4){
	  Svoltage[ch] = atof(setv[ch]);
	  voltage[ch]  = atof(prev[ch]);
	  current[ch]  = atof(prec[ch]);

	  if(ch==0){
	    std::cout
	      << " < ESS1 >     Vset       Vmon      Cmon" << std::endl;
	  }
	  if(ch==2){
	    std::cout << std::endl
		      << " < ESS2 >     Vset       Vmon      Cmon" << std::endl;
	  }
	  
	  std::cout << " " << title[ch] << " :  "
		    << std::fixed << std::setprecision(1) << Svoltage[ch] << "[kV]"
		    << "  " << voltage[ch] << "[kV]"
		    << "  " << current[ch] << "[uA]"
		    <<  std::endl;
	  
	}
	else{
	  ossvacuum.str("");
	  ossvacuum.clear(std::stringstream::goodbit);
	  ossvacuum << setv[ch];
	  ossvacuum >> current[ch] >> dummy2;

	  if(ch==4){
	    std::cout << std::endl;
	  }
	  std::cout << " vacuum " << title[ch] << " :  "
		    << "  " << setv[ch] << "  "
		    << std::endl;
	}

	
      }

    }

  OUT_label:
    std::cout << " " << std::endl;

    double cth = atof(argv[1]);
    if( current[0]>cth ||current[1]>cth ||current[2]>cth ||current[3]>cth ){
      std::cout << "\x1b[1;33;40m"
  		<< "status: over current !!"
  		<< "\x1b[0m" << std::endl;
      status = system("sh call_hatena.sh &");
    }
    else{
      std::cout << "status: normal..." << std::endl;
    }


    // output file //
    std::ofstream fout("ReadValues.txt");
    fout << voltage[0] << std::endl
	 << voltage[1] << std::endl
	 << voltage[2] << std::endl
	 << voltage[3] << std::endl
	 << current[0] << std::endl
	 << current[1] << std::endl
	 << current[2] << std::endl
	 << current[3] << std::endl
	 << std::setprecision(9) << current[4] << std::endl
	 << std::setprecision(9) << current[5] << std::endl;
    fout.close();

  }

  return 0;
}
