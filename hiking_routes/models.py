from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator

class Post(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    image = models.ImageField(upload_to='hiking_route/images/%Y/%M/%D/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    max_member = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    date = models.DateField(max_length=50, null=False, blank=False)
    start_point = models.CharField(max_length=30)
    end_point = models.CharField(max_length=30)

    def __str__(self):
        return f'[{self.pk}]-{self.title} - {self.author}'
    def get_absolute_url(self):
        return f'/routes/{self.pk}'

class Participate(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)