from django.db import models
from django.contrib.auth.models import User




# Try to configure using django user model

# class Student(models.Model):
#     name =
#     email =
#     profile_image =


class Chapter(models.Model):
    name = models.CharField(max_length=300)
    content = models.TextField()
    cover_image = models.ImageField(upload_to='chapters_cover_images')

    def __str__(self):
        return self.name


class Exam(models.Model):
    chapter = models.OneToOneField(Chapter, on_delete=models.CASCADE)
    question_number = models.PositiveIntegerField()
    marks = models.IntegerField()
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} Exam  - {}'.format(self.chapter.name, self.student)


class Question(models.Model):
    name = models.CharField(max_length=300)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    answer1=models.CharField(max_length=200)
    answer2=models.CharField(max_length=200)
    answer3=models.CharField(max_length=200)
    answer4=models.CharField(max_length=200)
    answer5=models.CharField(max_length=200)
    answer_options=(('Answer1','Answer1'),('Answer2','Answer2'),('Answer3','Answer3'),('Answer4','Answer4'),('Answer5','Answer5'))
    answers=models.CharField(max_length=200,choices=answer_options)

    def __str__(self):
        return '{}  Question  - In {}'.format(self.name, self.exam.chapter)


class Result(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}  Marks  - by  {} - in {}'.format(self.marks, self.student, self.exam.chapter)


class News(models.Model):
    title = models.CharField(max_length=300)
    content = content = models.TextField()
    published_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
