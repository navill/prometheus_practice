from django.contrib import admin
from django.urls import path
from django_prometheus.exports import ExportToDjangoView

from api.views import TaskListView, TaskDetailView
from system_reporter import collect_system_metrics


def CustomExportToDjangoView(request):
    collect_system_metrics()
    return ExportToDjangoView(request)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", TaskListView.as_view()),
    path("api/<int:pk>/", TaskDetailView.as_view()),
    path('prometheus-xyzabc/metrics', CustomExportToDjangoView, name="prometheus-django-metrics"),

]
