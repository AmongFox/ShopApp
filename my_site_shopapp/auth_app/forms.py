from django import forms
import phonenumbers
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

from .models import CustomUserModel
from profiles_app.models import UserProfileModel


class UserSignupForm(forms.ModelForm):
    username = forms.CharField(
        label=_("Имя пользователя"),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Имя пользователя"),
            }
        ),
        max_length=40,
        required=True,
    )
    password = (
        forms.CharField(
            label=_("Пароль"),
            widget=forms.PasswordInput(
                attrs={
                    "placeholder": _("Введите пароль"),
                }
            ),
            required=True,
        ),
    )
    password_confirm = forms.CharField(
        label=_("Подтверждение пароля"),
        widget=forms.PasswordInput(
            attrs={
                "placeholder": _("Повторите пароль"),
            }
        ),
        required=True,
    )
    email = forms.EmailField(
        label=_("Почта"),
        widget=forms.EmailInput(
            attrs={
                "placeholder": _("example@mail.com"),
            }
        ),
        required=True,
    )
    phone_number = forms.CharField(
        label=_("Номер телефона"),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("+71234567890"),
            }
        ),
        min_length=11,
        max_length=12,
        required=True,
    )

    class Meta:
        model = CustomUserModel
        fields = (
            "username",
            "password",
            "password_confirm",
            "email",
            "phone_number",
        )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        email = cleaned_data.get("email")
        phone_number = cleaned_data.get("phone_number")

        # Проверка существования пользователя с таким же username
        if CustomUserModel.objects.filter(username=username).exists():
            raise forms.ValidationError(
                _("Пользователь с таким именем уже существует.")
            )

        # Проверка существования пользователя с таким же email
        if CustomUserModel.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Пользователь с таким email уже существует."))

        # Проверка существования пользователя с таким же номером телефона
        if CustomUserModel.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError(
                _("Пользователь с таким номером телефона уже существует.")
            )

        # Проверка схожести паролей
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError(_("Пароли не совпадают."))

        return cleaned_data

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        try:
            parsed_number = phonenumbers.parse(phone_number, "RU")
            if not phonenumbers.is_valid_number(parsed_number):
                raise forms.ValidationError(
                    f"{phone_number} недействительный номер телефона."
                )
        except phonenumbers.NumberParseException:
            raise forms.ValidationError(
                f"{phone_number} недопустимый формат номера телефона."
            )
        return phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            UserProfileModel.objects.create(
                user=user,
            )
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Имя пользователя"), max_length=40, required=True
    )
    password = forms.CharField(
        label=_("Пароль"), widget=forms.PasswordInput, required=True
    )

    class Meta:
        model = CustomUserModel
        fields = (
            "username",
            "password",
        )
