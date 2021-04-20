from core.models import Chapter, Exam, Question
from .models import *
from .forms import *
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from .filters import QuestionFilter, ResultFilter




def homepage(request):
    chapters = Chapter.objects.all()
    return render(request, 'core/homepage.html',{'chapters':chapters})

def chapter_content(request, slug):
    chapter = get_object_or_404(Chapter, slug=slug)
    return render(request, 'core/chapter_content.html',{'chapter':chapter})


def take_exam(request, id):
    exam = Exam.objects.get(chapter=id)
    exams = Exam.objects.all()
    number_of_questions = Question.objects.all().filter(exam=exam).count()
    questions = Question.objects.filter(exam=exam)
    total_marks = 0

    for question in questions:
        total_marks = total_marks + question.score

    return render(request, 'core/exam.html',{'exam':exam, 'number_of_questions':number_of_questions, 'total_marks':total_marks ,'questions':questions, 'exams':exams})


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

def view_result(request):
    exams = Exam.objects.all()
    return render(request,'core/view-results.html',{'exams':exams})

def results(request, id):
    exam=Exam.objects.get(id=id)
    student = get_object_or_404(StudentProfile, id=id)
    result= Result.objects.all().filter(exam=exam).filter(student=student)
    return render(request,'core/result.html',{'result':result})

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

        return redirect('view_result')



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
def chapter(request, id):
    chapter = get_object_or_404(Chapter, id=id)
    chapters = Chapter.objects.all()
    return render(request, 'core/chapter.html', {'chapter':chapter, 'chapters':chapters})

def add_chapter(request):
    form = ChapterForm()
    if request.method == 'POST':
        form = ChapterForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.name =  request.POST['name']
            form.content =  request.POST['content']
            form.cover_image =  request.FILES['cover_image']   
            form.file_to_download =  request.FILES['file_to_download']   
            form.save()
            return redirect('view_chapters')
        else:
            form = ChapterForm()
    return render(request, 'core/add_chapter.html')


def add_exam(request):
    exam_form = ExamForm()
    if request.method == 'POST':
        exam_form = ExamForm(request.POST or None)
        if exam_form.is_valid():
            exam_form.save()
            return redirect('add_question')
        else:
            exam_form = ExamForm()
    return render(request, 'core/add_exam.html', {'exam_form':exam_form})


def add_question(request):
    question_form = QuestionForm()
    if request.method == 'POST':
        question_form = QuestionForm(request.POST or None)
        if question_form.is_valid():
            question_form.save()
            return redirect('add_question')
        else:
            question_form = QuestionForm()
    return render(request, 'core/add_question.html',{'question_form':question_form})


def view_exams(request):
    exams = Exam.objects.all()
    return render(request, 'core/view_exams.html',{'exams':exams})


def view_questions(request):
    filter = QuestionFilter(request.GET, queryset=Question.objects.all())
    return render(request, 'core/view_questions.html',{'questions':filter})


def view_chapters(request):
    chapters = Chapter.objects.all()
    return render(request, 'core/view_chapters.html',{'chapters':chapters})


def edit_exam(request, pk):
    exam = Exam.objects.get(pk=pk)
    exam_form = ExamForm(request.POST or None, instance=exam)
    if exam_form.is_valid():
        exam_form.save()
        return redirect('view_exams')
    return render(request, 'core/edit_exam.html', {'exam_form':exam_form})


def edit_question(request, pk):
    question = Question.objects.get(pk=pk)
    question_form = QuestionForm(request.POST or None, instance=question)
    if question_form.is_valid():
        question_form.save()
        return redirect('view_questions')
    return render(request, 'core/edit_question.html', {'question_form':question_form})


def edit_question(request, pk):
    question = Question.objects.get(pk=pk)
    question_form = QuestionForm(request.POST or None, instance=question)
    if question_form.is_valid():
        question_form.save()
        return redirect('view_questions')
    return render(request, 'core/edit_question.html', {'question_form':question_form})


def edit_chapter(request, pk):
    chapter = Chapter.objects.get(pk=pk)
    chapter_form = ChapterForm(request.POST or None, files=request.FILES, instance=chapter)
    if chapter_form.is_valid():
        chapter_form.save()
        return redirect('view_chapters')
    chapter_form = ChapterForm(request.POST or None, files=request.FILES, instance=chapter)
    return render(request, 'core/edit_chapter.html', {'chapter_form':chapter_form})


def students_results(request):
    filter = ResultFilter(request.GET, Result.objects.all().exclude(student__is_superuser=False))
    return render(request, 'core/students_results.html',{'results':filter})

































































def take_test(request, chapter_id):
    test = Test.objects.filter(chapter=chapter_id)
    questions = QuestionOne.objects.all().filter(test=test)

    
    return render(request, 'take_test.html', {'questions':questions})
