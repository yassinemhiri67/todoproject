from django.db import models
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles

# Task status constants
TASK_STATUS_TODO = 'TODO'
TASK_STATUS_INPROGRESS = 'INPROGRESS'
TASK_STATUS_DONE = 'DONE'
TASK_STATUS_CHOICES = [
    (TASK_STATUS_TODO, 'To Do'),
    (TASK_STATUS_INPROGRESS, 'In Progress'),
    (TASK_STATUS_DONE, 'Done'),
]

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

class Employee(models.Model):
    """Model representing an employee in the company."""
    name = models.CharField(max_length=100, help_text="Full name of the employee.")
    email = models.EmailField(unique=True, help_text="Unique company email address.")
    birth_date = models.DateField(null=True, blank=True, help_text="Birth date of the employee.")
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True, help_text="Profile picture.")
    bio = models.TextField(blank=True, help_text="Short biography.")
    is_active = models.BooleanField(default=True, help_text="Is the employee currently active?")
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Monthly salary.")
    department = models.CharField(
        max_length=100,
        choices=[('HR', 'HR'), ('ENG', 'Engineering'), ('MKT', 'Marketing')],
        default='ENG',
        help_text="Department of the employee."
    )

    def __str__(self):
        """String for representing the Employee object."""
        return self.name

class Task(models.Model):
    """Model representing a task assigned to an employee."""
    employee = models.ForeignKey(Employee, related_name='tasks', on_delete=models.CASCADE, null=True, blank=True, help_text="Employee assigned to the task.")
    title = models.CharField(max_length=255, help_text="Title of the task.")
    description = models.TextField(blank=True, help_text="Detailed description of the task.")
    completed = models.BooleanField(default=False, help_text="Is the task completed?")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Task creation timestamp.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Task last update timestamp.")
    due_date = models.DateTimeField(null=True, blank=True, help_text="Due date for the task.")
    priority = models.IntegerField(default=1, help_text="Priority of the task (1-5).")
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True, help_text="Related file attachment.")
    tags = models.CharField(max_length=255, blank=True, help_text='Comma-separated tags')
    status = models.CharField(
        max_length=20,
        choices=TASK_STATUS_CHOICES,
        default=TASK_STATUS_TODO,
        help_text="Current status of the task."
    )

    def __str__(self):
        """String for representing the Task object."""
        return self.title

class Snippet(models.Model):
    """Model representing a code snippet related to a task."""
    task = models.ForeignKey('Task', related_name='snippets', on_delete=models.CASCADE, help_text="Task related to this snippet.")
    code = models.TextField(help_text="The code content of the snippet.")
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100, help_text="Programming language of the snippet.")
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100, help_text="Style for code highlighting.")
    linenos = models.BooleanField(default=False, help_text="Show line numbers in the highlighted code?")
    created = models.DateTimeField(auto_now_add=True, help_text="Snippet creation timestamp.")

    class Meta:
        ordering = ['created']
        verbose_name = "Snippet"
        verbose_name_plural = "Snippets"

    @property
    def highlighted(self):
        """Returns the highlighted HTML representation of the code snippet."""
        lexer = get_lexer_by_name(self.language)
        formatter = HtmlFormatter(style=self.style, full=True, linenos=self.linenos)
        return highlight(self.code, lexer, formatter)