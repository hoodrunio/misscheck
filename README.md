# misscheck
Application to get missing block counters from cosmos chains. 

We are using influxdb for storing time series data, grafana
for visualization, python scripts for fetching data.

We will use nginx for web server.

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


## Grafana

Grafana is a free, open-source, and composable observability and data
visualization platform. It is used for monitoring, analysis, and
visualization of real-time system data.


### Add Grafana Repository

By default, the Grafana package is not included in the Ubuntu 20.04
default repository. So you will need to add the Grafana official
repository to your system.

First, install all required dependencies using the following command:

    sudo apt-get install wget curl gnupg2 apt-transport-https software-properties-common -y

Next, download and add the Grafana GPG key with the following command:

    wget -q -O - https://packages.grafana.com/gpg.key | apt-key add -

Next, add the Grafana repository to APT using the following command:

    echo "deb https://packages.grafana.com/oss/deb stable main" | tee -a /etc/apt/sources.list.d/grafana.list

Once the repository is added to your system, you can update it with the following command:

    apt-get update -y

### Install Grafana

Now, you can install the Grafana by running the following command:

    apt-get install grafana -y

Once the Grafana package is installed, verify the Grafana version with the following command:

    grafana-server -v

Now, start the Grafana service and enable it to start at system reboot:

    systemctl start grafana-server
    systemctl enable grafana-server

You can now check the status of the Grafana with the following command:

    systemctl status grafana-server

At this point, Grafana is started and listens on port 3000. You can check it with the following command:

    ss -antpl | grep 3000

You should see the following output:

    LISTEN    0     4096        *:3000     *:*        users:(("grafana-server",pid=5432,fd=8))                                       


### Configure Nginx as a Reverse Proxy for Grafana

Next, you will need to install the Nginx as a reverse proxy for Grafana.
First, install the Nginx package using the following command:

    apt-get install nginx -y

Once the Nginx is installed, create an Nginx virtual host configuration file:

    nano /etc/nginx/conf.d/grafana.conf

Add the following lines, don't forget to change the hostname:

    Server {
        server_name grafana.example.com;
        listen 80;
        access_log /var/log/nginx/grafana.log;

        location / {
                proxy_pass http://localhost:3000;
                proxy_set_header Host $http_host;
                proxy_set_header X-Forwarded-Host $host:$server_port;
                proxy_set_header X-Forwarded-Server $host;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }

Save and close the file then verify the Nginx configuration file using the following command:

    nginx -t

You will get the following output:

    nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
    nginx: configuration file /etc/nginx/nginx.conf test is successful

Finally, restart the Nginx service to apply the changes:
 
    systemctl restart nginx

### Access Grafana Dashboard

Now, open your web browser and access the Grafana dashboard using the URL
http://grafana.example.com. You will be redirected to the Grafana login page.

Provide default admin username and password as admin/admin and click on
the Log in button. You should see the Grafana password change screen.


Change your default password and click on the Submit button. You should
see the Grafana dashboard on the following screen.


