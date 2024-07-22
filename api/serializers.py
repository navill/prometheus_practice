from rest_framework import serializers

from api.models import TaskModel


class TaskModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = "__all__"
