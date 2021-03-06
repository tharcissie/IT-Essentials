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
    profile_image = models.ImageField(upload_to='profile_images',null=True, blank=True, default="me.png")
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
    content = models.TextField()
    cover_image = models.ImageField(upload_to='chapters_cover_images')
    file_to_download = models.FileField(upload_to='chapter_file', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    def snippet(self):
        return self.content[:80] + '...'


class Exam(models.Model):
    chapter = models.OneToOneField(Chapter, on_delete=models.CASCADE)


    def __str__(self):
        return self.chapter.name


class Question(models.Model):
    test = models.ForeignKey(Exam, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    score = models.PositiveIntegerField()
    answer1=models.CharField(max_length=200)
    answer2=models.CharField(max_length=200)
    answer3=models.CharField(max_length=200)
    answer4=models.CharField(max_length=200)
    answer5=models.CharField(max_length=200)
    answer_options=(('Answer1','Answer1'),('Answer2','Answer2'),('Answer3','Answer3'),('Answer4','Answer4'),('Answer5','Answer5'))
    answers=models.CharField(max_length=200,choices=answer_options)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}  <------>  {}'.format(self.name, self.exam.chapter)


class Result(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='results')
    test = models.ForeignKey(Exam,on_delete=models.CASCADE)
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

    def snippet(self):
        return self.content[:80] + '...'

