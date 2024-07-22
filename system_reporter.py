import prometheus_client
import psutil

SYSTEM_USAGE = prometheus_client.Gauge('prometheus_practice_system_usage',
                                       'current system resource usage',
                                       ['resource_type'])


def collect_system_metrics():
    SYSTEM_USAGE.labels('CPU').set(psutil.cpu_percent())
    SYSTEM_USAGE.labels('Memory').set(psutil.virtual_memory()[2])
    # print(psutil.virtual_memory())
