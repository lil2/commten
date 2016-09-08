from django.conf.urls import url,include
from . import views
from rest_framework import routers
from django.contrib.auth.views import logout
from django.contrib.auth.decorators import login_required

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)

urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', lambda request: logout(request, "/"), name='logout'),
    url(r'^user/create/$', views.signup_view, name='signup'),
    url(r'^find-friends/$', views.follow_view, name='follow'),
    url(r'^follows/$', views.follow_to_view, name='follow_to'),
    url(r'^posts/$', login_required(views.PostView.as_view()), name='posts'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.post_edit_view, name='post_edit'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'new-post/$', views.new_post_view, name='new_post'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.post_delete_view, name='delete'),
    url(r'music/$', views.music_view, name='music'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]