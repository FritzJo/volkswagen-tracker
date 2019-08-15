import datetime

from influxdb import InfluxDBClient
from environment import get_database_host, get_database_port, get_database_user, get_database_pass


def add_entry(data, current_range):
    time = datetime.datetime.now()

    # Connect to the database
    client = InfluxDBClient(get_database_host(),
                            get_database_port(),
                            get_database_user(),
                            get_database_pass(),
                            'volkswagen')

    client.create_database('volkswagen')

    # Create the json containing the relevant data
    json_body = [
        {
            "measurement": "mileage",
            "time": time,
            "fields": {
                "mileage_value": data
            }
        },
        {
            "measurement": "range",
            "time": time,
            "fields": {
                "current_range": current_range
            }
        }
    ]

    # Write the data to the database
    client.write_points(json_body)
