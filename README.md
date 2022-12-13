# misscheck
Application to get missing block counters from cosmos chains. 

We are using influxdb for storing time series data, grafana
for visualization, python scripts for fetching data.

## Influxdb

Influxdb is an open source time series database highly  optimized for storing time data.

Influxdb can be installed in ubuntu 20.04  directly from the official repositories by the following commands:

    sudo curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
    sudo echo "deb https://repos.influxdata.com/ubuntu bionic stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
    sudo apt update
    sudo apt install influxdb
    sudo systemctl enable --now influxdb
    sudo systemctl start influxdb

Once installed, check the status of the service via:

    sudo systemctl status influxdb

### Configuring Influxdb

The InfluxDB configuration file is located by default in the /etc/influxdb/influxdb.conf folder.

Many features are commented out. To enable them, simply open the configuration file and delete the "#" symbols from the relevant line.

To modify the configuration file use the command:

    sudo nano /etc/influxdb/influxdb.conf

To enable http endpoint, locate the "[http]" section and uncomment the "enabled = true" line. Then restart the influxdb service by:

    sudo systemctl restart influxdb

We will need an administrator account. To create an account, run the following command, by changing the "password":

    curl -XPOST "http://localhost:8086/query" --data-urlencode "q=CREATE USER admin WITH PASSWORD 'password' WITH ALL PRIVILEGES"

Once the account is created, access the InfluxDB shell by using the command:

    influx -username 'admin' -password 'password'

### Enabling the Firewall

Since InfluxDB can also be queried from the outside, it may be necessary to update the firewall rules to allow it to connect.

If your firewall is  UFW just type the following commands:

    sudo ufw allow 8086/tcp

This will allow TCP traffic on port 8086 used by InfluxDB for querying the database from outside.
