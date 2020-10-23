from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import View
from .forms import QuestionAnswerForm
from django.forms.formsets import formset_factory

from polls.models import Question, Survey, Respondent


class SurveyView(ListView):
    """Передает в шаблон названия опросов, при нажатии на которые отобразятся вопросы и ответы."""
    model = Survey


class TakeSurvey(View):
    """Показывает форму вопросы - ответы. Делает запись данных в бд."""

    def was_interviewed(self, request, survey_id):  # survey_id получаем из метода get_absolute_url у модели Survey
        return len(Respondent.objects.filter(ip=self.get_client_ip(request), survey=survey_id)) > 0

    def get_client_ip(self, request):
        """Получение ip пользователя"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get(self, request, survey_id):
        message = ''  # Для отображения сообщения для пользователя об успешном добавлении либо наоборот.
        if not self.was_interviewed(request, survey_id):
            questions = Question.objects.filter(survey=survey_id)  # Получаем вопросы для конкретного опроса.
            # в extra передает количество вопросов для формирования необходимого количества форм.
            QuestionAnswerFormSet = formset_factory(QuestionAnswerForm, extra=questions.count())
            return render(request, 'polls/take_survey.html', {'formset': QuestionAnswerFormSet(), 'questions': questions})
        else:
            message = 'Что-то пошло не так... Возможно вы уже принимали участие в этом опросе.'
            return render(request, 'polls/take_survey.html', {'message': message})

    def post(self, request, survey_id):
        message = ''
        questions = Question.objects.filter(survey=survey_id)
        # Вторая проверка сравнивает количество пришедших ответов на вопросы с количеством вопросов.
        # Прибавляем пятерку, потому что request.POST помимо ответов на вопросы содержит и другие данные, например
        # csrf_token и другие, которых 5, а делее уже идут ответы на вопросы. Т.о. если пользователь ответит не на все
        # вопросы, то ему отобразится сообщение об ошибке, а вопросы на которые он ответил, не запишутся в бд.
        if not self.was_interviewed(request, survey_id) and len(request.POST) == (len(questions) + 5):
            cnt = 0
            QuestionAnswerFormSet = formset_factory(QuestionAnswerForm, extra=questions.count())
            formset = QuestionAnswerFormSet(request.POST)
            if formset.is_valid():
                for form in formset:
                    form = form.save(commit=False)
                    form.question = questions[cnt].title  # Перед сохранением добавляем вопросы, на которые были ответы.
                    cnt += 1
                    form.save()
                # После успешного сохранения вопросов и ответов, записываем в бд респондента и опрос, который он прошел.
                Respondent.objects.create(ip=self.get_client_ip(request), survey_id=survey_id)
                message = 'Спасибо за принятие участия в опросе!'
                return render(request, 'polls/take_survey.html', {'message': message})

        else:
            message = 'Что-то пошло не так... Возможно вы заполнили не все поля.'
            return render(request, 'polls/take_survey.html', {'message': message})
