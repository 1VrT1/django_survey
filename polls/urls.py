from django.urls import path
from .views import SurveyView, TakeSurvey

urlpatterns = [
    path('', SurveyView.as_view(), name='survey_list'),
    path('take-survey/<int:survey_id>/', TakeSurvey.as_view(), name='take_survey')
]
