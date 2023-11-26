from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .froms import LoginForm
from django.http import HttpResponse

# Create your views here.
def user_login(request):
    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return HttpResponse('User Authenticated')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
    return render(request, 'user/login_form.html', {'form': form})
