SAMPLES = EssMonitor

CC      = g++ 
CFLAGS  = -g -Wall
#INCLUDE = $(shell root-config --cflags)
#LIB     = $(shell root-config --libs)
INCLUDE = `root-config --cflags`
LIB     = `root-config --libs`

all: $(SAMPLES)

EssMonitor: EssMonitor.o
	$(CC) $(CFLAGS) $(INCLUDE) -o $@ $@.o $(LIB)

.c.o:
	$(CC) $(CFLAGS) $(INCLUDE) -c $< 


clean:
	rm -f *.o
	rm -f $(SAMPLES)
