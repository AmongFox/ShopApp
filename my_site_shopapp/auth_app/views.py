from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView

from .forms import UserSignupForm, UserLoginForm


class UserSignupView(FormView):
    """
    Регистрация нового пользователя
    form_class: Class - Модель заполнения данных в форме
    template_name: String - Шаблон отрисовки HTML кода
    success_url: String - Ссылка для перехода после регистрации
    """
    form_class = UserSignupForm
    template_name = 'signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(reverse('profiles_app:profiles_detail', kwargs={'username': user.username}))


class UserLoginView(FormView):
    form_class = UserLoginForm
    template_name = 'login.html'

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )

        if user is not None:
            login(self.request, user)
            return redirect(reverse('profiles_app:profiles_detail', kwargs={'username': user.username}))


class UserLogoutView(FormView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('auth_app:login'))
