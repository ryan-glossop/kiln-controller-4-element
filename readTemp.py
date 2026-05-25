#!/home/ryan/kiln-controller/venv/bin/python
#from max6675 import MAX6675, MAX6675Error
import sys
import board
import digitalio
from MAX31856.max31856 import max31856
import pymongo
import pprint
import time
import datetime
import busio

#thermocouple_type = adafruit_max31856.MAX31856_K_TYPE
gpio_sensor_cs = 25
gpio_sensor_clock = 23
gpio_sensor_data = 24
gpio_sensor_di = 22 # only used with max31856

if len(sys.argv) < 2:
        print("usage: " + sys.argv[0] + " <poll_interval_seconds>")
        sys.exit(1)
poll_interval_seconds = float(sys.argv[1])

try:
        client = pymongo.MongoClient('mongodb://192.168.0.111:27017')
        col_temperature = client.kiln.temp
        mongo=True
except:
        mongo=False

#clear the DB:
#col_temperature.delete_many({})

thermocouple = max31856(csPin = 25)
thermocouple.setupGPIO()

while True:
        try:
                tempC = thermocouple.readThermocoupleTemp()
                temp = (tempC * 9.0/5.0) + 32
                timestamp = datetime.datetime.now()
                print(str(timestamp) + " - @ temp - " + str(temp))
                if(mongo):
                        col_temperature.insert_one({'temp':temp,'time':timestamp})
                else:
                        try:
                                client = pymongo.MongoClient('mongodb://192.168.0.111:27017')
                                col_temperature = client.kiln.temp
                                mongo=True
                        except:
                                mongo=False
                time.sleep(poll_interval_seconds)
        except KeyboardInterrupt:
                raise
        except:
                print("error!")
thermocouple.cleanup()
