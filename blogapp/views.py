from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect,reverse, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .serializers import PostSerializer
from .models import Post, User
from django.utils import timezone
from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import PostForm

'''REST Views'''


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('id')
    serializer_class = PostSerializer


'''App Views'''

# Create your views here.


def home_page(request):
    return render(request, 'blogapp/home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        return render(request, 'blogapp/login_info.html')
    return redirect(home_page)


def signup_view(request):
    if request.method == 'POST':
        if request.is_ajax():
            usr = request.POST['name']
            pwd = request.POST['pwd']
            new_user = User.objects.create_user(username=usr, email=None, password=pwd)
            login(request, new_user)
            return HttpResponse('')


def follow_view(request):
    users = User.objects.all().exclude(id=request.user.id)
    followees = request.user.follows.all()
    return render(request, 'blogapp/users_list.html', {'users': users, 'followees': followees})


def follow_to_view(request):
    if request.method == 'POST':
        current_user = User.objects.get(username=request.user)
        follow_id = request.POST.get('follow_id')
        status = str(request.POST.get('follow_text')).strip()

        user_to_follow = User.objects.get(id=follow_id)
        if status == 'Followed':
            current_user.follows.remove(user_to_follow)
            status = 'Follow'
        elif status == 'Follow':
            current_user.follows.add(user_to_follow)
            status = 'Followed'
        return JsonResponse({'status': status})
    return HttpResponse('')


class PostView(generic.ListView):
    template_name = 'blogapp/post.html'
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Post.objects.all()
        else:
            return Post.objects.filter(author__in=User.objects.get(username=self.request.user).follows.all())


class DetailView(generic.DetailView):
    model = Post
    template_name = 'blogapp/detail.html'
    context_object_name = 'post_detail'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['next'] = Post.objects.filter(id__gt=self.kwargs['pk']).first()
        context['previous'] = Post.objects.filter(id__lt=self.kwargs['pk']).last()
        return context


def post_edit_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post_form = PostForm(request.POST or None, request.FILES or None, instance=post)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.create_date = timezone.now()
            post.save()
            messages.success(request, "Successfully Saved !", extra_tags='alert alert-success')
            return redirect('detail', pk=post.pk)
    else:
        post_form = PostForm(instance=post)
    return render(request, 'blogapp/post_edit.html', {'post_form': post_form})


def new_post_view(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST or None, request.FILES or None)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.create_date = timezone.now()
            post.save()
            messages.success(request, "Successfully Created !",extra_tags='alert alert-success')
            return redirect('detail', pk=post.pk)
        else:
            messages.error(request, "Not Successfully Created !")
    else:
        post_form = PostForm()
    return render(request, 'blogapp/post_edit.html', {'post_form': post_form})


def post_delete_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    messages.success(request, "Successfully delete !", extra_tags='alert alert-warning')
    return redirect('posts')


def music_view(request):
    return render(request, 'blogapp/music.html')



