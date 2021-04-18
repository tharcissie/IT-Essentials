from django.shortcuts import render
from core.models import Chapter


def homepage(request):
    chapters = Chapter.objects.all()
    return render(request, 'core/homepage.html',{'chapters':chapters})
