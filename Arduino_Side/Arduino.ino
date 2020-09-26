/*
  LiquidCrystal Library - Hello World

 Demonstrates the use a 16x2 LCD display.  The LiquidCrystal
 library works with all LCD displays that are compatible with the
 Hitachi HD44780 driver. There are many of them out there, and you
 can usually tell them by the 16-pin interface.

 This sketch prints "Hello World!" to the LCD
 and shows the time.

  The circuit:
 * LCD RS pin to digital pin 12
 * LCD Enable pin to digital pin 11
 * LCD D4 pin to digital pin 5
 * LCD D5 pin to digital pin 4
 * LCD D6 pin to digital pin 3
 * LCD D7 pin to digital pin 2
 * LCD R/W pin to ground
 * LCD VSS pin to ground
 * LCD VCC pin to 5V
 * 10K resistor:
 * ends to +5V and ground
 * wiper to LCD VO pin (pin 3)

 Library originally added 18 Apr 2008
 by David A. Mellis
 library modified 5 Jul 2009
 by Limor Fried (http://www.ladyada.net)
 example added 9 Jul 2009
 by Tom Igoe
 modified 22 Nov 2010
 by Tom Igoe

 This example code is in the public domain.

 http://www.arduino.cc/en/Tutorial/LiquidCrystal
 */

//CAMBIARE LCSD CON INTERFACCIA I2C
//FOMATTARE SCRITTURA SU LCD
//USARE INTERRUPT PER TUTTI I PULSANTI
//INPUT SERIALE RASPI>ARDU

// include the library code:
#include <LiquidCrystal.h>

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 13);

int contatore = 0;
int resetbtn = 0;
int poweroff = 0;
int totalCount = 0;

const byte interruptPin = 2;


void tic() {
  totalCount++;
  Serial.println(1); 
  lcd.print(totalCount);
}

void setup() {
  lcd.begin(16, 2);
  Serial.begin(115200);

  pinMode(8, INPUT);
  pinMode(7, INPUT);
  pinMode(interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin), tic, CHANGE);
}

void loop() {
  
  lcd.setCursor(0, 1);
  resetbtn = digitalRead(8);
  poweroff = digitalRead(7);

 // Serial.println(totalCount);
  
  
  
  if (resetbtn == HIGH) //contatore simulato
  {
    Serial.println(3);
  } 
  
  if (poweroff == HIGH) //contatore simulato
  {
    Serial.println(2);
  } 
}



 
