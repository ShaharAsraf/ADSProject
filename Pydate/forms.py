import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from Pydate.models import PersonalQuestionAnswer, PersonalQuestionContent
from Pydate.models import User


class RegisterForm(UserCreationForm):
    initial_date = datetime.date.today() - datetime.timedelta(days=365 * 18)
    birth_date = forms.DateField(initial=initial_date)
    username = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=200)
    sex = forms.ChoiceField(choices=(("F", "F"), ("M", "M")))
    searching_for = forms.ChoiceField(choices=(("F", "F"), ("M", "M"), ("Both", "Both")))
    whatsapp = forms.CharField(max_length=12)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'birth_date', 'sex', 'searching_for','whatsapp')

    def clean_birth_date(self):
        data = self.cleaned_data['birth_date']
        if data > datetime.date.today() - datetime.timedelta(days=365 * 18):
            raise ValidationError(_('You have to be an adult to create a profile!'))
        return data


class PersonalQuestionsForm(ModelForm):
    content = forms.CharField(required=True,
                              widget=forms.TextInput(attrs={"class": "answer", "required": "true"}),
                              max_length=200)

    class Meta:
        model = PersonalQuestionAnswer
        fields = ("content",)

    def clean_content(self):
        answer = self.cleaned_data['content']
        if not answer or answer == "":
            raise ValidationError("Please, answer all of the questions")
        return answer


class PersonalQuestionsCreateForm(ModelForm):
    content = forms.CharField(required=True,
                              widget=forms.TextInput(attrs={"class": "answer", "required": "true"}),
                              max_length=250)

    class Meta:
        model = PersonalQuestionContent
        fields = ("content",)

    def clean_content(self):
        q = self.cleaned_data['content']
        if not q or q == "":
            raise ValidationError("Please, complete all of the questions")
        return q


class RemainForm(forms.Form):
    message = forms.CharField(required=True, label='Your name', max_length=250)
