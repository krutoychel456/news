from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from .forms import LoginForm, RegisterForm, ProfileModelForm
from django.contrib.auth.models import User
from django.http import Http404

def logout_view(request):
    logout(request)
    return redirect("/")

def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user_name = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=user_name, password=password)
        if user:
            login(request, user)
            return redirect("/")
    return render(request, 'profiles/form.html', {'form': form})

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user_name = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = User.objects.create_user(user_name, email, password)
        user.save()
        return redirect("/")
    return render(request, 'profiles/form.html', {'form': form, 'registration': True})
# Create your views here.

def detail_user_view(request, pk):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        raise Http404
    
    if request.method == 'POST':
        form = ProfileModelForm(request.POST, request.FILES)
        
    else:
        form = ProfileModelForm()
    if form.is_valid():
            obj = form.save(commit=False)
            obj.profile = user
            obj.save()
    return render(request, 'profiles/detail.html', {'profile': user, 'form': form})