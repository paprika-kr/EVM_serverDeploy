from django.db import models
from accounts.models import *

class problem(models.Model):
    problem_id = models.CharField(primary_key=True, max_length=13)
    ID = models.ForeignKey(monitor, on_delete=models.CASCADE)
    answer = models.IntegerField()
    type = models.CharField(max_length=20)
    blank_num = models.IntegerField()
    info = models.CharField(max_length=30, null=True)
    image = models.ImageField(upload_to='problems/',null=True, blank=True)
    text = models.TextField(blank=True, null=True)
    blank_text = models.TextField(blank=True, null=True)
    translation_text = models.TextField(blank=True, null=True)
    problem_image = models.ImageField(upload_to='results/', null=True, blank=True)
    keyword_duplicate = models.BooleanField(default=True)

class class_cnt(models.Model):
    class_cnt_id = models.IntegerField(primary_key=True, default=1)
    problem_cnt = models.BigIntegerField(default=1)


