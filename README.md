# django-prometheus
- https://github.com/korfuri/django-prometheus: django에서 사용할 수 있는 Prometheus 연동 라이브러리
  - prometheus_client를 의존하고 있음
  - https://prometheus.github.io/client_python/: 메트릭 관련 라이브러리(prometheus_client)
    - 주요 메트릭 클래스를 가지고있음. 컨택스트 매니저, 데코레이터로 활용 가능
    

- 실행 순서(django start)

  1. django.apps.registry.Apps이 호출되면서 INSTALLED_APP에 등록된 앱들의 AppConfig 클래스 호출

     ```python
     INSTALLED_APPS = [
     		...
         'django_prometheus',
       	...
     ]
     ```

  2. app_config.ready() 호출

     ```python
     class Apps:
       	def populate():
             ...
             # Phase 3: run ready() methods of app configs.
             for app_config in self.get_app_configs():
                 app_config.ready()
     ```

  3. DjangoPrometheusConfig(AppConfig).ready() 호출 -> SetupPrometheusExportsFromConfig() 호출
     - settings에 정의된 port(PROMETHEUS_METRICS_EXPORT_PORT, PROMETHEUS_METRICS_EXPORT_PORT_RANGE), address(PROMETHEUS_METRICS_EXPORT_ADDRESS)를 바탕으로 wsgi 서버 시작(daemon thread)

   - 새로 생성한 Metric 인스턴스는 별도로 등록하지 않아도 prometheus_client.registry.REGISTRY()에 담겨있음
     - 수집하려는 데이터는 호출 시점까지 업데이트 되어있어야함

- Grafana 연동

  grafana 대시보드는 오픈소스 이용(https://grafana.com/grafana/dashboards/9528-django-prometheus/)
  ![image](https://github.com/user-attachments/assets/97b5061f-b495-43fc-af6d-b06baf699cc4)

### Trouble shooting

- docker-compose 실행 시 django 컨테이너만 실행되지 않고 `Error: That port is already in use.` 에러

  => django와 prometheus 실행 포트를 다르게 설정해야함

  - django가 실행될 때 prometheus도 지정된 포트로 데몬 서버를 띄움

    - django 메인 스레드 실행(socket: 8000) & prometheus의 SetupPrometheusEndpointOnPort 함수 실행(socket: 8000)

      ![image](https://github.com/user-attachments/assets/bc290645-8f8d-46d1-aeaa-57629707149b)

    - 개발(mac) 환경에서는 같은 포트로 실행하더라도 다른 타입의 동일한 포트로 프로세스가 실행됨(놓친 부분)



- system 자원(cpu, memory 등) 수집 활성화

  => mac에서는 prometheus_client.ProcessCollector를 지원하지 않음

  - prometheus_client.ProcessCollector 실행은 리눅스의 /proc/stat 파일을 읽어서 실행됨

  - 맥에서 시스템 자원을 확인하기 위해 별도의 메트릭 코드를 추가

    ```python
    # system_reporter.py
    import prometheus_client
    import psutil
    from django.conf import settings
    
    SYSTEM_USAGE = prometheus_client.Gauge('system_usage',
                                           'current system resource usage',
                                           ['resource_type'],
                                           namespace=settings.PROMETHEUS_METRIC_NAMESPACE)
    
    def collect_system_metrics():
        SYSTEM_USAGE.labels('CPU').set(psutil.cpu_percent())
        SYSTEM_USAGE.labels('Memory').set(psutil.virtual_memory()[2])
    
    # urls.py
    from django_prometheus.exports import ExportToDjangoView
    from system_reporter import collect_system_metrics
    
    
    def ExportToDjangoViewForMac(request):
        collect_system_metrics()
        return ExportToDjangoView(request)
    
    urlpatterns = [
        path('prometheus-xyzabc/metrics/for-mac', ExportToDjangoViewForMac, name="prometheus-django-metrics-for-mac"),
    ]
    ```
  
  - Custom Collector를 추가하는 방법
  
    ```python
    # system_collector.py
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
    
    # prometheus_practice/__init__.py
    from system_collector import SystemResourceCollector
    
    # register 실행을 위한 임포팅
    __all__ = [
        "SystemResourceCollector"
    ]
    
    
    ```
  
    

