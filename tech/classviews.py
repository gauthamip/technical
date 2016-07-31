from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from tech.models import *
from django.db.models import F
from rest_framework import viewsets
from tech.serializers import *

@method_decorator(login_required,name='dispatch')
class LListView(ListView):
    model = Question

class UserListView(ListView):
    model = User_points
    template_name = 'leader.html'

    def get_queryset(self):
        return User_points.objects.distinct('user_id__username','credits').order_by(credits)


@method_decorator(login_required,name='dispatch')
class LDetailView(DetailView):
    model=Question

    def get_object(self, queryset=None):
        id1 = self.kwargs.get('pk')
        queryset = Question.objects.all().get(id=id1)
        return queryset

@method_decorator(login_required,name='dispatch')
class LCreateView(CreateView):
    model = Question
    fields =['questions']

    def get_success_url(self):
        return reverse('create')

    def form_valid(self, form):

        form.instance.user = self.request.user

        try:
            c = User_points.objects.all().get(user_id=self.request.user)
            form.instance.pic = User_points.objects.get(user_id_id=self.request.user.id)
            points = c.credits
        except User_points.DoesNotExist:
            c = User_points(user_id=self.request.user, credits=2).save()
            form.instance.pic = User_points.objects.get(user_id_id=self.request.user.id)
            points = 2
        User_points.objects.filter(user_id=self.request.user).update(credits=F('credits') + 4)
        # User_points.save()
        return super(LCreateView, self).form_valid(form)

@method_decorator(login_required,name='dispatch')
class ICreateView(CreateView):
    model = Answer
    fields=['answers']
    def get_success_url(self):
        return reverse('item')

    def form_valid(self, form):
        form.instance.user = self.request.user
        id1 = self.kwargs.get('pk')
        form.instance.question_id=Question.objects.get(id=id1)

        try:
            c = User_points.objects.all().get(user_id=self.request.user)
            form.instance.pic = User_points.objects.get(user_id_id=self.request.user.id)
            points = c.credits
        except c.DoesNotExist:
            c = User_points(user_id=self.request.user, credits=2).save()
            form.instance.pic = User_points.objects.get(user_id_id=self.request.user.id)
            points = 2
        User_points.objects.filter(user_id=self.request.user).update(credits=F('credits') + 3)
        # User_points.save()
        return super(ICreateView, self).form_valid(form)

@method_decorator(login_required,name='dispatch')
class CCreateView(CreateView):
    model = Comment
    fields=['comments']
    def get_success_url(self):
        return reverse('create_comment')

    def form_valid(self, form):
        form.instance.user = self.request.user
        id1 = self.kwargs.get('pk')
        form.instance.question_id=0

        form.instance.answer_id=Answer.objects.all().get(id=id1)
        try:
            c = User_points.objects.all().get(user_id=self.request.user)
            form.instance.pic = User_points.objects.get(user_id_id=self.request.user.id)
            points = c.credits
        except c.DoesNotExist:
            c=User_points(user_id=self.request.user, credits=2).save()
            form.instance.pic = User_points.objects.get(user_id_id=self.request.user.id)
            points = 2
        User_points.objects.filter(user_id=self.request.user).update(credits=F('credits') + 2)
        # User_points.save()

        return super(CCreateView,self).form_valid(form)



@method_decorator(login_required,name='dispatch')
class LUpdateView(UpdateView):
    model = Question
    fields = ['questions']
    def get_success_url(self):
        pk=self.kwargs.get('pk')
        return reverse('update')


@method_decorator(login_required,name='dispatch')
class UserUpdateView(UpdateView):
    model = User_points
    fields = ['photo']

    def get_success_url(self):
        pk=self.kwargs.get('pk')
        return reverse('photo')

@method_decorator(login_required,name='dispatch')
class LDeleteView(DeleteView):
    model=Question
    success_url =reverse_lazy('delete')


class TodolistViewset(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('id')
    serializer_class = TodolistSerializer

class TodoitemViewset(viewsets.ModelViewSet):
    queryset = Answer.objects.all().order_by('item_list')
    serializer_class = TodoitemSerializer
