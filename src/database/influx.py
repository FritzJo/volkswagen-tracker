import datetime

from influxdb import InfluxDBClient
from environment import get_database_host, get_database_port, get_database_user, get_database_pass


def add_entry(data, current_range, time=""):
    if time is "":
        print("[INFO] Empty timestamp. Using current local time!")
        time = datetime.datetime.now()
    client = InfluxDBClient(get_database_host(),
                            get_database_port(),
                            get_database_user(),
                            get_database_pass(),
                            'volkswagen')

    # client.drop_database('carnet')
    client.create_database('volkswagen')
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

    client.write_points(json_body)
