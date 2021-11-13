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
      ├── Dockerfile
      ├── LICENSE
      ├── README.md
      ├── docker-compose.yml
      ├── mosquitto
      │   └── mosquitto.conf
      ├── node
      │   ├── Dockerfile
      │   ├── app.js
      │   ├── index.html
      │   ├── package-lock.json
      │   └── package.json
      ├── python
      │   └── health_monitoring
      │       └── publisher.py
      └── requirements.txt

      4 directories, 12 files

### SLOC

      17 node/app.js
     173 node/index.html
      60 python/health_monitoring/publisher.py
     270 total

state: 11/13/2021

