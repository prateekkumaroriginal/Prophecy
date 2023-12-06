from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, CommentForm
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
    # for comment
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        new_comment = comment_form.save(commit=False)
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        new_comment.post = post
        new_comment.save()
    else:
        comment_form = CommentForm()

    posts = Post.objects.all().order_by('-created')
    return render(request, 'posts/feed.html', {'posts': posts, 'comment_form': comment_form})

@login_required
def like_post(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    if post.liked_by.filter(id=request.user.id).exists():
        post.liked_by.remove(request.user)
    else:
        post.liked_by.add(request.user)
    return redirect('feed')