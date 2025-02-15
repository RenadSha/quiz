from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_quizzes')
    users = models.ManyToManyField(User, through='QuizUser', related_name='quizzes')
    duration = models.IntegerField(help_text="Duur van de quiz in minuten")
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def participate_in_quiz(self, user):
        """Voegt een gebruiker toe aan de quiz als deelnemer."""
        if not QuizUser.objects.filter(quiz=self, user=user).exists():
            QuizUser.objects.create(quiz=self, user=user)

    def start_quiz(self):
        """Start de quiz door de starttijd te zetten en deze actief te maken."""
        from django.utils.timezone import now
        self.started_at = now()
        self.is_active = True
        self.save()

class QuizUser(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    joined_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.name

class Answer(models.Model):
    text = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'Correct' if self.is_correct else 'Wrong'})"

class Invite(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invites')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invites')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} invited {self.receiver} to {self.quiz}"
