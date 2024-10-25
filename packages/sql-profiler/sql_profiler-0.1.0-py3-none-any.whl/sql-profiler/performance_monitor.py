# sql_profiler/performance_monitor.py
import psutil
import logging

class PerformanceMonitor:
    def monitor(self):
        """
        Monitors system performance, including CPU, memory, and disk usage.
        """
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        disk_io = psutil.disk_io_counters()

        logging.info(f'CPU Usage: {cpu_usage}%, Memory Usage: {memory_info.percent}%, Disk I/O: {disk_io}')
        print(f'CPU Usage: {cpu_usage}%, Memory Usage: {memory_info.percent}%, Disk I/O: {disk_io}')
