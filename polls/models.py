from django.db import models
from django.urls import reverse


class Answer(models.Model):
    """Через админку добавляем ответ на вопрос, который отобразится для каждого вопроса."""
    title = models.CharField("Ответ", max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


class Survey(models.Model):
    """Через админку добавляем опрос. Далее читать описание в модели Question"""
    title = models.CharField("Опрос", max_length=200)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('take_survey', kwargs={'survey_id': self.id})

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"


class Respondent(models.Model):
    """Модель для индентификации респондента."""
    ip = models.CharField("IP адрес", max_length=20)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name="Опрос")

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = "Респондент"
        verbose_name_plural = "Респонденты"


class Question(models.Model):
    """
    Модель для отображения вопросов в опросе. Через админку добавляем вопрос и выбираем опрос,
    в котором будет отображаться этот вопрос. Готово, теперь пользователи могут участвовать в опросе.
    """
    title = models.CharField("Вопрос", max_length=200)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class QuestionAnswer(models.Model):
    """Модель для записи ответов респондента на вопросы."""
    question = models.CharField("Вопрос", max_length=200)
    answer = models.ForeignKey(Answer, on_delete=models.DO_NOTHING, verbose_name="Ответ")

    def __str__(self):
        return f'{self.question} - {self.answer}'

    class Meta:
        verbose_name = "Вопросы и ответы"
        verbose_name_plural = "Вопросы и ответы"
