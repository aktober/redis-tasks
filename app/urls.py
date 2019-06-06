from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet, basename='Tasks')

urlpatterns = [
    path('', views.IndexPage.as_view()),
    path('api/', include(router.urls)),
]
