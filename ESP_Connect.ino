#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <BLE2902.h>

#define BUTTON_PIN 27

#define SERVICE_UUID "12345678-1234-1234-1234-1234567890ab"
#define FLAG_UUID    "abcd1234-5678-90ab-cdef-1234567890ab"

BLECharacteristic *pCharacteristic;

uint8_t flag = 0;

void setup() {

  Serial.begin(115200);
  delay(1000);

  Serial.println("Starting BLE...");

  // GPIO 27 normally HIGH because of internal pull-up
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  BLEDevice::init("Capstone_ESP32");

  BLEServer *pServer = BLEDevice::createServer();

  BLEService *pService =
      pServer->createService(SERVICE_UUID);

  pCharacteristic = pService->createCharacteristic(
      FLAG_UUID,
      BLECharacteristic::PROPERTY_READ |
      BLECharacteristic::PROPERTY_NOTIFY
  );

  // Needed for BLE notifications
  pCharacteristic->addDescriptor(new BLE2902());

  // Initial flag
  pCharacteristic->setValue(&flag, 1);

  pService->start();

  BLEAdvertising *pAdvertising =
      BLEDevice::getAdvertising();

  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->start();

  Serial.println("BLE advertising started");
}

void loop() {

  // Jumper touching GND = 1
  if (digitalRead(BUTTON_PIN) == LOW) {
    flag = 1;
  }
  else {
    flag = 0;
  }

  // Update BLE characteristic
  pCharacteristic->setValue(&flag, 1);

  // Send notification
  pCharacteristic->notify();

  Serial.print("Sending flag: ");
  Serial.println(flag);

  delay(5000);
}
