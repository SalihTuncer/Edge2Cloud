# Edge2Cloud

Stastics of youre Computer shown as a web app via MQTT, Python and Node. 

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/SalihTuncer/Edge2Cloud.git
   ```
2. Install pip packages
   ```sh
   pip install -r requirements.txt
   ```
3. Run mosquitto via
   ```sh
   /usr/local/sbin/mosquitto -c /usr/local/etc/mosquitto/mosquitto.conf
   ```
   the publisher via
   ```sh
   python python/publisher.py
   ```
   and the subscriber via
   ```sh
   python python/subscriber.py
   ```

### Project Organization

    ├── Dockerfile
    ├── LICENSE
    ├── README.md
    ├── node
    ├── python
    │   ├── plugins
    │   │   └── health_monitoring
    │   │       └── main.py
    │   ├── publisher.py
    │   ├── ressources
    │   └── subscriber.py
    └── requirements.txt

    5 directories, 7 files

### SLOC

    41 ./python/plugins/health_monitoring/main.py
    16 ./python/subscriber.py
    15 ./python/publisher.py
    72 total

state: 11/11/2021

