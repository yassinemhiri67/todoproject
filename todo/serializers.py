from datetime import date
from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Employee, Snippet, Task

class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Employee model."""
    tasks = serializers.SerializerMethodField()
    class Meta:
        model = Employee
        fields = [
            'url',
            'id',
            'name',
            'email',
            'birth_date',
            'profile_picture',
            'bio',
            'is_active',
            'salary',
            'department',
            'tasks',
        ]
    def get_tasks(self, obj):
        """Return a list of tasks for the employee."""
        request = self.context.get('request')
        return [
            {
                'name': task.title,
                'url': reverse('task-detail', args=[task.pk], request=request)
            }
            for task in obj.tasks.all()
        ]

    def validate_email(self, value):
        """Validate that the email is a company email address."""
        if not value.endswith('@yourcompany.com'):
            raise serializers.ValidationError("Email must be a company email address.")
        return value

    def validate_salary(self, value):
        """Validate that the salary is not negative."""
        if value is not None and value < 0:
            raise serializers.ValidationError("Salary cannot be negative.")
        return value

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Task model."""
    employee = serializers.HyperlinkedRelatedField(
        queryset=Employee.objects.all(),
        view_name='employee-detail'
    )
    employee_info = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'url',
            'id',
            'employee',
            'employee_info',
            'title',
            'description',
            'completed',
            'created_at',
            'updated_at',
            'due_date',
            'priority',
            'attachment',
            'tags',
            'status',
        ]
 
    def get_employee_info(self, obj):
        """Return employee info for the task."""
        if obj.employee:
            request = self.context.get('request')
            return {
                'name': obj.employee.name,
                'url': reverse('employee-detail', args=[obj.employee.pk], request=request)
            }
        return None

    def validate_due_date(self, value):
        """Validate that the due date is not in the past."""
        if value and value < date.today():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value

    def validate_priority(self, value):
        """Validate that the priority is between 1 and 5."""
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Priority must be between 1 and 5.")
        return value

    def get_employee_name(self, obj):
        """Return the employee's name for the task."""
        return obj.employee.name if obj.employee else None

    def get_is_overdue(self, obj):
        """Return True if the task is overdue and not completed."""
        from datetime import datetime
        if obj.due_date and not obj.completed:
            return obj.due_date < datetime.now()
        return False

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Snippet model."""
    highlighted = serializers.ReadOnlyField()
    class Meta:
        model = Snippet
        fields = [
            'url',
            'id',
            'task',
            'code',
            'language',
            'style',
            'linenos',
            'created',
            'highlighted',
        ]
        