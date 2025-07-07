from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.renderers import StaticHTMLRenderer
from .models import Task, Employee, Snippet
from .serializers import TaskSerializer, EmployeeSerializer, SnippetSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from rest_framework import permissions
from django.shortcuts import render, get_object_or_404

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    The request is authenticated as a superuser, or is a read-only request.
    """
    def has_permission(self, request, view):
        # SAFE_METHODS are GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_superuser

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'employees': reverse('employee-list', request=request, format=format),
        'tasks': reverse('task-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format),
    })

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['department', 'birth_date', 'name', 'email']

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['status', 'employee', 'due_date', 'title']  # Add fields you want to filter by

class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['task', 'language', 'created']

class SnippetHighlight(APIView):
    renderer_classes = [StaticHTMLRenderer]
    def get(self, request, pk, format=None):
        snippet = Snippet.objects.get(pk=pk)
        return Response(snippet.highlighted)

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner
        return obj.owner == request.user



