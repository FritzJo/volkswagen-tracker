# Volkswagen-Tracker
Volkswagen-Tracker is a Python script to gather information about your Volkswagen.
I initially created this tool to measure the mileage of my car in a grafana dashboard, but decided
to expand the project to cover other data as well.

It uses the unofficial API of the Volkswagen Car-Net Website, which means this application only works with CarNet-enabled vehicles.
All the data collected is stored in a database.

The API interaction itself is mainly based on the work of [reneboer](https://github.com/reneboer/python-carnet-client).

## Features
* Collecting:
    * Mileage
    * Range
* Writing the gathered data to a database
* Supported database types
    * InfluxDB
* Docker integration

## Roadmap
* Collect more information from Car-Net
* Add more options for database backends
* Predicting the mileage at the end of month or given period of time


# How-To
## Docker
```bash
git clone https://github.com/FritzJo/volkswagen-tracker.git
cd volkswagen-tracker
docker build -t volkswagen-tracker .
docker run -e CARNET_USERNAME=<Your Car-Net Email> \
           -e CARNET_PASSWORD=<Your Car-Net Password> \
           -e CARNET_DATABASE_HOST=<Your InfluxDB Hostaddress> \
           -e CARNET_DATABASE_PORT=<Your InfluxDB Port> \
           -e CARNET_DATABASE_USER=<Your InfluxDB User> \
           -e CARNET_DATABASE_PASS=<Your InfluxDB Password> \
           -e CARNET_UPDATE_INTERVAL=<Wait time between updates (hours)> \
           volkswagen-tracker
```
Alternatively use the docker-compose file that is provided with this repository.
Simply edit the yml file, fill in your credentials and run the following command to
start the application with a InfluxDB. The database will be exposed to port 8086
by default.
```bash
docker-compose up -d --build
```
