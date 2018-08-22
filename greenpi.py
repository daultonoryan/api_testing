import Adafruit_DHT
import RPi.GPIO as GPIO
import os
import argparse
import time
import requests


GPIO.setmode(GPIO.BCM)


def sensor_data_post(sensor_data):
    headers = {"Authorization": "Token "}
    try:
        r = requests.post("", headers=headers, data=sensor_data)
        print(r)
    except Exception as e:
        print("post failure ", e)


def get_moisture(pin):
    GPIO.setup(pin, GPIO.IN)
    moisture = GPIO.input(pin)
    return moisture


def get_temp_hum(pin):
    hum, temp = Adafruit_DHT.read_retry(11, pin)
    if temp < 24:
        print("its too cold function called")
    elif temp > 24:
        print("its too hot function called")
    print("humidity: %s" % hum)
    print("temp: %s" % temp)
    return temp, hum


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-temp_pin", help="input pin for temperature humidity sensor", type=int, required=True)
    parser.add_argument("-soil_moisture_pin", help="input pin for soil moisture", type=int, required=True)
    parser.add_argument("-water_level_pin", help="input pin for water level", type=int, required=True)
    args = parser.parse_args()
    count = 0
    while True:
        temp, hum = get_temp_hum(args.temp_pin)
        soil = get_moisture(args.soil_moisture_pin)
        print("moisture: %s" % soil)
        if soil == 1:
            print("please refill tank")
        os.system("raspistill -o rpi_imgs/" + str(count) + ".jpg")
        sensor_data = {"temp": temp,
                       "unit_id": os.environ["DEVICE_ID"],
                       "humidity": hum,
                       "soil_moisture": soil,
                       "light_status": True,
                       "snapshot": "rpi_imgs/" + str(count) + ".jpg"}

	time.sleep(5)
	count += 1


if __name__ == "__main__":
    main()


