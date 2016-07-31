from django.contrib.auth.views import password_reset
from django.forms import ModelForm
from django.shortcuts import render
from tech.models import *
from django.template import loader
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from tech.serializers import *
from django import forms

# Create your views here.
class JSONResponse(HttpResponse):
    def __init__(self,data,**kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type']='application/json'
        super(JSONResponse,self).__init__(content,**kwargs)

def User_update(request):
    user=User.objects.all(user=request.user)
    pro=User_points.objects.all().get(user_id_id=request.user.id)


def leader(request):
    leader1=User_points.objects.all().order_by("-credits")
    template = loader.get_template("leader.html")
    result = template.render(context={"list": leader1})
    return HttpResponse(result)

def questions(request):
    list = Question.objects.all()
    template = loader.get_template("questions_list.html")
    result = template.render(context={"list": list})
    return HttpResponse(result)

def answers(request,questions):
    items=Answer.objects.all().filter(question_id=questions)
    users=request.user

    # items = Answer.objects.all().filter(question_id=question)
    template = loader.get_template("answers.html")
    if items.exists():
        q = Question.objects.get(id=items[0].question_id_id)
        result = template.render(context={"item": items,"users":users,"question":q})
    else:
        q=Question.objects.get(id=questions)
        result = template.render(context={"item": items, "users": users,"question":q})

    return HttpResponse(result)

def comments(request,answers):
    items=Comment.objects.all().filter(answer_id=answers)
    users = request.user
    # items = Answer.objects.all().filter(question_id=question)
    template = loader.get_template("comments.html")
    if items.exists():
        a=Answer.objects.get(id=items[0].answer_id_id)
        result = template.render(context={"comment": items,"users":users,"answer":a})
    else:
        a=Answer.objects.get(id=answers)
        result = template.render(context={"comment": items, "users": users, "answer": a})
    return HttpResponse(result)

@csrf_exempt
def list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Question.objects.all()
        serializer = TodolistSerializer(snippets, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TodolistSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

def profile1(request,user_id_id):
    list2 = User_points.objects.all().get(user_id_id=user_id_id)
    list1 = User.objects.get(id=list2.user_id_id)
    template = loader.get_template("profile.html")
    result = template.render(context={"profile": list1,"points":list2})
    return HttpResponse(result)

@csrf_exempt
def list_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TodolistSerializer(snippet)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TodolistSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)

class PhotoForm(ModelForm):
    class Meta:
        model=User_points
        fields=('photo',)

def photo_update(request,pk):
    instance=User_points.objects.get(pk=pk)
    form=PhotoForm(request.POST or None,request.FILES or None,instance=instance)
    if form.is_valid():
        instance=form.save()
        instance.save()
        return HttpResponseRedirect('/tech/profile')
    context={
        "photo":instance.photo,
        "instance":instance,
        "form":form,
    }
    return render(request,"profile_photo.html",context)


def my_password_reset(request, template_name='password_reset_form.html'):
    return password_reset(request, template_name)

class UserForm(ModelForm):
    class Meta:
        username = forms.CharField(max_length=30)
        email=forms.CharField(max_length=30)
        password=forms.CharField(max_length=30,widget=forms.PasswordInput)
        model = User
        fields=('username','email','password')
        widgets={
            'password': forms.PasswordInput(),
        }
        # fields = ('username', 'email', 'password')

def adduser(request):
    template = loader.get_template("comments.html")
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            return HttpResponseRedirect('/tech/homepage')
    else:
        form = UserForm()
    return render(request, 'user_register.html', {'form': form})

def update_user(request,pk):
    instance = User.objects.get(pk=pk)
    form = UserForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save()
        instance.save()
        return HttpResponseRedirect('/tech/profile')
    context = {
        "username": instance.username,
        "instance": instance,
        "form": form,
    }
    return render(request, "user_register.html", context)

def homepage(request):
    template = loader.get_template("homepage.html")
    return HttpResponse(template.render())

def profile(request):
    list3=None
    try:
       list2 = User_points.objects.all().get(user_id=request.user)
       list3=Question.objects.all().filter(user_id=request.user)
    except User_points.DoesNotExist:
        User_points(user_id=request.user, credits=2).save()
        list2 = User_points.objects.all().get(user_id=request.user)
    except Question.DoesNotExist:
        list3=None
        pass
    list1 = request.user
    template = loader.get_template("profile.html")
    result = template.render(context={"profile": list1,"points":list2,"questions":list3})
    return HttpResponse(result)

def points(request):
    list1 = User_points.objects.all().get(user_id=User.objects.get(is_active=1))
    template = loader.get_template("profile.html")
    result = template.render(context={"points": list1})
    return HttpResponse(result)

