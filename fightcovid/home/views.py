from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
# Create your views here.

# This is a little complex because we need to detect when we are
# running in various configurations

class HomeView(View):
    def get(self, request) :
        print(request.get_host())
        host = request.get_host()
        islocal = host.find('localhost') >= 0 or host.find('127.0.0.1') >= 0
        context = {
            'installed' : settings.INSTALLED_APPS,
            'islocal' : islocal
        }
        return render(request, 'home/main.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST, label_suffix='')
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            url = request.POST.get('next', reverse('qa:all'))
            return HttpResponseRedirect(url)
    else:
        form = UserCreationForm(label_suffix='')
    return render(request, 'registration/register.html', {'form': form})

