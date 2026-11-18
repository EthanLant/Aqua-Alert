
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <BLE2902.h>

#define WATER_SENSOR 34
#define WATER_THRESHOLD 1500 //Ive noticed that my finger gets around 800-100, water is around 1500, so thats how I got the number
                             //Values go from 0-4095, i've never seen above 2500. Open for calibration.
#define SERVICE_UUID "12345678-1234-1234-1234-1234567890ab"
#define FLAG_UUID "abcd1234-5678-90ab-cdef-1234567890ab"

BLECharacteristic *pCharacteristic;
BLEServer *pServer;

bool deviceConnected = false;
bool oldDeviceConnected = false;

uint8_t flag = 0;

// Bluetooth connection callbacks, this is new, it tracks whether the device is connected or not
//Now it only sends flags if the BT is connected. See if statement below for the characteristic
class ServerCallbacks : public BLEServerCallbacks {

  void onConnect(BLEServer *server) override {
    deviceConnected = true;
    Serial.println("[BLE] Client connected");
  }

  void onDisconnect(BLEServer *server) override {
    deviceConnected = false;
    Serial.println("[BLE] Client disconnected");
  }
};

void setup() {
  Serial.begin(115200);

  pinMode(WATER_SENSOR, INPUT);
  analogReadResolution(12);

  BLEDevice::init("Capstone_ESP32");

  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new ServerCallbacks());

  BLEService *pService = pServer->createService(SERVICE_UUID);

  pCharacteristic = pService->createCharacteristic(
    FLAG_UUID,
    BLECharacteristic::PROPERTY_READ |
    BLECharacteristic::PROPERTY_NOTIFY
  );

  pCharacteristic->addDescriptor(new BLE2902());
  pCharacteristic->setValue(&flag, 1);

  pService->start();

  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->start();

  Serial.println("[BLE] Advertising started");
}

void loop() {

  int waterValue = analogRead(WATER_SENSOR);

  flag = (waterValue > WATER_THRESHOLD) ? 1 : 0;

  // Update BLE characteristic
  pCharacteristic->setValue(&flag, 1);

  // Send notification only when connected
  if (deviceConnected) {
    pCharacteristic->notify();
  }

  Serial.print("Water: ");
  Serial.print(waterValue);
  Serial.print(" | Flag: ");
  Serial.print(flag);
  Serial.print(" | Connected: ");
  Serial.println(deviceConnected ? "YES" : "NO");

  // Restart advertising after disconnection, if the oldconnection status doesnt = current status, then it disconnected, and restarts
  if (!deviceConnected && oldDeviceConnected) {
    delay(200);
    pServer->startAdvertising();
    Serial.println("[BLE] Advertising restarted");
    oldDeviceConnected = false;
  }

  if (deviceConnected && !oldDeviceConnected) {
    oldDeviceConnected = true;
  }

  delay(2000);
}
