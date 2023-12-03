from django.shortcuts import render
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from .models import Post

# Create your views here.
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
    else:
        form = PostForm()
    return render(request, 'posts/create.html', {'form': form})
            
@login_required
def my_posts(request):
    current_user = request.user
    posts = Post.objects.filter(user=current_user)
    profile = current_user.profile
    return render(request, 'user/index.html', {'posts': posts, 'profile': profile})

def feed(request):
    posts = Post.objects.all().order_by('-created')
    return render(request, 'posts/feed.html', {'posts': posts})