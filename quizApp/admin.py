from django.contrib import admin
from .models import Invite, Question, Quiz, QuizUser, Answer

# Register your models here.
admin.site.register(Invite)
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(QuizUser)
admin.site.register(Answer)
