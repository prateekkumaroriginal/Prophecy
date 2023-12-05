from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from .models import Post
from django.db.models import Exists, OuterRef

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
    posts = Post.objects.annotate(
        liked_by_current_user=Exists(
            Post.objects.filter(id=OuterRef('id'), liked_by=request.user)
        )
    ).order_by('-created')
    return render(request, 'posts/feed.html', {'posts': posts})

@login_required
def like_post(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    if post.liked_by.filter(id=request.user.id).exists():
        post.liked_by.remove(request.user)
    else:
        post.liked_by.add(request.user)
    return redirect('feed')