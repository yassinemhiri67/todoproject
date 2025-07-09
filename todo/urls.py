"""URL configuration for the todo app."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (EmployeeViewSet, SnippetHighlightView, SnippetViewSet, TaskViewSet, api_root)

# Set up DRF router
router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'snippets', SnippetViewSet)

urlpatterns = [
    path('', api_root, name='api-root'),  # API root endpoint
    path('snippets/<int:pk>/highlight/', SnippetHighlightView.as_view(), name='snippet-highlight'),
]

# Include router-generated URLs
urlpatterns += router.urls