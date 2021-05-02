from it_essentials.models import Chapter, Exam, Question
from .models import *
from .forms import *
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from .filters import QuestionFilter, ResultFilter
from django.utils import timezone
import datetime





def homepage(request):
    if request.user.is_superuser:
        return redirect('account')
    chapters = Chapter.objects.all()
    return render(request, 'core/homepage.html',{'chapters':chapters})


def chapter(request, id):
    chapter = get_object_or_404(Chapter, id=id)
    exam = Exam.objects.all().filter(chapter=chapter)
    chapters = Chapter.objects.exclude(id=chapter.id)
    return render(request, 'core/chapter.html', {'chapter':chapter, 'chapters':chapters, 'exam':exam})


@login_required(login_url='login')
def take_test(request, id):
    exam = Exam.objects.get(chapter=id)
    exams = Exam.objects.exclude(id=exam.id)
    number_of_questions = Question.objects.all().filter(exam=exam).count()
    questions = Question.objects.filter(exam=exam)
    total_marks = 0

    for question in questions:
        total_marks = total_marks + question.score

    return render(request, 'core/exam.html',{'exam':exam, 'number_of_questions':number_of_questions, 'total_marks':total_marks ,'questions':questions, 'exams':exams})


@login_required(login_url='login')
def start_test(request, id):
    if request.user.is_authenticated:
        exam = Exam.objects.get(id=id)

        result = Result.objects.filter(exam=exam.id).filter(student=request.user.id).exists()
        if result:
            return redirect('done_test')
        questions = Question.objects.filter(exam=exam)
        if request.method=='POST':
            pass
        response = render(request, 'core/start_exam.html',{'exam':exam, 'questions':questions})
        response.set_cookie('exam_id',exam.id)
        return response
    return redirect('login')


@login_required(login_url='login')
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

        return redirect('after_exam', exam_id)


@login_required(login_url='login')
def after_exam(request, id):
    student = request.user.id
    exam = Exam.objects.get(id=id)
    exams=Exam.objects.all()
    result=Result.objects.filter(student=student).order_by('-id')[:1]
    return render(request, 'core/after_exam.html',{'result':result,'exams':exams, 'exam':exam})


@login_required(login_url='login')
def results(request, id):
    exam = Exam.objects.get(id=id)
    exams  = Exam.objects.exclude(id=exam.id)
    student = request.user.id
    questions = Question.objects.all().filter(exam=exam)
    result = Result.objects.all().filter(exam=exam).filter(student=student)
    return render(request,'core/result.html',{'result':result,'exams':exams,'exam':exam,'questions':questions})


@login_required(login_url='login')
def view_result(request):
    results = Result.objects.filter(student=request.user)
    return render(request,'core/view-results.html',{'results':results})


@login_required(login_url='login')
def done_test(request):
    return render(request, 'core/done-test.html')


@login_required(login_url='login')
def profile(request):
    return render(request ,'core/profile.html')


def news(request):
    news=News.objects.all()
    chapters = Chapter.objects.all()
    return render(request, 'core/news.html',{'news':news,'chapters':chapters})


def news_details(request, id):
    news=News.objects.get(id=id)
    chapters = Chapter.objects.all()
    return render(request, 'core/news_details.html',{'news':news,'chapters':chapters})


def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST or None,files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    form = SignupForm()

    return render(request, 'core/signup.html',{'form':form})


@staff_member_required
def account(request):
    students_list = StudentProfile.objects.all().exclude(is_superuser=True)
    students = StudentProfile.objects.all().exclude(is_superuser=True).count()
    chapters = Chapter.objects.all().count()
    tests = Exam.objects.all().count()
    questions = Question.objects.all().count()

    now = datetime.datetime.now()
    curr = str(now.year) + "-" + str(now.month) + "-01"
    curr_year = int(now.year)
    curr_month = int(now.month)
    dataArray = []
    for i in range(0, 6):
        if(curr_month-i <= 0):
            curr_year -= 1
            curr_month += 12
        curr_array = dict()
        curr_array["year"] = curr_year
        curr_array["month"] = curr_month - i -1
        if(curr_month - i != 12):
            curr_array["count"] = StudentProfile.objects.exclude(is_superuser=True).filter(date_joined__range = (datetime.date(curr_year, curr_month-i, 1), datetime.date(curr_year, curr_month-i + 1, 1))).count()
        else:
            curr_array["count"] = StudentProfile.objects.exclude(is_superuser=True).filter(date_joined__range = (datetime.date(curr_year, 12, 1), datetime.date(curr_year+1, 1, 1))).count()
        dataArray.append(curr_array)

    return render(request, 'admin/account.html', {'students_list':students_list,'students':students,'chapters':chapters, 'tests':tests,'questions':questions,'dataArray':dataArray})


@staff_member_required
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
    return render(request, 'admin/add_chapter.html')


@staff_member_required
def add_exam(request):
    exam_form = ExamForm()
    if request.method == 'POST':
        exam_form = ExamForm(request.POST or None)
        if exam_form.is_valid():
            exam_form.save()
            return redirect('add_question')
        else:
            exam_form = ExamForm()
    return render(request, 'admin/add_exam.html', {'exam_form':exam_form})


@staff_member_required
def add_question(request):
    question_form = QuestionForm()
    if request.method == 'POST':
        question_form = QuestionForm(request.POST or None)
        if question_form.is_valid():
            question_form.save()
            return redirect('view_questions')
        else:
            question_form = QuestionForm()
    return render(request, 'admin/add_question.html',{'question_form':question_form})


@staff_member_required
def view_exams(request):
    exams = Exam.objects.all()
    return render(request, 'admin/view_exams.html',{'exams':exams})


@staff_member_required
def view_questions(request):
    filter = QuestionFilter(request.GET, queryset=Question.objects.all())
    return render(request, 'admin/view_questions.html',{'questions':filter})


@staff_member_required
def view_chapters(request):
    chapters = Chapter.objects.all()
    return render(request, 'admin/view_chapters.html',{'chapters':chapters})


@staff_member_required
def edit_exam(request, pk):
    exam = Exam.objects.get(pk=pk)
    exam_form = ExamForm(request.POST or None, instance=exam)
    if exam_form.is_valid():
        exam_form.save()
        return redirect('view_exams')
    return render(request, 'admin/edit_exam.html', {'exam_form':exam_form})


@staff_member_required
def edit_question(request, pk):
    question = Question.objects.get(pk=pk)
    question_form = QuestionForm(request.POST or None, instance=question)
    if question_form.is_valid():
        question_form.save()
        return redirect('view_questions')
    return render(request, 'admin/edit_question.html', {'question_form':question_form})


@staff_member_required
def edit_chapter(request, pk):
    chapter = Chapter.objects.get(pk=pk)
    chapter_form = ChapterForm(request.POST or None, files=request.FILES, instance=chapter)
    if chapter_form.is_valid():
        chapter_form.save()
        return redirect('view_chapters')
    chapter_form = ChapterForm(request.POST or None, files=request.FILES, instance=chapter)
    return render(request, 'admin/edit_chapter.html', {'chapter_form':chapter_form})



@staff_member_required
def students_results(request):
    results = Result.objects.all().exclude(student__is_superuser=False)
    return render(request, 'admin/students_results.html',{'results':results})


@staff_member_required
def registered_students(request):
    students = StudentProfile.objects.exclude(is_superuser=True)
    return render(request, 'admin/registered_students.html', {'students':students})
