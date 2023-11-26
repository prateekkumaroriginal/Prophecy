from django.shortcuts import render
from .froms import LoginForm

# Create your views here.
def login(request):
    form = LoginForm()
    return render(request, 'user/login_form.html', {'form': form})
    