#include "LiquidCrystal_PCF8574.h"


//LCD
#define LCD_ADDRESS 0x3F //controllare shield
#define LCD_ROWS 2
#define LCD_COLUMNS 16
#define SCROLL_DELAY 150
#define BACKLIGHT 255
LiquidCrystal_PCF8574 lcd;


/*

 lcd.clear();                          // Clear LCD screen.
 lcd.print("  Circuito.io  ");                   // Print print String to LCD on first line
 lcd.selectLine(2);                    // Set cursor at the begining of line 2

*/

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

void resetta() {
    Serial.println(3);
    totalCount = 0;
}

void poweroff() {

    Serial.println(2);
    lcd.clear()
    lcd.print("   SPENTO")

}

void setup() {
  lcd.begin(LCD_COLUMNS, LCD_ROWS, LCD_ADDRESS, BACKLIGHT); 
  Serial.begin(115200);
  pinMode(8, INPUT);
  pinMode(7, INPUT);
  pinMode(interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(0), tic, CHANGE); //rivelatore
  attachInterrupt(digitalPinToInterrupt(1), resetta, CHANGE); //reset
  attachInterrupt(digitalPinToInterrupt(7), poweroff, CHANGE); //poweroff
}

void loop() {
  
  lcd.setCursor(0, 1);
  resetbtn = digitalRead(8);
  poweroff = digitalRead(7);

 // Serial.println(totalCount);

}



