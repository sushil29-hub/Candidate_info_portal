from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class CandidateInfo(BaseModel):

    name = models.CharField(max_length=30)
    address = models.TextField()
    number = models.BigIntegerField(unique=True)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=50)
    tech_skills = models.JSONField()
    resume_url = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'candidate_info'


# Access Key: AKIAWQZZ2NM7RFCCBKOI
# Secret access key: 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