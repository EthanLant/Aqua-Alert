
import asyncio
import csv
import time
from datetime import datetime
from pathlib import Path

from bleak import BleakScanner, BleakClient

# =====================================
# CONFIGURATION - handles naming bt device id, and parameter's that we can set. Be sure to include on report somewhere
# =====================================

DEVICE_NAME = "Capstone_ESP32"
FLAG_UUID = "abcd1234-5678-90ab-cdef-1234567890ab"

LOG_COOLDOWN = 30
RECONNECT_DELAY = 3

LOG_FILE = Path(__file__).resolve().parent / "water_detection_log.csv"

last_log_time = None


# =====================================
# EVENT LOGGING - 
# =====================================

def log_water_event():
    global last_log_time

    now = time.monotonic()

    if last_log_time is not None:
        if now - last_log_time < LOG_COOLDOWN: # this line makes it so our logs dont spam
            return

    timestamp = datetime.now().astimezone()

    new_file = (
        not LOG_FILE.exists()
        or LOG_FILE.stat().st_size == 0
    ) #creates file


    #Next section opens file, writes to it, and saves it
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if new_file:
            writer.writerow([
                "Timestamp",
                "Device",
                "Event",
                "Flag",
                "Status"
            ])

        writer.writerow([
            timestamp.isoformat(timespec="seconds"),
            DEVICE_NAME,
            "Water Detection",
            1,
            "ALERT"
        ])

    last_log_time = now

    print("\n" + "=" * 55)
    print("              WATER DETECTION ALERT")
    print("=" * 55)
    print(f"Timestamp : {timestamp.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"Device    : {DEVICE_NAME}")
    print("Event     : Water Detected")
    print("Flag      : 1")
    print("Status    : LOGGED")
    print("=" * 55 + "\n")


# =====================================
# BLUETOOTH NOTIFICATIONS - Esp gets a byte, calls flag recieved
# =====================================

def flag_received(sender, data):

    if not data:
        print("[WARNING] Empty BLE notification")
        return

    flag = data[0]

    if flag == 1:
        log_water_event()
    elif flag == 0:
        print("[NORMAL] Sensor dry")
    else:
        print(f"[WARNING] Unknown flag: {flag}")


# =====================================
# BLUETOOTH CONNECTION - biggest change was trying connection again if disconnect
# =====================================

async def monitor_device():

    while True:
        disconnected = asyncio.Event() #this tells if bluetooth got disconnected

        try:
            print(f"\n[SCAN] Searching for {DEVICE_NAME}...")

            device = await BleakScanner.find_device_by_name(
                DEVICE_NAME,
                timeout=10
            )

            if device is None:
                print("[WARNING] Device not found.")
                await asyncio.sleep(RECONNECT_DELAY)
                continue

            print(f"[FOUND] {device.name}")
            print("[CONNECTING] Establishing BLE connection...")

            def on_disconnect(client):
                print("\n[DISCONNECTED] Bluetooth connection lost.")
                disconnected.set()

            async with BleakClient(
                device,
                disconnected_callback=on_disconnect
            ) as client:

                print("[CONNECTED] BLE connection established.")

                await client.start_notify(
                    FLAG_UUID,
                    flag_received
                ) #This function is crucial for the send/recieve. Subscribes to any data from ESP and send to flag_recieved func

                print("[MONITORING] Waiting for sensor updates...\n")

                # Stay connected until BLE disconnects.
                await disconnected.wait()

        except asyncio.CancelledError:
            raise

        except Exception as error:
            print(f"[ERROR] Bluetooth issue: {error}")

        print(f"[RECONNECT] Retrying in {RECONNECT_DELAY} seconds...")
        await asyncio.sleep(RECONNECT_DELAY)


# =====================================
# MAIN
# =====================================

async def main():
    print("=" * 55)
    print("       CAPSTONE WATER MONITORING SYSTEM")
    print("=" * 55)
    print(f"Device       : {DEVICE_NAME}")
    print(f"Log cooldown : {LOG_COOLDOWN} seconds")
    print(f"Log file     : {LOG_FILE}")
    print("=" * 55)

    await monitor_device()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[STOPPED] Monitoring ended by user.")
