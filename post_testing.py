import requests
import os
import uuid


# if os.getenv("device_id") == None:
#     with open(os.path.expanduser("~/.bashrc"), "a") as outfile:
#         # 'a' stands for "append"
#         outfile.write("export 'device_id'=%s" % str(uuid.uuid4()))
# else:
#     print("device id is %s posting with this id" % os.environ["device_id"])


temp = 500
hum = 531
soil_moisture = 504


d = {
    "temp": temp,
    "unit_id": os.environ["DEVICE_ID"],
    "humidity": hum,
    "soil_moisture": soil_moisture,
    "light_status": True,
    "snapshot":
}

headers = {"Authorization": "Token "}


def sensor_data_post(sensor_data):
    try:
        r = requests.post("http://127.0.0.1:8000/sensors/", headers=headers, data=sensor_data)
        print(r)
    except Exception as e:
        print("post failure ", e)


sensor_data_post(d)
