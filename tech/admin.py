from django.contrib import admin

# Register your models here.

from tech.models import *
from django import forms
admin.site.register([Question,Answer,Comment])

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['answer_id']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['answer_id'].queryset = Answer.objects.filter(
                                        question_id=self.instance.question_id)