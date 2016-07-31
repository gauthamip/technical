from django.conf.urls import url
from django.contrib import admin
from tech import views
from tech.classviews import LListView,LCreateView,LDetailView,ICreateView,LUpdateView,LDeleteView,CCreateView,UserUpdateView
from django.contrib.auth.views import password_reset
urlpatterns = [
    url(r'^question/',views.questions,name='create'),
    url(r'^question/',views.questions,name='update'),
    url(r'^question/',views.questions,name='delete'),
    url(r'^question/',views.questions,name='create_comment'),
    url(r'^questions/(?P<pk>[0-9]*)/',LDetailView.as_view(template_name='questions_detail.html')),
    url(r'^create/questions/',LCreateView.as_view(template_name='questions_create.html')),
    url(r'^create/comments/(?P<pk>[0-9]*)/',CCreateView.as_view(template_name='comments_create.html'),name='create_comment_1'),
    url(r'^delete/(?P<pk>[0-9]*)/$',LDeleteView.as_view(template_name='questions_confirm_delete.html')),
    url(r'update/questions/(?P<pk>[0-9]*)/',LUpdateView.as_view(template_name='questions_create.html')),
    url(r'^create/answers/(?P<pk>[0-9]*)/',ICreateView.as_view(template_name='answers_create.html'),name='create_answer_1'),
    url(r'^question/',views.questions,name='item'),
    url(r'^answers/(?P<questions>[0-9]*)/',views.answers),
    url(r'^comments/(?P<answers>[0-9]*)/',views.comments),
    url(r'list/$',views.list),
    url(r'list_details/(?P<pk>[0-9]*)/$',views.list_detail),
    url(r'homepage/',views.homepage),
    url(r'register/',views.adduser),
    url(r'profile/',views.profile,name='photo'),
    url(r'update/photo/(?P<pk>[0-9]*)/',UserUpdateView.as_view(template_name='profile_photo.html')),
    url(r'profile1/(?P<user_id_id>[0-9]*)/',views.profile1),
    url(r'edit/details/(?P<pk>[0-9]*)/',views.update_user),
    url(r'leaderboard/',views.leader)
]