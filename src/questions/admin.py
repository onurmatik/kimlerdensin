from django.contrib import admin
from questions.models import Verb, Answer, Question

admin.site.register(Verb)
admin.site.register(Answer)
admin.site.register(Question)