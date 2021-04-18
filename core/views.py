from .models import *
from .forms import *
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required


def homepage(request):
    chapters = Chapter.objects.all()
    return render(request, 'core/homepage.html',{'chapters':chapters})

def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST or None,files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            form = SignupForm()

    return render(request, 'core/signup.html',{'form':form})

@login_required(login_url='login')
def account(request):
    chapters = Chapter.objects.all()
    return render(request, 'core/account.html', {'chapters':chapters})

@login_required(login_url='login')
def chapter(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    return render(request, 'core/chapter.html', {'chapter':chapter})

@login_required(login_url='login')
def exam(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    question = Question.objects.filter(exam=exam)
    return render(request, 'core/exam.html', {'exam':exam,'question':question})
