import psutil

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
	print('CPU INFORMATIONS:\n')
	print(f'Total CPU Usage: {psutil.cpu_percent(interval=0.025)}%\n')

def memory_informations():
	print('MEMORY INFORMATIONS:\n')
	# Memory details
	mem = psutil.virtual_memory()
	print(f'Total: {size_of(mem.total)}')
	print(f'Used: {size_of(mem.used)} ({mem.percent}%)')
	print(f'Available: {size_of(mem.available)}\n')

def disk_informations():
	print('DISK INFORMATIONS:\n')
	# informations about the partitions are not necessary
	io_counters = psutil.disk_io_counters()
	print(f'Read: {size_of(io_counters.read_count)}')
	print(f'Write: {size_of(io_counters.write_count)}\n')

def temperature_informations():
	print('TEMPERATURE INFORMATIONS:\n')
	print(psutil.cpu_stats.__dict__)

if __name__ == '__main__':
	cpu_informations()
	memory_informations()
	disk_informations()
	temperature_informations()
