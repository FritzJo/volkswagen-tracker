from time import sleep

import requests

from vw_carnet import CarNetLogin, getMileage, getRange
from environment import get_username, get_password, get_database_host, get_database_port
from database.influx import add_entry

# Login information for the VW CarNet app
CARNET_USERNAME = get_username()  # Insert your credentials here, if you run this application manually
CARNET_PASSWORD = get_password()  # Insert your credentials here, if you run this application manually

s = requests.Session()  # Create a session to save cookies and connection data
url = CarNetLogin(s, CARNET_USERNAME, CARNET_PASSWORD)  # Login and receive the custom URL for your Carnet account

"""Request mileage data every 3 hours and write it to the database"""
while True:
    distanceCovered_str = getMileage(s, url)  # Pull the information from Carnet
    distanceCovered = int(distanceCovered_str.replace(".", ""))
    current_range = int(getRange(s, url))
    add_entry(distanceCovered, current_range)  # Insert the value into the database
    sleep(1 * 60 * 60 * 3)  # Wait for 3 h
