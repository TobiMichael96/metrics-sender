import argparse
import json
import time

import adafruit_dht
import board
import paho.mqtt.publish as publish


def send_message(temperature, humidity):
    message = {
        "temperature": temperature,
        "humidity": humidity
    }
    publish.single(topic="home/office/clock", hostname=mqtt_hostname, auth=mqtt_auth, payload=json.dumps(message))


def get_temp():
    try:
        temp = dhtDevice.temperature
        humidity = dhtDevice.humidity
        temp = str(round(temp, 2))
        humidity = str(round(humidity, 2))
        return temp, humidity
    except RuntimeError:
        return None, None


parser = argparse.ArgumentParser(description='Simple Desk-Clock (TME).')
parser.add_argument('--mqtt', nargs='+', dest='mqtt', action='store',
                    help='Activate mqtt output ([host] [username] [password]).')
args = parser.parse_args()

mqtt_hostname = args.mqtt[0]
if len(args.mqtt) == 3:
    mqtt_auth = {
        "username": args.mqtt[1],
        "password": args.mqtt[2]
    }

# initial device
dhtDevice = adafruit_dht.DHT22(board.D2)

while True:
    get_temp()
    time.sleep(15)
