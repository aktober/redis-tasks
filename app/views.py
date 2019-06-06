from django.views.generic import TemplateView
from rest_framework import viewsets
import redis
from rest_framework.decorators import action
from rest_framework.response import Response

from app.serializers import TaskSerializer

r = redis.Redis(host='localhost', port=6379, db=0)


class IndexPage(TemplateView):
    template_name = 'index.html'


class TaskViewSet(viewsets.ViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    serializer_class = TaskSerializer

    def list(self, request):
        tasks = r.lrange('tasks', 0, -1)
        return Response({'tasks': tasks})

    def create(self, request, *args, **kwargs):
        d = request.data.dict()
        r.rpush('tasks', d['text'])
        tasks = r.lrange('tasks', 0, -1)
        return Response({'tasks': tasks})

    @action(detail=False, methods=['delete'], name='Delete all tasks')
    def destroy_all(self, request):
        r.delete('tasks')
        return Response({'tasks': []})

    @action(detail=False, methods=['delete'], name='Bulk delete tasks')
    def bulk_destroy(self, request):
        print(request.data)
        tasks = request.data.getlist('ids[]')
        tasks = [int(task) for task in tasks]

        for task in tasks:
            val = r.lindex('tasks', task)
            r.lrem('tasks', 1, val)

        tasks = r.lrange('tasks', 0, -1)
        return Response({'tasks': tasks})
