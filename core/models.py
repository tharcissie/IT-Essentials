from django.db import models

# Create your models here.

class Chapter(models.Model):
    name = models.CharField(max_length=30)
    content =
    image =

class Exam(models.Model):
    chapter =
    marks =

class Question(models.Model):
    name =
    exam =
    score =
    answer =

class Student(models.Model):
    name =
    email =
    profile_image =

class News(models.Model):
    title =
    content =
    published_date =
