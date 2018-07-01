
// ==========================================================================
// Velleman K8062 DMX controller library for VM116/K8062
// ==========================================================================

#include <stdio.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <errno.h>
 
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <time.h>
 
#include "dmx.h"


int   * maxChanAddr;        // control register for # of channels to update
ubyte * exitAddr;           // control register to exit deamon
ubyte * chanData;           // 512 byte array of channel data

ubyte * shm;                // shared memory segment containing data & ctrl regs
int     shmid = -1;         // handel to shared memory segment

int address_value[50];

// ==========================================================================
// open the DMX connection
// ==========================================================================

int dmxOpen()
{

  // get the shared memory created by the deamon

    shmid = shmget ( 0x56444D58 , sizeof ( ubyte ) * 515 , 0666 );

    if ( shmid == -1 ) {
      printf ( "error[%d] - is dmxd running?\n" , errno );
      return ( errno );
    }

    // set up control and data registers

    shm = ( ubyte *) shmat ( shmid, NULL, 0 );
    printf("%d",*shm);
    //*shm=255;
    maxChanAddr  = ( int * ) shm;
    exitAddr     = ( ubyte * ) maxChanAddr + 2;
    chanData     = ( ubyte * ) maxChanAddr + 3;
    return 0;
}

// ==========================================================================
// close the DMX connection
// ==========================================================================

void dmxClose()
{
  if ( shmid != -1 ) shmdt ( shm );
}

// ==========================================================================
// dmxSetMaxChannels -- set the maximum # of channels to send
// ==========================================================================

void dmxSetMaxChannels ( int maxChannels )
{
  *maxChanAddr = maxChannels;
}

// ==========================================================================
// dmxSetValue -- set the value for a DMX channel
// ==========================================================================

void dmxSetValue ( ubyte channel , ubyte data )
{
  chanData[channel] = data;
}

void delay(int input_time){
	int i=0;
	int j=0;
	for(j=0; j<input_time; j++){
		for(i=0; i<10000; i++){}
    }
}


void toggle(int togglePin){
	if(address_value[togglePin] ==130){
	    //printf("%d off ",togglePin);
		dmxSetValue(togglePin,1);
		address_value[togglePin] = 1;
	} else {   
		dmxSetValue(togglePin,130);
		address_value[togglePin] = 130;
	    //printf("%d on ",togglePin);
	}
}

void set(int q){
	dmxSetValue(q,130);
}

void playSong(const char* songName, float bpm){
	FILE* file = fopen(songName, "r");
  float sixteenthNoteTime = 7.5;
  float whatever = sixteenthNoteTime / bpm;
  clock_t t;
  double timeTaken;
  bool toggled = false;
  sixteenthNoteTime = whatever * 20000000.0;
  t=clock();
  int i = 0;
  fscanf(file, "%d", &i);
  while(!feof (file)){
    if(i){
      if(i < 0){
	bpm = -1 * i;
	sixteenthNoteTime = 7.5;
        whatever = sixteenthNoteTime / bpm;
        sixteenthNoteTime = whatever * 1000000.0;
      } else {
	toggled = true;
	toggle(i);
      }
    } else {	
      set(59);
      //usleep(sixteenthNoteTime);
      while(clock() - t < sixteenthNoteTime){};
      //timeTaken = ((clock() - (double) t )) / CLOCKS_PER_SEC;
      //printf("%f\n", timeTaken);	
      t = clock();
    }
    fscanf(file, "%d", &i);
  }
  fclose(file);
}
 


int main(int argc, char *argv[]){
	
	int z=0;
	int q=0;
	
	for(int x=0; x < 50; x++){
		address_value[x] = 1;
	}

	//dmxSetMaxChannels(3);
    // open DMX interface

	int success = dmxOpen();
	if ( success < 0 ) return ( success );
	/*
	while(1){
	for(int x=1; x < 50; x++){
		toggle(x);
		delay(1000);
	}
	}
	*/
	
	playSong(argv[1], 140.0);

	
	printf("done");
	return 0;
}
