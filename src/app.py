import requests
import json

from time import sleep
from database.influx import add_entry

from vw_carnet import CarNetLogin, CarNetPost
from environment import get_username, get_password, get_update_interval

"""Generates a json-file with all relevant information"""
def getCarInformation(s, url_base):
    info = CarNetPost(s, url_base, '/-/vehicle-info/get-vehicle-details')
    json_info = json.loads(info)
    return json_info


s = requests.Session()  # Create a session to save cookies and connection data
url = CarNetLogin(s, get_username(), get_password())  # Login and receive the custom URL for your Carnet account

"""Request data every X hours and write it to the database"""
time_waited = 0
while True:
    if time_waited > 24:  # Refresh login every 24h
        s = requests.Session()  
        url = CarNetLogin(s, get_username(), get_password()) 
        time_waited = 0
    car_info_json = getCarInformation(s, url)
    add_entry(car_info_json)  # Insert the value into the database
    time_waited = time_waited + int(get_update_interval())  # Time since last login refresh
    sleep(1 * 60 * 60 * int(get_update_interval()))  # Wait for X h
