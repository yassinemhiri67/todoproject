from rest_framework import serializers
from .models import Task, Employee, Snippet
from datetime import date
from rest_framework.reverse import reverse


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
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
        request = self.context.get('request')
        return [
            {
                'name': task.title,
                'url': reverse('task-detail', args=[task.pk], request=request)
            }
            for task in obj.tasks.all()
        ]

    def validate_email(self, value):
        # Only allow company emails
        if not value.endswith('@yourcompany.com'):
            raise serializers.ValidationError("Email must be a company email address.")
        return value

    def validate_salary(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Salary cannot be negative.")
        return value

class TaskSerializer(serializers.HyperlinkedModelSerializer):
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
        if obj.employee:
            request = self.context.get('request')
            return {
                'name': obj.employee.name,
                'url': reverse('employee-detail', args=[obj.employee.pk], request=request)
            }
        return None

    def validate_due_date(self, value):
        if value and value < date.today():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value

    def validate_priority(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Priority must be between 1 and 5.")
        return value

    def get_employee_name(self, obj):
        return obj.employee.name if obj.employee else None

    def get_is_overdue(self, obj):
        from datetime import datetime
        if obj.due_date and not obj.completed:
            return obj.due_date < datetime.now()
        return False

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
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
        