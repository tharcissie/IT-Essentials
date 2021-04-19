from django.shortcuts import render, get_object_or_404, redirect
from core.models import Chapter, Exam, Question


def homepage(request):
    chapters = Chapter.objects.all()
    return render(request, 'core/homepage.html',{'chapters':chapters})

def chapter_content(request, name):
    chapter = get_object_or_404(Chapter, name=name)
    return render(request, 'core/chapter_content.html',{'chapter':chapter})

def chapter_exam(request, id):
    exam = Exam.objects.get(chapter=id)
    number_of_questions = Question.objects.all().filter(exam=exam).count()
    questions = Question.objects.filter(exam=exam)
    total_marks = 0

    for question in questions:
        total_marks = total_marks + question.score
    
    if request.method=='POST':
        pass
    response = render(request, 'core/start_exam.html',{'exam':exam, 'questions':questions, 'number_of_questions':number_of_questions, 'total_marks':total_marks})
    response.set_cookie('exam_id',exam.id)
    return response