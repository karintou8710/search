from django.db import models
from django.utils import timezone


class GradeInfo(models.Model):
    """成績データ
    """

    subject = models.CharField(max_length=100)
    lecture = models.CharField(max_length=100)
    group = models.CharField(max_length=100)
    teacher = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    semester = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)
    numOfStudents = models.IntegerField()
    gpa = models.FloatField()

    # 成績 ap -> A+ am -> A-
    ap = models.IntegerField()
    a = models.IntegerField()
    am = models.IntegerField()
    bp = models.IntegerField()
    b = models.IntegerField()
    bm = models.IntegerField()
    cp = models.IntegerField()
    c = models.IntegerField()
    d = models.IntegerField()
    dm = models.IntegerField()
    f = models.IntegerField()

    created_at = models.DateTimeField(default=timezone.now, editable=False)
