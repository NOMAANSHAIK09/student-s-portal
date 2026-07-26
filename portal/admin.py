from django.contrib import admin

# Register your models here.

from .models import QuestionPaper, UserInfo 

admin.site.register(QuestionPaper)
admin.site.register(UserInfo)