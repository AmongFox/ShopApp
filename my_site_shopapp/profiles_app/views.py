from auth_app.models import CustomUserModel
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView

from .forms import UserProfileForm
from .models import UserProfileModel


class ProfilesDetailView(LoginRequiredMixin, DetailView):
    template_name = "profiles-detail.html"
    form_class = UserProfileForm
    context_object_name = "profile"

    def get_object(self, queryset=None):
        username = self.kwargs.get("username")
        user = get_object_or_404(CustomUserModel, username=username)
        return UserProfileModel.objects.get_or_create(user=user)[0]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_user"] = self.request.user
        return context


class ProfilesUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = "profiles-update.html"
    context_object_name = "profile"
    form_class = UserProfileForm
    model = UserProfileModel

    def has_permission(self):
        return (
            self.kwargs.get("username") == self.request.user.username
            or self.request.user.is_superuser
        )

    def handle_no_permission(self):
        return render(self.request, "error/profiles-forbidden.html")

    def get_object(self, queryset=None):
        username = self.kwargs.get("username")
        user = get_object_or_404(CustomUserModel, username=username)
        return get_object_or_404(UserProfileModel, user=user)

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.save()
        return redirect(
            reverse(
                "profiles_app:profiles_detail",
                kwargs={"username": self.kwargs.get("username")},
            )
        )


class ProfilesListView(LoginRequiredMixin, ListView):
    template_name = "profiles-list.html"
    context_object_name = "profiles"
    queryset = UserProfileModel.objects.all().select_related("user")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_user"] = self.request.user
        return context
