import asyncio
from bleak import BleakClient
import bleak.exc
from bleak.exc import BleakError
import sys

ADDRESS = "F4:2D:C9:72:76:2E"
CHAR_UUID = "abcd1234-5678-90ab-cdef-1234567890ab"

async def main():
    try:
        async with BleakClient(ADDRESS) as client:
            value = await client.read_gatt_char(CHAR_UUID)
    
    except bleak.exc.BleakDeviceNotFoundError as e:
        print(e)

asyncio.run(main())
