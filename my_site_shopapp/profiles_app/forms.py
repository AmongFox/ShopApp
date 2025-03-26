from django import forms
from django.utils.translation import gettext_lazy as _

from .models import UserProfileModel


class UserProfileForm(forms.ModelForm):
    name = forms.CharField(label=_('Имя'), max_length=30, required=False)
    surname = forms.CharField(label=_('Фамилия'), max_length=30, required=False)
    bio = forms.CharField(
        label=_('О себе'),
        help_text=_('Максимум 200 символов'),
        max_length=200,
        widget=forms.Textarea,
        required=False,
    )
    avatar = forms.ImageField(label=_('Аватар'), required=False)

    class Meta:
        model = UserProfileModel
        fields = [
            "name",
            "surname",
            "bio",
            "avatar",
        ]

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
        return profile
