from django import forms
from django.core.validators import RegexValidator
from .models import Order


class OrderCreateForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={"size": "30", "class": "input-text input-text--primary-style"}
        ),
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={"size": "30", "class": "input-text input-text--primary-style"}
        ),
    )
    email = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.EmailInput(
            attrs={"size": "30", "class": "input-text input-text--primary-style"}
        ),
    )
    address = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.Textarea(
            attrs={"size": "30", "class": "input-text input-text--primary-style"}
        ),
    )
    postal_code = forms.CharField(
        max_length=10,
        validators=[RegexValidator(r"^\d{10}$", "Enter a valid Iranian postal code.")],
        label="Postal Code",
        widget=forms.TextInput(
            attrs={"size": "30", "class": "input-text input-text--primary-style"}
        ),
    )
    city = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={"size": "30", "class": "input-text input-text--primary-style"}
        ),
    )

    class Meta:
        model = Order
        fields = ["first_name", "last_name", "email", "address", "postal_code", "city"]
