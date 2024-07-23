from typing import Iterable

import psutil
from prometheus_client import Metric
from prometheus_client.metrics_core import GaugeMetricFamily
from prometheus_client.registry import Collector, REGISTRY


class SystemResourceCollector(Collector):
    def collect(self) -> Iterable[Metric]:
        resource_usage = GaugeMetricFamily('system_resource_usage', "system resource usage",
                                           labels=["cpu", "memory"])
        resource_usage.add_metric(["cpu"], psutil.cpu_percent())
        resource_usage.add_metric(["memory"], psutil.virtual_memory()[2])
        yield resource_usage


REGISTRY.register(SystemResourceCollector())
