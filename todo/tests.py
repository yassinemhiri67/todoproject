"""Test suite for the todo app."""

from django.test import TestCase
from .models import Employee

class EmployeeModelTest(TestCase):
    """Test the Employee model."""
    def test_str_returns_name(self):
        """__str__ should return the employee's name."""
        employee = Employee.objects.create(name='John Doe', email='john@yourcompany.com')
        self.assertEqual(str(employee), 'John Doe')
