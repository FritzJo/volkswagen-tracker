import requests
import json

from time import sleep
from database.influx import add_entry

from vw_carnet import CarNetLogin, CarNetPost
from environment import get_username, get_password, get_update_interval

#s = requests.Session()  # Create a session to save cookies and connection data
#url = CarNetLogin(s, get_username(), get_password())  # Login and receive the custom URL for your Carnet account

"""Request data every X hours and write it to the database"""
time_waited = 0
while True:
    s = requests.Session()  
    url = CarNetLogin(s, get_username(), get_password()) 
    car_info_json = json.loads(CarNetPost(s, url, '/-/vehicle-info/get-vehicle-details'))
    emanager_info_json = json.loads(CarNetPost(s, url, '/-/emanager/get-emanager'))
    add_entry(car_info_json, emanager_info_json)  # Insert the value into the database
    sleep(1 * 60 * 60 * int(get_update_interval()))  # Wait for X h
