TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = K18Monitor
# K18Monitor.dbd will be created and installed
DBD += K18Monitor.dbd

# K18Monitor.dbd will be made up from these files:
K18Monitor_DBD += base.dbd

# Include dbd files from all support applications:
K18Monitor_DBD += devSKSNMR.dbd
K18Monitor_DBD += devD4Probe.dbd
K18Monitor_DBD += devTR700W.dbd
K18Monitor_DBD += devTR72NW_socket.dbd
K18Monitor_DBD += devTR72NW.dbd
K18Monitor_DBD += devAiTR72NW.dbd
K18Monitor_DBD += devHTTP_k18magnet.dbd
K18Monitor_DBD += devHTTP_aline.dbd
K18Monitor_DBD += devHTTP_bline.dbd
K18Monitor_DBD += devHTTP_sepa.dbd
K18Monitor_DBD += devHTTP_accel.dbd
K18Monitor_DBD += devHTTP_hduser.dbd
K18Monitor_DBD += devAiHTTP.dbd
K18Monitor_DBD += devCAENHV.dbd
K18Monitor_DBD += devCAENV895.dbd
K18Monitor_DBD += devZRRX40.dbd
K18Monitor_DBD += devAiZRRX40.dbd
K18Monitor_DBD += devZRRX45.dbd
K18Monitor_DBD += devGL840_BGO.dbd
K18Monitor_DBD += devGL840_AFT.dbd
K18Monitor_DBD += devGL840_RC.dbd
K18Monitor_DBD += devHDDAQ.dbd
K18Monitor_DBD += devAiHDDAQ.dbd
K18Monitor_DBD += devHUL_Trigger.dbd
K18Monitor_DBD += devAiHUL_Trigger.dbd
#K18Monitor_DBD += devAiMppcBias.dbd
K18Monitor_DBD += devMppcBias.dbd
K18Monitor_DBD += devGAS.dbd
K18Monitor_DBD += devMisc.dbd
K18Monitor_DBD += devMQV9500.dbd
K18Monitor_DBD += devAiMQV9500.dbd
K18Monitor_DBD += devGL840_TPC.dbd
K18Monitor_DBD += devGL840_KURAMA.dbd
K18Monitor_DBD += devSHS.dbd
K18Monitor_DBD += devAiHulScaler.dbd
K18Monitor_DBD += devHulScaler.dbd
K18Monitor_DBD += devGL840_DCVth.dbd
K18Monitor_DBD += devPMX18.dbd
K18Monitor_DBD += devPresSDC.dbd

#K18Monitor_DBD += devHBJ.dbd
#K18Monitor_DBD += devAiHBJ.dbd

# Add all the support libraries needed by this IOC
#K18Monitor_LIBS += xxx

# K18Monitor_registerRecordDeviceDriver.cpp derives from K18Monitor.dbd
K18Monitor_SRCS += UserSocket.cc
K18Monitor_SRCS += K18Monitor_registerRecordDeviceDriver.cpp
K18Monitor_SRCS += devSKSNMR.cc
K18Monitor_SRCS += devD4Probe.cc
K18Monitor_SRCS += devTR700W.cc
K18Monitor_SRCS += devTR72NW_socket.cc
K18Monitor_SRCS += devTR72NW.cc
K18Monitor_SRCS += devAiTR72NW.cc
K18Monitor_SRCS += devHTTP_k18magnet.cc
K18Monitor_SRCS += devHTTP_aline.cc
K18Monitor_SRCS += devHTTP_bline.cc
K18Monitor_SRCS += devHTTP_sepa.cc
K18Monitor_SRCS += devHTTP_accel.cc
K18Monitor_SRCS += devHTTP_hduser.cc
K18Monitor_SRCS += devAiHTTP.cc
K18Monitor_SRCS += devCAENHV.cc
K18Monitor_SRCS += devCAENV895.cc
K18Monitor_SRCS += devAiZRRX40.cc
K18Monitor_SRCS += devZRRX40.cc
K18Monitor_SRCS += devZRRX45.cc
K18Monitor_SRCS += devGL840_BGO.cc
K18Monitor_SRCS += devGL840_AFT.cc
K18Monitor_SRCS += devGL840_RC.cc
K18Monitor_SRCS += devHDDAQ.cc
K18Monitor_SRCS += devAiHDDAQ.cc
K18Monitor_SRCS += devHUL_Trigger.cc
K18Monitor_SRCS += devAiHUL_Trigger.cc
#K18Monitor_SRCS += devAiMppcBias.cc
K18Monitor_SRCS += devMppcBias.cc
K18Monitor_SRCS += devGAS.cc
K18Monitor_SRCS += devMisc.cc
K18Monitor_SRCS += devMQV9500.cc
K18Monitor_SRCS += devAiMQV9500.cc
K18Monitor_SRCS += devGL840_TPC.cc
K18Monitor_SRCS += devGL840_KURAMA.cc
K18Monitor_SRCS += devSHS.cc
K18Monitor_SRCS += devAiHulScaler.cc
K18Monitor_SRCS += devHulScaler.cc
K18Monitor_SRCS += devGL840_DCVth.cc
K18Monitor_SRCS += devPMX18.cc
K18Monitor_SRCS += devPresSDC.cc
#K18Monitor_SRCS += devHBJ.cc
#K18Monitor_SRCS += devAiHBJ.cc

# Build the main IOC entry point on workstation OSs.
K18Monitor_SRCS_DEFAULT += K18MonitorMain.cpp
K18Monitor_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#K18Monitor_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
K18Monitor_LIBS += $(EPICS_BASE_IOC_LIBS)

# User Link
USR_CXXFLAGS += -I/usr/include/libxml2 $(shell unpacker-config --include)
USR_LDFLAGS += -lcaenhvwrapper -lcurl -lxml2 $(shell unpacker-config --libs)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE
