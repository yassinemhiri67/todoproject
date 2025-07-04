from django.db import models
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=bool(True))
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    department = models.CharField(
        max_length=100,
        choices=[('HR', 'HR'), ('ENG', 'Engineering'), ('MKT', 'Marketing')],
        default='ENG'
    )

    def __str__(self):
        return self.name
# Create your models here.
class Task(models.Model):
    employee = models.ForeignKey(Employee, related_name='tasks', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=bool(False))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(default=int(1))
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)
    tags = models.CharField(max_length=255, blank=True, help_text='Comma-separated tags')
    status = models.CharField(
        max_length=20,
        choices=[('TODO', 'To Do'), ('INPROGRESS', 'In Progress'), ('DONE', 'Done')],
        default='TODO'
    )

    def __str__(self):
        return self.title

class Snippet(models.Model):
    task = models.ForeignKey('Task', related_name='snippets', on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    linenos = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    @property
    def highlighted(self):
        lexer = get_lexer_by_name(self.language)
        formatter = HtmlFormatter(style=self.style, full=True, linenos=self.linenos)
        return highlight(self.code, lexer, formatter)