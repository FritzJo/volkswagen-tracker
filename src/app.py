import requests
from time import sleep
from database.influx import add_entry

from vw_carnet import CarNetLogin, getMileage, getRange
from environment import get_username, get_password, get_update_interval

s = requests.Session()  # Create a session to save cookies and connection data
url = CarNetLogin(s, get_username(), get_password())  # Login and receive the custom URL for your Carnet account
# the authentication information doesn't get refreshed once the container started, this might be a problem later...

"""Request data every X hours and write it to the database"""
time_waited = 0
while True:
    if time_waited > 24:  # Refresh login every 24h
        s = requests.Session()  
        url = CarNetLogin(s, get_username(), get_password()) 
        time_waited = 0
    distanceCovered_str = getMileage(s, url)  # Pull the information from Carnet
    distanceCovered = int(distanceCovered_str.replace(".", ""))  # Removes the . in the mileage value (6.400 -> 6400)
    current_range = int(getRange(s, url))
    add_entry(distanceCovered, current_range)  # Insert the value into the database
    time_waited = time_waited + get_update_interval()  # Time since last login refresh
    sleep(1 * 60 * 60 * get_update_interval())  # Wait for X h
