from django.db import models


class UserInfo(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    roll_no = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    semester = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class QuestionPaper(models.Model):
    subject = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    semester = models.IntegerField()
    exam_year = models.IntegerField()
    pdf = models.FileField(upload_to='question_papers/')

    def __str__(self):
        return self.subject