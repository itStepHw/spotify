from django.shortcuts import render, redirect
from .form import UserAuthForm, SignInForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test


def register(request):
    if request.user.is_authenticated:
        redirect('category_view')
    if request.method == 'POST':
        reg_form = UserAuthForm(request.POST)
        if reg_form.is_valid():
            user = reg_form.save()
            login(request, user)
            return redirect('category_view')

    register_form = UserAuthForm()
    context = {'register_form': register_form}
    return render(request, 'user_app/register.html', context)


def login_view(request):
    if request.user.is_authenticated:
        redirect('category_view')
    if request.method == 'POST':
        fw = SignInForm(request.POST)
        print('login 1')
        if fw.is_valid():
            print('login 2')
            username = fw.cleaned_data['username']
            password = fw.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('category_view')

    login_form = SignInForm()
    context = {'login_form': login_form}
    return render(request, 'user_app/login.html', context)


# def check_user_permision(request):
#     return user.is_superuser


# @user_passes_test(check_user_permision, login_url='login')



def logout_view(request):
    logout(request)
    return redirect('login')
