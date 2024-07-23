import prometheus_client
import psutil
from django.conf import settings

SYSTEM_USAGE = prometheus_client.Gauge('system_usage',
                                       'current system resource usage',
                                       ['resource_type'],
                                       namespace=settings.PROMETHEUS_METRIC_NAMESPACE)


def collect_system_metrics():
    # mac OS에서는 prometheus_client.process_collector.ProcessCollector()가 활성화되지 않음
    # (linux의 /proc/stat을 기준으로 실행되기 때문)
    # mac에서는 직접 데이터를 수집하는 메트릭을 추가해야함
    SYSTEM_USAGE.labels('CPU').set(psutil.cpu_percent())
    SYSTEM_USAGE.labels('Memory').set(psutil.virtual_memory()[2])
