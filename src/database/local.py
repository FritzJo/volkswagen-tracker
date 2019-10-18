import datetime


def add_entry(json_info, emanager_info_json):
    time = datetime.datetime.now()
    mileage = int(json_info['vehicleDetails']['distanceCovered'].replace(".", ""))
    current_range = int(json_info['vehicleDetails']['range'])
    charge_status = 0 if emanager_info_json['EManager']['rbc']['status']['chargingState'] == 'OFF' else 1
    battery_percentage = emanager_info_json['EManager']['rbc']['status']['batteryPercentage']

    with open("database.txt", "a") as f:
        f.write(time + ";" + mileage + ";" + current_range + ";" + charge_status + ";" + battery_percentage)
