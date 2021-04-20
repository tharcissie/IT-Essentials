import django_filters
from .models import Question, Result


class QuestionFilter(django_filters.FilterSet):
    class Meta:
        model = Question
        fields = ['exam']

class ResultFilter(django_filters.FilterSet):
    class Meta:
        model = Result
        fields = ['student','exam']