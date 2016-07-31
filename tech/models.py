from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class User_points(models.Model):
    user_id=models.ForeignKey(User)
    credits=models.IntegerField()
    photo=models.ImageField(height_field='height',width_field='width',default='/static/sample.png')
    height=models.IntegerField(default=20)
    width=models.IntegerField(default=20)

class Question(models.Model):
    # question_id=models.IntegerField(auto_created=True)
    user = models.ForeignKey(User)
    pic=models.ForeignKey(User_points)
    questions=models.TextField()

    def __unicode__(self):
        return self.questions

class Answer(models.Model):
    user = models.ForeignKey(User)
    pic=models.ForeignKey(User_points)
    question_id=models.ForeignKey(Question)
    answers=models.TextField()
    def __unicode__(self):
        return self.answers

class Comment(models.Model):
    user = models.ForeignKey(User)
    pic=models.ForeignKey(User_points)
    answer_id=models.ForeignKey(Answer)
    comments=models.TextField()