from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView

from .forms import UserLoginForm, UserSignupForm


class UserSignupView(FormView):
    """
    Регистрация нового пользователя.

    :param form_class: Модель заполнения данных в форме.
    :type form_class: Class
    :param template_name: Шаблон отрисовки HTML кода.
    :type template_name: String
    :param success_url: Ссылка для перехода после регистрации.
    :type success_url: String

    :return: Редирект на страницу профиля пользователя после успешной регистрации.
    :rtype: HttpResponseRedirect
    """

    form_class = UserSignupForm
    template_name = "signup.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(
            reverse("profiles_app:profiles_detail", kwargs={"username": user.username})
        )


class UserLoginView(FormView):
    """
    Авторизация пользователя.

    :param form_class: Модель заполнения данных в форме.
    :type form_class: Class
    :param template_name: Шаблон отрисовки HTML кода.
    :type template_name: String

    :return: Редирект на страницу профиля пользователя после успешной авторизации.
    :rtype: HttpResponseRedirect
    """

    form_class = UserLoginForm
    template_name = "login.html"

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )

        if user is not None:
            login(self.request, user)
            return redirect(
                reverse(
                    "profiles_app:profiles_detail", kwargs={"username": user.username}
                )
            )


class UserLogoutView(FormView):
    """
    Выход пользователя из системы.

    :return: Редирект на страницу авторизации.
    :rtype: HttpResponseRedirect
    """

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse("auth_app:login"))
