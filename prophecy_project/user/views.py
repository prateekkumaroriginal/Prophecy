from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from posts.models import Post
from django.contrib import messages

# Create your views here.
def user_login(request):
    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return redirect('feed')
            else:
                messages.error(request, 'Invalid Credentials')
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'user/login_form.html', {'form': form})

@login_required
def index(request):
    current_user = request.user
    posts = Post.objects.filter(user=current_user)
    profile = current_user.profile
    return render(request, 'user/index.html', {'posts': posts, 'profile': profile})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'user/register_done.html')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'user/register.html', {'user_form':user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'user/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
