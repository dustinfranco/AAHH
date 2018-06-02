// ===========================================================================
// DMXWheel - a simple program that sets the color on a DMX device using
//            the color wheel selector on the screen
// ===========================================================================


// ===========================================================================

#include <stdio.h>
#include <stdlib.h>
#include "dmx.h"                              // DMX interface library


// constants and definitions

#define RedChannel  2                         // DMX channel for red control
#define GrnChannel  3                         // DMX channel for green control
#define BluChannel  4                         // DMX channel for blue control
#define NumChannels 3                         // # of DMX channels used


// global variables

// forward declarations

static int      initDMX       ();
static void     setDMXColor   ( double, double, double );
static void     exitDMX       ();


// ===========================================================================
//  main program
// ===========================================================================

int main( int argc, char *argv[] )
{
  int error;


  // initialize

  error = initDMX();
  if ( error < 0 ) return ( error );

  
  // terminate

  exitDMX();

  return ( 0 );

}


// ===========================================================================
// initDMX -- initialize DMX interface
// ===========================================================================

int initDMX()
{

  // open DMX interface

  int success = dmxOpen();
  if ( success < 0 ) return ( success );
  int i=0;

  // configure

  dmxSetMaxChannels ( NumChannels );
  while(1){
      setDMXColor(255,255,255);
      for(i = 0; i<10000; i++){};

      setDMXColor(1024,1024,1024);
      for(i = 0; i<10000; i++){};
  }

  // return valid status

  return ( 0 );


}

// ===========================================================================
// setDMXColor -- set the color values for the DMX device
// ===========================================================================

void setDMXColor ( double red, double grn, double blu )
{

  // convert values to unsigned bytes

  ubyte redVal = (ubyte) ( 255.0f * red );
  ubyte grnVal = (ubyte) ( 255.0f * grn );
  ubyte bluVal = (ubyte) ( 255.0f * blu );


  // set the channel colors

  dmxSetValue ( RedChannel , redVal );
  dmxSetValue ( GrnChannel , grnVal );
  dmxSetValue ( BluChannel , bluVal );
}


// ===========================================================================
// exitDMX -- terminate the DMX interface
// ===========================================================================

void exitDMX()
{

 // blackout

  dmxSetValue ( RedChannel , 0 );
  dmxSetValue ( GrnChannel , 0 );
  dmxSetValue ( BluChannel , 0 );


  // close the DMX connection

  dmxClose();

}


