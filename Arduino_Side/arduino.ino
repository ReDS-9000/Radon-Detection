#include "LiquidCrystal_PCF8574.h"
#include <Wire.h>


LiquidCrystal_PCF8574 lcd(0x27); //controllare scheda I2C


int totalCount = 0;
int countmin= 0;    // TODO: calcolare conteggi al minuto
const byte interruptPin = 2;


void tic() {
  totalCount++;
  Serial.println(1); 
}

void resetta() {
  Serial.println(3);
  totalCount = 0;
}

void poweroff() {
  Serial.println(2);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("   SPENTO");
  LowPower.deepSleep(10000);
}

void setup() {
  lcd.print("Rivelatore Radon");
  lcd.setCursor(0, 1);
  lcd.print("V 3.0");
  Serial.begin(115200);
  pinMode(8, INPUT);
  pinMode(7, INPUT);
  pinMode(interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(0), tic, CHANGE); //rivelatore
  attachInterrupt(digitalPinToInterrupt(1), resetta, CHANGE); //reset
  attachInterrupt(digitalPinToInterrupt(7), poweroff, CHANGE); //poweroff
  delay(2000);
  lcd.clear();
}

void loop() {
  lcd.setCursor(0, 0);
  lcd.print("tot: ");
  lcd.print(totalCount);
  lcd.setCursor(0, 1);
  lcd.print("/min: ");
  lcd.print(countmin);
  // Serial.println(totalCount);
}

