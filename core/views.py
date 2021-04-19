from core.models import Chapter, Exam, Question
from .models import *
from .forms import *
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required


def homepage(request):
    chapters = Chapter.objects.all()
    return render(request, 'core/homepage.html',{'chapters':chapters})

def chapter_content(request, name):
    chapter = get_object_or_404(Chapter, name=name)
    return render(request, 'core/chapter_content.html',{'chapter':chapter})


def take_exam(request, id):
    exam = Exam.objects.get(chapter=id)
    number_of_questions = Question.objects.all().filter(exam=exam).count()
    questions = Question.objects.filter(exam=exam)
    total_marks = 0

    for question in questions:
        total_marks = total_marks + question.score

    return render(request, 'core/take_exam.html',{'exam':exam, 'number_of_questions':number_of_questions, 'total_marks':total_marks ,'questions':questions})




def start_exam(request, id):
    if request.user.is_authenticated:
        exam = Exam.objects.get(id=id)
        questions = Question.objects.filter(exam=exam)

        if request.method=='POST':
            pass
        response = render(request, 'core/start_exam.html',{'exam':exam, 'questions':questions})
        response.set_cookie('exam_id',exam.id)
        return response
    return redirect('login')
  



def calculate_marks(request):
    if request.COOKIES.get('exam_id') is not None:
        exam_id = request.COOKIES.get('exam_id')
        exam = Exam.objects.get(id=exam_id)
        
        total_marks=0
        questions = Question.objects.all().filter(exam=exam)
        for i in range(len(questions)):
            
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answers
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].score
        student = StudentProfile.objects.get(id=request.user.id)
        result = Result()
        result.marks=total_marks
        result.exam=exam
        result.student=student
        result.save()

        return redirect('homepage')





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
















def take_test(request, chapter_id):
    test = Test.objects.filter(chapter=chapter_id)
    questions = QuestionOne.objects.all().filter(test=test)

    
    return render(request, 'take_test.html', {'questions':questions})
