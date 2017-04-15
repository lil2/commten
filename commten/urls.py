from django.conf.urls import url,include
from . import views
from rest_framework import routers
from django.contrib.auth.views import logout
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^noticeboard/$', views.noticeboard_page, name='NoticeBoard'),
    url(r'^privacy/$', views.privacy, name='privacy'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', lambda request: logout(request, "/"), name='logout'),
    url(r'^signup/$', views.signup_view, name='signup'),
    url(r'^Tickets/$', login_required(views.PostView.as_view()), name='posts'),
    url(r'^post/(?P<pk>[0-9]+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/(?P<pk>[0-9]+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>[0-9]+)/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.post_edit_view, name='post_edit'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'new-post/$', views.new_post_view, name='new_post'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.post_delete_view, name='delete'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^accounts/update/(?P<pk>[\-\w]+)/$', views.edit_user, name='account_update'),
]