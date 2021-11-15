# Edge2Cloud

Web-App with Node.js which shows the statistics of your device via MQTT and python. 

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/SalihTuncer/Edge2Cloud.git
   ```
2. Run the application
   ```sh
   docker-compose up -d
   ```

### Project Organization

      .
      ├── Architecture.drawio
      ├── Architecture.pdf
      ├── Dockerfile
      ├── LICENSE
      ├── README.md
      ├── docker-compose.yml
      ├── mosquitto
      │   └── mosquitto.conf
      ├── node
      │   ├── Dockerfile
      │   ├── app.js
      │   ├── js
      │   │   └── health_monitoring.js
      │   ├── monitoring.html
      │   ├── package-lock.json
      │   └── package.json
      ├── python
      │   ├── client
      │   │   ├── __pycache__
      │   │   │   └── mqtt_client.cpython-39.pyc
      │   │   └── mqtt_client.py
      │   └── health_monitoring.py
      └── requirements.txt

      6 directories, 17 files

### SLOC

      22 ./node/monitoring.html
     208 ./node/js/health_monitoring.js
      21 ./node/app.js
     118 ./python/health_monitoring.py
      55 ./python/client/mqtt_client.py
     424 total

state: 11/15/2021

