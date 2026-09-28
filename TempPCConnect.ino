import asyncio
from bleak import BleakScanner, BleakClient

DEVICE_NAME = "Capstone_ESP32"
FLAG_UUID = "abcd1234-5678-90ab-cdef-1234567890ab"

def flag_received(sender, data):
    flag = data[0]
    print(f"FLAG RECEIVED: {flag}")

async def main():
    print("Searching for ESP32...")

    device = await BleakScanner.find_device_by_name(
        DEVICE_NAME,
        timeout=10
    )

    if device is None:
        print("ESP32 not found!")
        return

    print(f"Found: {device.name}")
    print("Connecting...")

    async with BleakClient(device) as client:
        print("CONNECTED!")
        print("Waiting for flag updates...\n")

        await client.start_notify(FLAG_UUID, flag_received)

        # Stay connected forever
        while True:
            await asyncio.sleep(1)

asyncio.run(main())
