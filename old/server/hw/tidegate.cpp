#include "tidegate.h"


TideGate::TideGate(GPIO_PIN p, uint8_t open, uint8_t closed)
: servo(p),
  OPEN(open),
  CLOSED(closed),
  state(0)
{
}


void TideGate::Open()
{   
	SetValue(state = OPEN);   
}


void TideGate::Close()
{  
	SetValue(state = CLOSED);
}

