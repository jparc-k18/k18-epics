// -*- C++ -*-

// Author: Shuhei Hayakawa

#include <algorithm>
#include <bitset>
#include <ctime>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <vector>

#include <TString.h>
#include <TSystem.h>
#include <TTimeStamp.h>

#include "EpicsAlarm.hh"

namespace epics
{

namespace
{
  TString g_file_name;
  const UInt_t CheckInterval = 10; // [s]
  const UInt_t NTime         =  6;
  std::vector<TString>  ChannelList;
  std::vector<Double_t> HighLEVEL;
  std::vector<Double_t> LowLEVEL;
  std::vector< std::vector<Double_t> > value;
  std::vector< std::bitset<NTime> > bit;
  std::time_t now;
}

//_____________________________________________________________________________
void
AlarmSound( void )
{
  // gSystem->Exec("sh script/call_alarm.sh 2>/dev/null &");
  // gSystem->Exec("aplay --device=hw:0,0 script/alarm_sound.wav 2>/dev/null &");
  gSystem->Exec("aplay script/alarm_sound.wav 2>/dev/null &");
}

//_____________________________________________________________________________
void
CheckEpicsData( void )
{
  static const TString addr_list = "EPICS_CA_ADDR_LIST=192.153.109.232";
  static const TString caget = "caget -w 1 -t ";

  for( Int_t i=0, n=ChannelList.size(); i<n; ++i ){
    TString channel = ChannelList[i];
    TString command = caget + channel;
    if( channel.Contains("ALH:") ||
        channel.Contains("HDSYS:") ||
        channel.Contains("HDMON:") ||
        channel.Contains("MRSLW:") ||
        channel.Contains("HDRGPM:") ||
        channel.Contains("HDPPS:") ||
        channel.Contains("RADHD:") ||
        channel.Contains("HDESS:") ||
        channel.Contains("HDPS:") ){
      command = addr_list + " " + command;
    }
    FILE* pipe = gSystem->OpenPipe(command, "r");
    TString ret;
    ret.Gets(pipe);
    gSystem->ClosePipe(pipe);

    Double_t data = ret.Atof();
    Double_t buf[3];
    if( std::sscanf( ret.Data(), "%lf %lf %lf",
                     &buf[0], &buf[1], &buf[2] ) == 3 ){
      data = buf[1];
    }

    for( Int_t j=0, m=NTime-1; j<m; ++j ){
      value[i][j] = value[i][j+1];
      bit[i][j] = bit[i][j+1];
    }

    value[i][NTime-1] = data;
    bit[i].reset(NTime-1);

    if( data < LowLEVEL[i] || HighLEVEL[i] < data )
      bit[i].set(NTime-1);

    gSystem->Sleep(10);
  }

  std::stringstream ss;

  ss << std::left << std::setw(30) << "Name ";// << "Counts ";
  for( Int_t i=0, n=NTime; i<n; ++i )
    ss << std::right << std::setw(6)
       << Form("-%ds", CheckInterval*(n-i-1));
  ss << std::endl;

  Int_t nAlarm = 0;
  Int_t nDisp = 0;

  for( Int_t i=0, n=value.size(); i<n; ++i ){
    // << std::right
    // << std::setw(2) << bit[i].count() << "/"
    // << std::setw(2) << NTime << " ";
    std::stringstream sbuf;
    for( Int_t j=0, m=value[i].size(); j<m; ++j ){
      if( bit[i][j] ) sbuf << "\033[0;33;1m";
      sbuf << std::right << std::setw(6)
	   << Form("%.1lf", value[i][j]);
      if( bit[i][j] ) sbuf << "\033[0m";
    }

    // if( bit[i].count()==NTime ){
    if( bit[i][NTime-1] ){
      sbuf << "\033[0;33;1m"
	   << "  !!! Alarm !!!" << "\033[0m";
      nAlarm++;
    } else {
      sbuf << "               ";
    }

    sbuf << std::endl;
    if( bit[i].any() ){
      ss << std::left << std::fixed << std::setprecision(1)
	 << std::setw(30) << ChannelList[i]// << " ";
	 << sbuf.str();
      nDisp++;
    }
  }
  if( nDisp > 0 )
    std::cout << ss.str() << "\033[J" << std::flush;
  else
    std::cout << " " << ChannelList.size() << " channels are ok\033[0K\033[J"
	      << std::endl;
  if( nAlarm > 0 )
    AlarmSound();
}

//_____________________________________________________________________________
void
Initialize( const TString& file_name )
{
  g_file_name = file_name;
  std::ifstream ifs( file_name );
  if( !ifs.is_open() ){
    std::cerr << "#E No such file " << file_name << std::endl;
    std::exit( EXIT_FAILURE );
  }

  TString line;
  while( ifs.good() && line.ReadLine(ifs) ){
    if( line[0]=='#' ) continue;
    TString c;
    Double_t p1,p2;
    std::stringstream ss(line.Data());
    if( !( ss >> c >> p1 >> p2 ) )
      continue;
    ChannelList.push_back(c);
    LowLEVEL.push_back(p1);
    HighLEVEL.push_back(p2);
  }
  ifs.close();

  value.resize( ChannelList.size() );
  bit.resize( ChannelList.size() );
  for( Int_t i=0, n=ChannelList.size(); i<n; ++i ){
    value[i].resize(NTime);
  }
}

//_____________________________________________________________________________
void
PrintTime( void )
{
  TTimeStamp s;
  s.Add( -TTimeStamp::GetZoneOffset() );
  std::cout << "Last update : " << s.AsString("s") << "\033[0K"
	    << std::endl << "\033[0K" << std::endl;
}

//_____________________________________________________________________________
void
Run( void )
{
  std::cout << "\033[2J";
  while( true ){
    std::cout << "\033[H"
	      << "EPICS Alarm is running ... " << g_file_name
	      << "\033[0K" << std::endl;
    now = std::time(0);
    // ShowThreshold();
    PrintTime();
    CheckEpicsData();
    Int_t rest = CheckInterval - (std::time(0) - now);
    if( rest>0 ) ::sleep(rest);
  }
}

//_____________________________________________________________________________
void
ShowThreshold( void )
{
  std::cout << TString('=',5) << " Threshold " << TString('=', 64) << std::endl
	    << std::left
	    << std::setw(4) << "CH" << std::setw(20) << "Name"
	    << std::right
	    << std::setw(8) << "Low"
	    << std::setw(8) << "High" << std::endl;
  for( Int_t i=0, n=ChannelList.size(); i<n; ++i ){
    value[i].resize(NTime);
    std::cout << std::left
	      << std::setw(4) << i+1
	      << std::setw(20) << ChannelList[i]
	      << std::right << std::fixed << std::setprecision(1)
	      << std::setw(8) << LowLEVEL[i]
	      << std::setw(8) << HighLEVEL[i] << std::endl;
  }
  std::cout << TString('=', 80) << std::endl;
}

}
