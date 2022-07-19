import argparse
import json
import time

import adafruit_dht
import board
import paho.mqtt.publish as publish


def send_message(message):
    publish.single(topic="home/office/clock", hostname=mqtt_hostname, port=1883, auth=mqtt_auth, payload=message)
    print(f'Message sent: {message}')


def get_temp():
    try:
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
        temperature = str(round(temperature, 2))
        humidity = str(round(humidity, 2))
        return json.dumps({
            "temperature": temperature,
            "humidity": humidity
        })
    except RuntimeError:
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


if __name__ == "__main__":
    while True:
        json_message = get_temp()
        if json_message is not None:
            send_message(json_message)
        time.sleep(15)
