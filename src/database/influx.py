from influxdb import InfluxDBClient

from environment import get_database_host, get_database_port, get_database_user, get_database_pass


def add_entry(data):
    # Create the json containing the relevant data
    json_body = [
        {
            "measurement": "mileage",
            "time": data[0],
            "fields": {
                "mileage_value": data[1]
            }
        },
        {
            "measurement": "range",
            "time": data[0],
            "fields": {
                "current_range": data[2]
            }
        },
        {
            "measurement": "charging",
            "time": data[0],
            "fields": {
                "chargingState": data[3],
                "batteryPercentage": data[4],
            }
        }
    ]

    # Connect to the database
    client = InfluxDBClient(get_database_host(),
                            get_database_port(),
                            get_database_user(),
                            get_database_pass(),
                            'volkswagen')

    client.create_database('volkswagen')

    # Write the data to the database
    client.write_points(json_body)
