#! /usr/bin/python3

# Push Scale to websocket should be fun

import asyncio
import websockets
import time
import sys

import RPi.GPIO as GPIO
from hx711 import HX711

hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(377)

print("Tare done! Add weight now...")

hx.reset()
hx.tare()

ReadList = []

async def the_socket(websocket, path):
    try:
        while True:
            await websocket.send(str(sum(ReadList)/len(ReadList)))
            await asyncio.sleep(1)
    except  websockets.exceptions.ConnectionClosed :
        print ("closed")   

async def read_scale():
    global ReadList
    while True:
        ReadList.append(hx.get_weight(5))
        if len(ReadList) > 5 :
            ReadList.pop(0)
        hx.power_down()
        hx.power_up()

        await asyncio.sleep(0.2)

start_server = websockets.serve(the_socket, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(asyncio.wait([   
   read_scale(),
   start_server
]))
asyncio.get_event_loop().run_forever()