from django.contrib import admin
from django.urls import path
from django_prometheus.exports import ExportToDjangoView

from api.views import TaskListView, TaskDetailView
from system_reporter import collect_system_metrics


def ExportToDjangoViewForMac(request):
    collect_system_metrics()
    return ExportToDjangoView(request)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/<int:pk>/", TaskDetailView.as_view()),
    path("api/", TaskListView.as_view()),
    path('prometheus-xyzabc/metrics/for-mac', ExportToDjangoViewForMac, name="prometheus-django-metrics-for-mac"),
    path('prometheus-xyzabc/metrics/', ExportToDjangoView, name="prometheus-django-metrics"),
]
