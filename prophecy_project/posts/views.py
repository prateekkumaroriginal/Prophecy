from django.shortcuts import render
from .forms import PostForm
from django.contrib.auth.decorators import login_required

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
            