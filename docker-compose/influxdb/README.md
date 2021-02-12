# InfluxDB

## Usage

Start InfluxDB.

    sudo docker-compose up -d

## Hacking

Start an InfluxDB shell.

    sudo docker exec -it influxdb_influxdb_1 /bin/bash
    influx -username admin -password admin
