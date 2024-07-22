from rest_framework.generics import ListAPIView, RetrieveAPIView

from api.models import TaskModel
from api.serializers import TaskModelSerializer


# Create your views here.
class TaskListView(ListAPIView):
    queryset = TaskModel.objects.all()
    serializer_class = TaskModelSerializer


class TaskDetailView(RetrieveAPIView):
    queryset = TaskModel.objects.all()
    serializer_class = TaskModelSerializer
    lookup_field = "pk"
