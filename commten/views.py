from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from rest_framework import viewsets
from .models import Tickets, User, Comment
from django.utils import timezone
from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import PostForm, UserSignupForm, CommentForm, UserProfileForm
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserForm
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

User = get_user_model()
'''App Views'''

# Create your views here.


# Home Page View
def home_page(request):
    return render(request, 'commten/home.html')


def noticeboard_page(request):
    return render(request, 'commten/NoticeBoard.html')

# User Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        return render(request, 'commten/login_info.html')
    return redirect("posts")


# User Signup View
def signup_view(request):
    if request.method == "POST":
        signup_form = UserSignupForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            print(request.POST['username'])
            new_user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, new_user)
            return redirect('posts')
        else:
            if User.objects.filter(username=request.POST['username']).exists():
                return HttpResponse("User already existed!")
            return HttpResponse("Enter at least 9 charactors or more with combination of numbers and letters!!!!")

    else:
        signup_form = UserSignupForm()
    return render(request, 'commten/signup.html', {'signup_form': signup_form})


# User List View
def follow_view(request):
    users = User.objects.all().exclude(id=request.user.id)
    users_are_followed = request.user.follows.all()
    return render(request, 'commten/users_list.html', {'users': users, 'users_are_followed': users_are_followed})


# Ajax Call to Add or Remove Users From followed List
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


# Generic ListView for Creating Post objects along with Paginator
class PostView(generic.ListView):
    template_name = 'commten/post.html'
    context_object_name = "posts"
    paginate_by = 5

    # Override default queryset to show posts based on followed users
    def get_queryset(self):
        if self.request.user.is_superuser:         # Superuser would be able to view all the post from all users
            return Tickets.objects.all().order_by('-create_date')
        else:
            current_user = User.objects.get(username=self.request.user)
            current_user_follow_objects = User.objects.get(username=self.request.user).follows.all()
            search_keyword = self.request.GET.get('q')
            if search_keyword:
                return Tickets.objects.filter(Q(title__icontains=str(search_keyword)) &
                                           (Q(author=current_user) | Q(author__in=current_user_follow_objects)) ).order_by('-create_date')
            return Tickets.objects.filter(Q(author__in=current_user_follow_objects) | Q(author=current_user)).order_by('-create_date')


# Generic DetailView for Post objects
class DetailView(generic.DetailView):
    model = Tickets
    template_name = 'commten/detail.html'
    context_object_name = 'post_detail'

    # Override default context and add 'next' and 'previous' context to show the detail of next and previous post object
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        user = User.objects.get_by_natural_key(self.request.user)
        context['address'] = UserProfile.objects.get(user=kwargs['object'].author).address
        # print(type(kwargs['object'].author))
        context['apt'] = UserProfile.objects.get(user=kwargs['object'].author).apt
        context['next'] = Tickets.objects.filter(id__gt=self.kwargs['pk']).first()
        context['previous'] = Tickets.objects.filter(id__lt=self.kwargs['pk']).last()
        return context


# Post Edit View
def post_edit_view(request, pk):
    post = get_object_or_404(Tickets, pk=pk)
    if request.method == 'POST':
        post_form = PostForm(request.POST or None, request.FILES or None, instance=post)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.create_date = timezone.now()
            post.save()
            messages.success(request, "Successfully Saved !", extra_tags='alert alert-success')
            return redirect('detail', pk=post.pk)
    else:
        post_form = PostForm(instance=post)
    return render(request, 'commten/post_edit.html', {'post_form': post_form})


# New Post View
def new_post_view(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST or None, request.FILES or None)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.create_date = timezone.now()
            post.save()
            messages.success(request, "Successfully Created !", extra_tags='alert alert-success')
            return redirect('detail', pk=post.pk)
        else:
            messages.error(request, "Not Successfully Created !")
    else:
        post_form = PostForm()
    return render(request, 'commten/post_edit.html', {'post_form': post_form})


# Post Delete View
def post_delete_view(request, pk):
    post = get_object_or_404(Tickets, pk=pk)
    post.delete()
    messages.success(request, "Successfully delete !", extra_tags='alert alert-warning')
    return redirect('posts')


# Music Post View
def music_view(request):
    return render(request, 'commten/music.html')




def add_comment_to_post(request, pk):
    post = get_object_or_404(Tickets, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'commten/add_comment_to_post.html', {'form': form})


def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('detail', pk=comment.post.pk)


def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('detail', pk=post_pk)


def apt(args):
    pass


@login_required
def edit_user(request, pk):
    user = User.objects.get(pk=pk)
    user_form = UserProfileForm(instance=user)

    ProfileInlineFormset = inlineformset_factory(User, UserProfile,
                                                 fields=('apt', 'address', 'phone', 'city', 'state', 'zipcode'))
    formset = ProfileInlineFormset(instance=user)
    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            user_form = UserProfileForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return redirect('home_page')
        return render(request, "commten/account/account_update.html", {
            "noodle": pk,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied