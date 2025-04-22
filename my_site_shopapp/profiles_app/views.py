from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView

from auth_app.models import CustomUserModel

from .forms import UserProfileForm
from .models import UserProfileModel


class ProfilesDetailView(LoginRequiredMixin, DetailView):
    """View для отображения детальной информации профиля пользователя.

    Attributes:
        template_name (str): Путь к шаблону страницы.
        form_class (Form): Класс формы для редактирования профиля.
        context_object_name (str): Имя переменной контекста для профиля.

    Methods:
        get_object: Получает объект профиля пользователя или создает новый, если его нет.
        get_context_data: Добавляет текущего пользователя в контекст шаблона.
    """

    template_name = "profiles-detail.html"
    form_class = UserProfileForm
    context_object_name = "profile"

    def get_object(self, queryset=None):
        """Получает объект профиля по username из URL.

        Args:
            queryset: QuerySet для поиска объекта (не используется).

        Returns:
            UserProfileModel: Объект профиля пользователя.

        Note:
            Если профиля не существует, создает новый.
        """
        username = self.kwargs.get("username")
        user = get_object_or_404(CustomUserModel, username=username)
        return UserProfileModel.objects.get_or_create(user=user)[0]

    def get_context_data(self, **kwargs):
        """Добавляет дополнительный контекст в шаблон.

        Args:
            **kwargs: Дополнительные аргументы контекста.

        Returns:
            dict: Контекст для рендеринга шаблона.
        """
        context = super().get_context_data(**kwargs)
        context["my_user"] = self.request.user
        return context


class ProfilesUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """View для обновления информации профиля пользователя.

    Attributes:
        template_name (str): Путь к шаблону страницы.
        context_object_name (str): Имя переменной контекста для профиля.
        form_class (Form): Класс формы для редактирования профиля.
        model (Model): Модель профиля пользователя.

    Methods:
        has_permission: Проверяет права доступа к редактированию профиля.
        handle_no_permission: Обрабатывает случай отказа в доступе.
        get_object: Получает объект профиля для редактирования.
        form_valid: Обрабатывает валидную форму и перенаправляет на страницу профиля.
    """

    template_name = "profiles-update.html"
    context_object_name = "profile"
    form_class = UserProfileForm
    model = UserProfileModel

    def has_permission(self):
        """Проверяет, имеет ли пользователь право редактировать профиль.

        Returns:
            bool: True если пользователь - владелец профиля или суперпользователь.
        """
        return (
            self.kwargs.get("username") == self.request.user.username
            or self.request.user.is_superuser
        )

    def handle_no_permission(self):
        """Обрабатывает случай отказа в доступе.

        Returns:
            HttpResponse: Рендер страницы с ошибкой доступа.
        """
        return render(self.request, "error/profiles-forbidden.html")

    def get_object(self, queryset=None):
        """Получает объект профиля для редактирования.

        Args:
            queryset: QuerySet для поиска объекта (не используется).

        Returns:
            UserProfileModel: Объект профиля пользователя.

        Raises:
            Http404: Если профиль не найден.
        """
        username = self.kwargs.get("username")
        user = get_object_or_404(CustomUserModel, username=username)
        return get_object_or_404(UserProfileModel, user=user)

    def form_valid(self, form):
        """Обрабатывает валидную форму и сохраняет изменения.

        Args:
            form: Валидная форма профиля.

        Returns:
            HttpResponseRedirect: Перенаправление на страницу профиля.
        """
        profile = form.save(commit=False)
        profile.save()
        return redirect(
            reverse(
                "profiles_app:profiles_detail",
                kwargs={"username": self.kwargs.get("username")},
            )
        )


class ProfilesListView(LoginRequiredMixin, ListView):
    """View для отображения списка всех профилей пользователей.

    Attributes:
        template_name (str): Путь к шаблону страницы.
        context_object_name (str): Имя переменной контекста для списка профилей.
        queryset (QuerySet): QuerySet всех профилей с предварительной загрузкой пользователей.

    Methods:
        get_context_data: Добавляет текущего пользователя в контекст шаблона.
    """

    template_name = "profiles-list.html"
    context_object_name = "profiles"
    queryset = UserProfileModel.objects.all().select_related("user")

    def get_context_data(self, **kwargs):
        """Добавляет дополнительный контекст в шаблон.

        Args:
            **kwargs: Дополнительные аргументы контекста.

        Returns:
            dict: Контекст для рендеринга шаблона.
        """
        context = super().get_context_data(**kwargs)
        context["my_user"] = self.request.user
        return context