from django.db import models
from .storage import SupabaseStorage

class UserInfo(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    roll_no = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    semester = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    
    # use for email verification and provide each user unique token
    # is_verified = models.BooleanField(default=False)
    # verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    

    def __str__(self):
        return self.name


class QuestionPaper(models.Model):
    subject = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    semester = models.IntegerField()
    exam_year = models.IntegerField()
    pdf = models.FileField(
        storage=SupabaseStorage(),
        upload_to='question_papers/'
    )

    def __str__(self):
        return self.subject