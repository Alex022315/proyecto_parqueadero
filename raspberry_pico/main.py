import network
import urequests
from machine import Pin
import time

SSID = "TU_WIFI"
PASSWORD = "TU_PASS"

sensor_entrada = Pin(16, Pin.IN)
sensor_salida = Pin(17, Pin.IN)

URL = "http://TU_IP_PC:5000/sensor"

# Conectar WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    time.sleep(1)

print("Conectado:", wlan.ifconfig())

while True:
    if sensor_entrada.value() == 0:
        urequests.post(URL, json={"evento": "entrada"})
        print("ENTRADA detectada")
        time.sleep(1)

    if sensor_salida.value() == 0:
        urequests.post(URL, json={"evento": "salida"})
        print("SALIDA detectada")
        time.sleep(1)
