import argparse
import json
import time
import logging

import adafruit_dht
import board
import paho.mqtt.publish as publish
import os


def send_message(message):
    publish.single(topic="office/sensor1", hostname=mqtt_hostname, port=1883, auth=mqtt_auth, payload=message)
    logging.info(f'Message sent: {message}')


def get_temp():
    try:
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
        temperature = round(temperature, 2)
        humidity = round(humidity, 2)
        return json.dumps({
            "temperature": temperature,
            "humidity": humidity
        })
    except RuntimeError:
        logging.debug('Could not get any data from the sensor.')
        return None


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

script_path = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(filename=f'{script_path}/metrics_sender.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)
logging.info(f'Starting metrics sender with: {mqtt_hostname}')

while True:
    json_message = get_temp()
    if json_message is not None:
        send_message(json_message)
    time.sleep(15)
