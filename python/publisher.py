# publisher
import paho.mqtt.client as mqtt
import time
import psutil
import json 

'''
Scale bytes to its proper format
source: https://stackoverflow.com/questions/1094841/get-human-readable-version-of-file-size
'''
def size_of(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return f'{num:3.1f}{unit}{suffix}'
        num /= 1024.0
    return f'{num:.1f}Yi{suffix}'

def cpu_informations():
    return {
		'cpu_usage': psutil.cpu_percent(interval=0.025)
	}

def memory_informations():
	mem = psutil.virtual_memory()
	return {
		'total_mem': size_of(mem.total),
		'used_mem': size_of(mem.used)
	}

def disk_informations():
	io_counters = psutil.disk_io_counters()
	return {
		'disk_read': size_of(io_counters.read_count),
		'disk_write': size_of(io_counters.write_count)
	}

'''
def temperature_informations():
	return {
		'Temperature:' psutil.sensors_temperatures()
	}
'''

if __name__ == '__main__':

    client = mqtt.Client(transport='websockets')
    client.connect('localhost', 9001)

    interval = 1

    while True:
        cpu = cpu_informations()
        mem = memory_informations()
        disk = disk_informations()
        stats = json.dumps([cpu, mem, disk])
        
        client.publish('health_monitoring', stats)
        print(f'health_monitoring: {stats}')
        time.sleep(interval)
