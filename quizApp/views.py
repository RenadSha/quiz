from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import  logout, authenticate, login
import requests
from quizProject import settings
from .forms import CreateNewUser
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
# Create your views here.


# @allowedUsers(allowedGroups='customer')

def home(request):
    invites = Invite.objects.filter(receiver=request.user, is_accepted=False)
    return render(request, "home.html", {'invites': invites})
@login_required
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, owner=request.user)

    # Start de quiz
    quiz.start_quiz()
    
    return redirect('quiz_page', quiz_id=quiz.id)
@login_required
def quiz_page(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'quiz.html', {'quiz': quiz})

@login_required
def accept_invite(request, invite_id):
    invite = get_object_or_404(Invite, id=invite_id, receiver=request.user, is_accepted=False)

    # Koppel de gebruiker aan de quiz
    invite.quiz.participate_in_quiz(request.user)

    # Markeer de uitnodiging als geaccepteerd
    invite.is_accepted = True
    invite.save()

    # Redirect naar de quizpagina (vervang 'quiz_page' met je echte view naam)
    return redirect('quiz_page', quiz_id=invite.quiz.id)


@login_required
def submit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    user = request.user
    quiz_user, created = QuizUser.objects.get_or_create(quiz=quiz, user=user)

    # Controleer of de tijd verstreken is
    if quiz.started_at and (now() - quiz.started_at).total_seconds() > (quiz.duration * 60):
        return redirect('quiz_result', quiz_id=quiz.id)  # Tijd is om, stuur naar resultaat

    score = 0

    if request.method == "POST":
        for question in quiz.questions.all():
            selected_answer_id = request.POST.get(f'question_{question.id}')
            if selected_answer_id:
                answer = Answer.objects.get(id=selected_answer_id)
                if answer.is_correct:
                    score += 1

    quiz_user.score = score
    quiz_user.save()

    return redirect('quiz_result', quiz_id=quiz.id)

@login_required
def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz_user = QuizUser.objects.get(quiz=quiz, user=request.user)

    # Sorteer de spelers op score (hoog naar laag)
    leaderboard = QuizUser.objects.filter(quiz=quiz).order_by('-score')

    return render(request, 'quiz_result.html', {
        'quiz': quiz,
        'score': quiz_user.score,
        'total_questions': quiz.questions.count(),
        'leaderboard': leaderboard
    })


def userLogin(request):

    if request.method == 'POST':
        username =request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Credentials error')
    context = {}
    return render(request, 'login.html', context)


def register(request):
    form = CreateNewUser()
    if request.method == 'POST':
        form = CreateNewUser(request.POST)
        if form.is_valid():

            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }

            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data)
            result = r.json()
            if result['success']:
                user = form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, username + ' Created successfully !')
                return redirect('login')
            else:
                messages.error(request, 'Invalid Recaptcha please try again.' )

            
            
            
    context = {'form': form}
    return render(request, 'register.html', context)


def userLogout(request):
    logout(request)
    return redirect('login')