
// ==========================================================================
// Velleman K8062 DMX controller library for VM116/K8062
// ==========================================================================

#include <stdio.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <errno.h>

#include "dmx.h"


int   * maxChanAddr;        // control register for # of channels to update
ubyte * exitAddr;           // control register to exit deamon
ubyte * chanData;           // 512 byte array of channel data

ubyte * shm;                // shared memory segment containing data & ctrl regs
int     shmid = -1;         // handel to shared memory segment


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

int main(){
	int i=0;
	int j=0;
	int z=0;
	int q=0;
	//dmxSetMaxChannels(3);
  // open DMX interface

  int success = dmxOpen();
  if ( success < 0 ) return ( success );\
 
/*
  for(j=255;j>0;j--){
  for(i=255;i>0;i--){
	dmxSetValue(i,j);
  }
  }
  //    for(j=1;j<129;j++){
  for(i=3;i<7;i++){
	dmxSetValue(i,128);
  }
  //}
*/

void delay(int input_time){
	for(j=0; j<input_time; j++){
    for(i=0; i<10000; i++){}
     }
}

while(1){
		
	for(z=1;z<6;z++){
		for(q=1;q<2;q++){
	
		dmxSetValue(z,1+q);
		
		delay(500);
		dmxSetValue(z,128+q);
		delay(500);
		printf("%d\n",z);
	}
	}
	printf("loop");
}
		printf("done");
		return 0;
	}
