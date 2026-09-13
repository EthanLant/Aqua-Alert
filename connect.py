import asyncio
from bleak import BleakClient
import sys

ADDRESS = "F4:2D:C9:72:76:2E"
CHAR_UUID = "abcd1234-5678-90ab-cdef-1234567890ab"

async def main():
    
    value = await client.read_gatt_char(CHAR_UUID)
    
    if not value:
        with open("recieve.txt", "w") as f:
            print("Device not found.")
        return
        
    async with BleakClient(ADDRESS) as client:
        with open("receive.txt", "w") as f: 
            print("Connected!", file=f)
            print("Received:", value.decode(), file=f)

asyncio.run(main())
