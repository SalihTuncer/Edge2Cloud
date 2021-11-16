from typing import Any, Dict
from client.mqtt_client import mqtt_client

import psutil
import time
import json
import argparse


def parse_arguments() -> Dict[str, Any]:
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument(
        '-ho', '--host', help='address of host | default: localhost', default='localhost', type=str)
    parser.add_argument(
        '-p', '--port', help='network port | default: 9001', default=9001, type=int)
    parser.add_argument(
        '-ri', '--reconnect_interval', help='connecting to broker | default: 3', default=3, type=float)
    parser.add_argument(
        '-pi', '--publish_interval', help='publishing messages | default: 1', default=1, type=float)
    parser.add_argument(
        '-x', '--publish_x', help='publishing interval min | default: 0.1', default=0.1, type=float)
    parser.add_argument(
        '-y', '--publish_y', help='publishing interval max | default: 100.0', default=100.0, type=float)
    return vars(parser.parse_args())


'''
Scale bytes to its proper format
source: https://stackoverflow.com/questions/1094841/get-human-readable-version-of-file-size
'''


def size_of(num: int, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            # return f'{num:3.1f}{unit}{suffix}'
            return float(f'{num:3.1f}'), f'{unit}{suffix}'
        num /= 1024.0
    return f'{num:.1f}Yi{suffix}'


'''
    return percentage usage of total cpu_processors of actual device
'''


def cpu_informations() -> None:
    return {
        'cpu_usage': psutil.cpu_percent(interval=0.025)
    }


'''
    return total memory and current used memory usage of actual device
'''


def memory_informations() -> None:
    mem = psutil.virtual_memory()
    return {
        # 'total_mem': size_of(mem.total),
        'used_mem': size_of(mem.used)
    }


'''
    return total read and write of all disks of actual device
'''


def disk_informations() -> None:
    io_counters = psutil.disk_io_counters()
    return {
        'disk_read': size_of(io_counters.read_count),
        'disk_write': size_of(io_counters.write_count)
    }


'''
    reaction of incoming messages from subscribed topics
    changes the interval in which we publish the messages
'''


def on_message(client, userdata, message) -> None:
    global config
    try:
        new_interval = float(message.payload.decode('utf-8'))
    except ValueError:
        return

    # we just accept values in the following range: [publish_x, publish_y]
    if (new_interval >= config['publish_x'] and new_interval <= config['publish_y']):
        config['publish_interval'] = new_interval
        print('Interval changed to', config['publish_interval'])


if __name__ == '__main__':
    # contains essential configurations for the mqtt client
    global config

    config = parse_arguments()

    client = mqtt_client(config['host'], config['port'],
                         config['reconnect_interval'])

    # subscribe so we can react to interval changes
    client.subcribe('health_monitoring_interval')
    client.set_on_message(on_message)

    # we permanently publish || should be changed in production
    while True:
        cpu = cpu_informations()
        mem = memory_informations()
        disk = disk_informations()
        # dump it in a JSON-object
        stats = json.dumps([cpu, mem, disk])
        # publish our JSON-object to the broker
        client.publish('health_monitoring', stats)
        # wait {publish_interval} seconds
        time.sleep(config['publish_interval'])
