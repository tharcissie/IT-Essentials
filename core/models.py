from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.conf import settings
from autoslug import AutoSlugField



class UserProfileManager(BaseUserManager):

    def create_user(self, email, name, profile_image, password=None):
        if not email:
            raise ValueError('Student must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name,profile_image=profile_image)
        
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, name, password):
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class StudentProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=30)
    name = models.CharField(max_length=250)
    profile_image = models.ImageField(upload_to='profile_images')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name



class Chapter(models.Model):
    name = models.CharField(max_length=300)
    slug = AutoSlugField(populate_from='name')
    content = models.TextField()
    cover_image = models.ImageField(upload_to='chapters_cover_images')
    file_to_download = models.FileField(upload_to='chapter_file', blank=True, null=True)

    def __str__(self):
        return self.name

    def snippet(self):
        return self.content[:150]


class Exam(models.Model):
    chapter = models.OneToOneField(Chapter, on_delete=models.CASCADE)
    question_number = models.PositiveIntegerField()
    marks = models.IntegerField()
    # student = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} Exam'.format(self.chapter.name)


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
        return '{}  <------>  {}'.format(self.name, self.exam.chapter)


class Result(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
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














class Test(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    chapter = models.OneToOneField(Chapter, on_delete=models.CASCADE)
    tested_date = models.DateTimeField(auto_now_add=True)
    avg = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{} Test'.format(self.chapter.name)

class QuestionOne(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question_name = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return '{} <-------------> {}'.format(self.question_name, self.test.chapter.name)


class Answer(models.Model):
    answer = models.CharField(max_length=300)
    is_true = models.BooleanField(default=False)
    question = models.ForeignKey(QuestionOne, on_delete=models.CASCADE)

    def __str__(self):
        return '{} <------------> {}'.format(self.answer, self.question.question_name)