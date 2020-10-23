from django import forms

from .models import QuestionAnswer


class QuestionAnswerForm(forms.ModelForm):

    class Meta:
        model = QuestionAnswer
        fields = ('answer',)
        widgets = {
            'answer': forms.RadioSelect()
        }
