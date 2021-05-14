from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import AuthenticationForm
from .models import *




class SignupForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput(attrs={'class':'form-control','label':'Password'}))

    class Meta:
        model = StudentProfile
        fields = ('email','name','profile_image','password1','password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = StudentProfile
        fields = ('email', 'name','profile_image','is_active', 'is_staff', 'is_superuser')
    
    def clean_password(self):
        return self.initial["password"]

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['name','content','cover_image','file_to_download']


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title','content']



class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['chapter']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['test','score','name','answer1','answer2','answer3','answer4','answer5','answers']



