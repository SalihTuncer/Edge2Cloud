from client.mqtt_client import mqtt_client

import psutil
import time
import json 

publish_interval = 1
# publish range from
publish_x = 0.1
# to 
publish_y = 100

'''
Scale bytes to its proper format
source: https://stackoverflow.com/questions/1094841/get-human-readable-version-of-file-size
'''
def size_of(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            # return f'{num:3.1f}{unit}{suffix}'
            return float(f'{num:3.1f}'), f'{unit}{suffix}'
        num /= 1024.0
    return f'{num:.1f}Yi{suffix}'

'''
    return percentage usage of total cpu_processors of actual device
'''
def cpu_informations():
    return {
		'cpu_usage': psutil.cpu_percent(interval=0.025)
	}

'''
    return total memory and current used memory usage of actual device
'''
def memory_informations():
	mem = psutil.virtual_memory()
	return {
		'total_mem': size_of(mem.total),
		'used_mem': size_of(mem.used)
	}

'''
    return total read and write of all disks of actual device
'''
def disk_informations():
	io_counters = psutil.disk_io_counters()
	return {
		'disk_read': size_of(io_counters.read_count),
		'disk_write': size_of(io_counters.write_count)
	}

'''
    reaction of incoming messages from subscribed topics
    changes the interval in which we publish the messages
'''
def on_message(client, userdata, message):
    global publish_interval, publish_x, publish_y
    value = float(message.payload.decode('utf-8'))

    # we just accept values in the following range: [publish_x, publish_y]
    if (value >= publish_x and value <= publish_y):
        publish_interval = value
        print(f'interval changed to {publish_interval}')
    
     

if __name__ == '__main__':

    host = 'localhost'
    port = 9001

    client = mqtt_client(host, port)

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
        time.sleep(publish_interval)