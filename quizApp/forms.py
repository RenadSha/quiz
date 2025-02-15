from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import inlineformset_factory, formset_factory
from .models import Quiz, Question, Answer





class CreateNewUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Gebruikersnaam'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
        }

    def __init__(self, *args, **kwargs):
        super(CreateNewUser, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Wachtwoord'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Bevestig wachtwoord'})














# Quiz Form
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name', 'duration']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quiz naam'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duur in minuten'}),
        }

# Question Form
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Voer een vraag in'}),
        }

# Answer Form
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Antwoord'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# Formsets for multiple questions and answers
QuestionFormSet = formset_factory(QuestionForm, extra=1)  # Allows adding multiple questions
AnswerFormSet = formset_factory(AnswerForm, extra=3)  # Allows adding multiple answers per question
