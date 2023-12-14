from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from .models import CustomUser


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=False,
        help_text="Optional.",
        widget=forms.TextInput(
            attrs={"size": "30", "class": "input-text input-text--primary-style"}
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        help_text="Optional.",
        widget=forms.TextInput(
            attrs={"size": "30", "class": "input-text input-text--primary-style"}
        ),
    )
    email = forms.EmailField(
        max_length=254,
        help_text="Required. Enter a valid email address.",
        required=True,
        widget=forms.TextInput(
            attrs={"size": "30", "class": "input-text input-text--primary-style"}
        ),
    )
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        help_text="Optional.",
        widget=forms.TextInput(
            attrs={"size": "30", "class": "input-text input-text--primary-style"}
        ),
    )
    address = forms.CharField(
        max_length=255,
        required=False,
        help_text="Optional.",
        widget=forms.Textarea(
            attrs={"rows": 3, "cols": 65, "class": "text-area text-area--primary-style"}
        ),
    )
    zip_code = forms.CharField(
        max_length=10,
        required=False,
        help_text="Optional.",
        widget=forms.TextInput(
            attrs={"size": "30", "class": "input-text input-text--primary-style"}
        ),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"size": "30", "class": "input-text input-text--primary-style"}
        ),
        help_text="Required. Minimum 8 characters.",
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={"size": "30", "class": "input-text input-text--primary-style"}
        ),
        help_text="Enter the same password as above, for verification.",
    )

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "address",
            "zip_code",
            "password1",
            "password2",
        ]


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={"size": "30", "class": "input-text input-text--primary-style"}
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"size": "30", "class": "input-text input-text--primary-style"}
        ),
        required=True,
    )


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        required=False,
        help_text="Optional.",
        widget=forms.TextInput(
            attrs={"size": "30", "class": "input-text input-text--primary-style"}
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        help_text="Optional.",
        widget=forms.TextInput(
            attrs={"size": "30", "class": "input-text input-text--primary-style"}
        ),
    )
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        help_text="Optional.",
        widget=forms.TextInput(
            attrs={"size": "30", "class": "input-text input-text--primary-style"}
        ),
    )
    address = forms.CharField(
        max_length=255,
        required=False,
        help_text="Optional.",
        widget=forms.Textarea(
            attrs={"rows": 3, "cols": 65, "class": "text-area text-area--primary-style"}
        ),
    )
    zip_code = forms.CharField(
        max_length=10,
        required=False,
        help_text="Optional.",
        widget=forms.TextInput(
            attrs={"size": "30", "class": "input-text input-text--primary-style"}
        ),
    )

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "phone_number", "address", "zip_code"]


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(
            attrs={"size": "30", "class": "input-text input-text--primary-style"}
        ),
        help_text="Required. Minimum 8 characters.",
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={"size": "30", "class": "input-text input-text--primary-style"}
        ),
        help_text="Enter the same password as above, for verification.",
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(
            attrs={"size": "30", "class": "input-text input-text--primary-style"}
        ),
        help_text="Enter the same password as above, for verification.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["old_password"].label = "Old Password"
        self.fields["new_password1"].label = "New Password"
        self.fields["new_password2"].label = "Confirm New Password"


class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"size": "30", "class": "input-text input-text--primary-style"}
        )
    )


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter your new password",
                "class": "input-text input-text--primary-style",
            }
        ),
    )
    new_password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm your new password",
                "class": "input-text input-text--primary-style",
            }
        ),
    )
