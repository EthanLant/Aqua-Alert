#include <BLEDevice.h>

#include <BLEUtils.h>

#include <BLEServer.h>
 
BLECharacteristic *pCharacteristic;
 
void setup() {

  Serial.begin(115200);

  delay(1000);

  Serial.println("Starting BLE...");
 
  BLEDevice::init("LifeguardDevice");
 
  BLEServer *pServer = BLEDevice::createServer();

  BLEService *pService = pServer->createService("12345678-1234-1234-1234-1234567890ab");
 
  pCharacteristic = pService->createCharacteristic(

    "abcd1234-5678-90ab-cdef-1234567890ab",

    BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY

  );
 
  pCharacteristic->setValue("Ethan is a nerd");

  pService->start();
 
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();

  pAdvertising->addServiceUUID("12345678-1234-1234-1234-1234567890ab");

  pAdvertising->start();
 
  Serial.println("BLE advertising started");

}
 
void loop() {

  delay(2000);

}
 