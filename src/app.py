import requests
import json
import logging
import datetime

from time import sleep

import database.local
import database.influx
import database.sqlite

from vw_carnet import CarNetLogin, CarNetPost
from environment import get_username, get_password, get_update_interval, get_database_type

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

# Define database backends
database_backends = {"influx": database.influx,
                     "sqlite": database.sqlite,
                     "local": database.local,
                     }

# Request data every X hours and write it to the database
time_waited = 0
while True:
    logging.info("Refreshing session and credentials")
    s = requests.Session()
    url = CarNetLogin(s, get_username(), get_password())
    logging.info("Requesting vehicle details from we-connect")
    car_info_json = json.loads(CarNetPost(s, url, '/-/vehicle-info/get-vehicle-details'))
    logging.info("Requesting e-manager information from we-connect")
    emanager_info_json = json.loads(CarNetPost(s, url, '/-/emanager/get-emanager'))

    # Collect important data from json
    time = datetime.datetime.now()
    mileage = int(car_info_json['vehicleDetails']['distanceCovered'].replace(".", ""))
    current_range = int(car_info_json['vehicleDetails']['range'])
    charge_status = 0 if emanager_info_json['EManager']['rbc']['status']['chargingState'] == 'OFF' else 1
    battery_percentage = emanager_info_json['EManager']['rbc']['status']['batteryPercentage']

    data = [time, mileage, current_range, charge_status, battery_percentage]

    logging.info("Writing data to database")

    # Select database type and insert value into db
    database_backends[get_database_type()].add_entry(data)
    logging.info("Waiting for " + get_update_interval() + " hours")
    sleep(1 * 60 * 60 * int(get_update_interval()))  # Wait for X h
