from django.urls import path, include
from .views import api_root, EmployeeViewSet, TaskViewSet, SnippetViewSet, SnippetHighlight
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'snippets', SnippetViewSet)

urlpatterns = [
    path('', api_root, name='api-root'),  # API root endpoint
    path('snippets/<int:pk>/highlight/', SnippetHighlight.as_view(), name='snippet-highlight'),
]

urlpatterns += router.urls