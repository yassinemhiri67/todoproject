"""
Views for the todo app: provides API endpoints for Employees, Tasks, and Snippets.
Follows company best practices for Django backend development.
"""

import logging

from django.shortcuts import get_object_or_404, render
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.renderers import StaticHTMLRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from django.utils import timezone
from rest_framework.decorators import action

from .models import Employee, Snippet, Task
from .serializers import EmployeeSerializer, SnippetSerializer, TaskSerializer

logger = logging.getLogger(__name__)

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission: Only superusers can modify, others have read-only access.
    """
    def has_permission(self, request, view):
        # SAFE_METHODS are GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_superuser

@api_view(['GET'])
def api_root(request, format=None):
    """API root endpoint providing links to main resources."""
    return Response({
        'employees': reverse('employee-list', request=request, format=format),
        'tasks': reverse('task-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format),
    })

class EmployeeViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Employee objects."""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['department', 'birth_date', 'name', 'email']

class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Task objects."""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['status', 'employee', 'due_date', 'title']

    @action(detail=True, methods=['post'])
    def lock(self, request, pk=None):
        task = self.get_object()
        employee = getattr(request.user, 'employee', None)
        if not employee:
            return Response({'detail': 'User is not associated with an employee.'}, status=400)
        if task.locked_by and task.locked_by != employee:
            return Response({'detail': 'Task is already locked by another user.'}, status=403)
        task.locked_by = employee
        task.locked_at = timezone.now()
        task.save()
        return Response({'detail': 'Task locked.'})

    @action(detail=True, methods=['post'])
    def unlock(self, request, pk=None):
        task = self.get_object()
        employee = getattr(request.user, 'employee', None)
        if not employee:
            return Response({'detail': 'User is not associated with an employee.'}, status=400)
        if task.locked_by != employee:
            return Response({'detail': 'You do not own the lock.'}, status=403)
        task.locked_by = None
        task.locked_at = None
        task.save()
        return Response({'detail': 'Task unlocked.'})

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        employee = getattr(request.user, 'employee', None)
        if task.locked_by and task.locked_by != employee:
            return Response({'detail': 'Task is locked by another user.'}, status=403)
        return super().update(request, *args, **kwargs)

class SnippetViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Snippet objects."""
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['task', 'language', 'created']

    @action(detail=True, methods=['post'])
    def lock(self, request, pk=None):
        snippet = self.get_object()
        employee = getattr(request.user, 'employee', None)
        if not employee:
            return Response({'detail': 'User is not associated with an employee.'}, status=400)
        if snippet.locked_by and snippet.locked_by != employee:
            return Response({'detail': 'Snippet is already locked by another user.'}, status=403)
        snippet.locked_by = employee
        snippet.locked_at = timezone.now()
        snippet.save()
        return Response({'detail': 'Snippet locked.'})

    @action(detail=True, methods=['post'])
    def unlock(self, request, pk=None):
        snippet = self.get_object()
        employee = getattr(request.user, 'employee', None)
        if not employee:
            return Response({'detail': 'User is not associated with an employee.'}, status=400)
        if snippet.locked_by != employee:
            return Response({'detail': 'You do not own the lock.'}, status=403)
        snippet.locked_by = None
        snippet.locked_at = None
        snippet.save()
        return Response({'detail': 'Snippet unlocked.'})

    def update(self, request, *args, **kwargs):
        snippet = self.get_object()
        employee = getattr(request.user, 'employee', None)
        if snippet.locked_by and snippet.locked_by != employee:
            return Response({'detail': 'Snippet is locked by another user.'}, status=403)
        return super().update(request, *args, **kwargs)

class SnippetHighlightView(APIView):
    """API view for returning highlighted HTML of a snippet."""
    renderer_classes = [StaticHTMLRenderer]
    def get(self, request, pk, format=None):
        """Return highlighted HTML for a snippet, or 404 if not found."""
        try:
            snippet = Snippet.objects.get(pk=pk)
            return Response(snippet.highlighted)
        except Snippet.DoesNotExist:
            logger.warning(f"Snippet with pk={pk} not found")
            return Response({'error': 'Snippet not found.'}, status=404)

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner
        return hasattr(obj, 'owner') and obj.owner == request.user



