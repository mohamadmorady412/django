from django.db import models

# Create your models here.

class Post(models.Model):
    """this id a class to defin posts of blog"""
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=250)
    content = models.TextField()
    status = models.BooleanField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name