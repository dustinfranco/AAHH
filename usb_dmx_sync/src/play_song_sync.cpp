
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

// dmx data and control registers

typedef unsigned char ubyte;

int   * maxChanAddr;      // control register for # of channels to update
ubyte * exitAddr;         // control register to exit deamon
ubyte * chanData;         // 512 byte array of channel data


ubyte *shm;              // shared memory segment containing data & ctrl regs
int shmid;               // handel to shared memory segment


// constants and defs

#define ProgName "dmxd"  // name of this program
#define VendorID 0x10cf  // K8062 USB vendor ID
#define ProdID   0x8062  // K8062 USB product ID

#define UpdateInt 0 // update interval ( microseconds )
#define DefMaxChans   60 // default number of maximum channels

// internal structures

struct usb_bus *bus;    // pointer to the USB bus
struct usb_device *dev; // pointer to the K8062 USB device
usb_dev_handle *udev;   // access handle to the K8062 device


// function delcarations

int  main();

int sendDMX();


int  initUSB();
int  writeUSB ( ubyte *data , int numBytes );
void exitUSB();

int  initSHM();
void exitSHM();

void timediff ( struct timeval *res, struct timeval *a, struct timeval *b );
void timeadd  ( struct timeval *res, struct timeval *a, struct timeval *b );


// ==========================================================================
// main -- dmx deamon
// ==========================================================================

int main() {

}


// ==========================================================================
// sendDMX -- send current DMX data
// ==========================================================================

int sendDMX ()
{
  ubyte data[8] = { 0, 0, 0, 0, 0, 0, 0, 0 };
  int numChans = *maxChanAddr;
  int x = 0;
  int success = 0;
  // find out how many consecutive zeroes are in the data - the start
  // packet can indicate this to avoid sending a bunch of leading
  // zeroes
  int curChanIdx = 0;
  
  //for(x=0; x<8; x++){
    //printf("f%d\n",curChanIdx);
    // build starting packet. this packet specifies how many channels have
    // zero data from the start and then contains the next 6 channels of 
    // data
    //printf("chanidx without 0:%d",curChanIdx);
    data[0] = 4;                          // start packet header (4)
    data[1] = curChanIdx;                 // number of zeroes ( not sent )
    
    data[2] = chanData [ curChanIdx++ ];  // first ( non-zero ) chan data
    data[3] = chanData [ curChanIdx++ ];  // next chan data
    data[4] = chanData [ curChanIdx++ ];  // next chan data
    data[5] = chanData [ curChanIdx++ ];  // next chan data
    data[6] = chanData [ curChanIdx++ ];  // next chan data
    data[7] = chanData [ curChanIdx++ ];  // next chan data
    success = writeUSB ( data , 8 );

    if ( !success ) {
    printf ( "%s: error sending DMX start packet\n" , ProgName );
    return ( 0 );
    }
  //}






  if ( curChanIdx >= numChans ) return ( 1 );

  

  // after the first packet additional packets are sent that contain seven
  // channels each up to 512.
 
  while ( curChanIdx < ( numChans - 7 ) ) {
    //printf("m%d\n",curChanIdx);  
    data[0] = 2;                          // start packet header (2)
    data[1] = chanData [ curChanIdx++ ];  // next chan data
    data[2] = chanData [ curChanIdx++ ];  // next chan data
    data[3] = chanData [ curChanIdx++ ];  // next chan data
    data[4] = chanData [ curChanIdx++ ];  // next chan data
    data[5] = chanData [ curChanIdx++ ];  // next chan data
    data[6] = chanData [ curChanIdx++ ];  // next chan data
  success = writeUSB ( data , 8 );
  }


  if ( !success ) {
    printf ( "%s: error sending DMX bulk packet\n" , ProgName );
    return ( 0 );
  }
  
  return ( 1 );

}

// ==========================================================================
// initUSB -- intialize the USB interface for the device
// ==========================================================================

int initUSB()
{
  int success;
  

  // open the usb library

  usb_init();


  // find the usb device for DMX controller

  usb_find_busses();
  usb_find_devices();

  usb_device_descriptor *descr = 0x0;

  for ( bus = usb_busses; bus; bus = bus -> next ) {

    for ( dev = bus->devices; dev; dev = dev -> next ) {

      printf ( "%s: checking device [%s]\n" , ProgName , dev -> filename );

      descr = & dev->descriptor;

      if (      ( descr -> idVendor == VendorID ) 
             && ( descr -> idProduct == ProdID  ) ) break;
    }
  }

  if ( !dev ) {
  printf ( "%s: DMX device not found on USB\n" , ProgName );      
  return ( 0 );
  }
  

  // open the device

  printf ( "%s: opening device [%s] ... " , ProgName , dev -> filename );

  udev = usb_open ( dev );

  if ( udev == 0x0 ) {
    printf ( "%s: error opening device\n" , ProgName );
    return ( 0 );
  }
  else {
     printf ( "ok\n" );
  }


  // claim the interface


#if     defined(LIBUSB_HAS_GET_DRIVER_NP) \
     && defined(LIBUSB_HAS_DETACH_KERNEL_DRIVER_NP)

  usb_detach_kernel_driver_np( udev, 0);

#endif


  // set configuration


  usb_set_debug(4);

  success = usb_set_configuration ( udev, 1 );

  if ( success != 0 ) {
    printf ( "%s: configuration error [%d]\n" , ProgName , success );
    return ( 0 );
    
  }


  // claim the interface
      
  success = usb_claim_interface ( udev, 0 );

  if ( success != 0 ) {
      
    printf ( "%s: error claiming interface [%d]\n" , success );
    return ( 0 );
  }

  return ( 1 );
}

// ==========================================================================
// writeUSB -- write a command to the USB interface
// ==========================================================================

int writeUSB ( ubyte *data , int numBytes )
{
  int nSent;

  //  printf ( "%s: writing [%d] bytes " , ProgName , numBytes );
  //  for ( int b = 0; b < numBytes; b++ ) printf ( "[%d]" , data[b] );
  //  printf ( "\n" );

  // write the data

  nSent = usb_interrupt_write ( udev ,
                                1,
                                (char *) data, 
                                numBytes, 
                                200 );

  if ( nSent != numBytes ) {
      
    printf ( "%s: error writing [%d] bytes [%d]\n" , numBytes , nSent );
    return ( 0 );
  }

  return ( 1 );
  
}


// ==========================================================================
// exitUSB -- terminate USB connection
// ==========================================================================

void exitUSB()
{
    usb_close(udev);
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
      countNegs++;
      sendDMX();
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
  struct timeval now,next,diff,delay;
  int success;
  int z=0;
  int q=0;


  // intialize USB device

  success = initUSB();

  if ( !success ) {
    printf ( "%s: error initializing USB interface\n" , ProgName );
    return ( -1 );
  }

  // loop until commanded to shutdown

  while( !*exitAddr ) {
    // send DMX data
    success = sendDMX();
    if ( !success ) {
      printf  ( "%s: DMX send error\n" , ProgName );
      *exitAddr++;
    }
  }

  printf ( "%s: dmx deamon is shutting down\n" , ProgName );


  // on shutdown reset all DMX channels

  memset ( chanData , 0, 512 * sizeof (ubyte) );

  sendDMX();


  // exit the system

	for(int x=0; x < 50; x++){
		address_value[x] = 1;
	}

	//dmxSetMaxChannels(3);
    // open DMX interface

	int success = dmxOpen();
	if ( success < 0 ) return ( success );
	
  exitUSB();
	playSong(argv[1], 140.0);

	
	printf("done");
	return 0;
}
