import Adafruit_DHT
import RPi.GPIO as GPIO
import os
import argparse
import time
import requests
import datetime


GPIO.setmode(GPIO.BCM)
headers = {"Authorization": "Token d906b53efa966d6dfa24224621801f25db6f637b"}

def sensor_data_post(sensor_data):
    try:
        r = requests.post("http://127.0.0.1:8000/sensors/", headers=headers, data=sensor_data)
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


def water_plant(pin):
    try:
        r = requests.get("http://127.0.0.1:8000/outputs/", headers=headers)
        print(r)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 1)
        time.sleep(int(r["daily_water"]) / 5)
        GPIO.output(pin, 0)
    except Exception as e:
        print("get failure ", e)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-temp_pin", help="input pin for temperature humidity sensor", type=int, required=True)
    parser.add_argument("-soil_moisture_pin", help="input pin for soil moisture", type=int, required=True)
    parser.add_argument("-water_level_pin", help="input pin for water level", type=int, required=True)
    parser.add_argument("-watering", help="input pin for watering", type=int, required=True)
    parser.add_argument("-light", help="input pin for light", type=int, required=True)
    args = parser.parse_args()
    count = 0
    while True:
        temp, hum = get_temp_hum(args.temp_pin)
        soil = get_moisture(args.soil_moisture_pin)
        print("moisture: %s" % soil)
        if soil == 1:
            print("please refill tank")
        #os.system("raspistill -o rpi_imgs/" + str(count) + ".jpg")
        sensor_data = {"temp": temp,
                       "unit_id": os.environ["DEVICE_ID"],
                       "humidity": hum,
                       "soil_moisture": soil,
                       "light_status": True,
                       #"snapshot": open("rpi_imgs/" + str(count) + ".jpg", "r")
                        }
        now = datetime.datetime.now()
        if now.hour == 1 & now.minute == 20:
            print("doing the thing")
            water_plant(args.watering)
            time.sleep(60)
        try:
            r = requests.get("http://127.0.0.1:8000/outputs/", headers=headers)
            print(r)
            if 0 <= now.hour <= int(r["daily_light"] - 1):
                GPIO.setup(args.light, GPIO.OUT)
                GPIO.output(args.light, 1)
            else:
                GPIO.setup(args.light, GPIO.OUT)
                GPIO.output(args.light, 0)
        except Exception as e:
            print("get failure ", e)
        time.sleep(30)
        count += 1


if __name__ == "__main__":
    main()


