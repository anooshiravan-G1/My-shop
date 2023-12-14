from django import forms
from tinymce.widgets import TinyMCE
from .models import Slider, ProductComment, Product, Contact


class SliderAdminForm(forms.ModelForm):
    type = forms.ChoiceField(choices=Slider.TYPE_CHOICES)
    description = forms.CharField(
        widget=TinyMCE(
            attrs={"cols": 30, "rows": 30},
            mce_attrs={
                "plugins": "a11ychecker advcode advlist advtable anchor autocorrect autolink autoresize autosave casechange charmap checklist code codesample directionality editimage emoticons export footnotes formatpainter fullscreen help image importcss inlinecss insertdatetime link linkchecker lists media mediaembed mentions mergetags nonbreaking pagebreak pageembed permanentpen powerpaste preview quickbars save searchreplace table tableofcontents template tinycomments tinydrive tinymcespellchecker typography visualblocks visualchars wordcount",
                "theme": "silver",
                "toolbar_mode": "floating",
                "menubar": "file edit view insert format tools table help",
            },
        )
    )

    class Meta:
        model = Slider
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].required = False
        self.fields["product"].required = False

    def clean(self):
        cleaned_data = super().clean()
        type = cleaned_data.get("type")
        if type == "category":
            if not cleaned_data.get("category"):
                self.add_error("category", "Category is required for this type.")
        elif type == "product" or type == "banner":
            if not cleaned_data.get("product"):
                self.add_error("product", "Product is required for this type.")


class ProductCommentForm(forms.ModelForm):
    text = forms.CharField(
        label="YOUR REVIEW *",
        widget=forms.Textarea(attrs={"class": "text-area text-area--primary-style"}),
    )
    name = forms.CharField(
        label="NAME *",
        widget=forms.TextInput(attrs={"class": "input-text input-text--primary-style"}),
        required=False,
    )
    email = forms.EmailField(
        label="EMAIL *",
        widget=forms.TextInput(attrs={"class": "input-text input-text--primary-style"}),
    )

    class Meta:
        model = ProductComment
        fields = ["text", "name", "email"]


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "description": TinyMCE(
                attrs={"cols": 80, "rows": 10},
                mce_attrs={
                    "plugins": "a11ychecker advcode advlist advtable anchor autocorrect autolink autoresize autosave casechange charmap checklist code codesample directionality editimage emoticons export footnotes formatpainter fullscreen help image importcss inlinecss insertdatetime link linkchecker lists media mediaembed mentions mergetags nonbreaking pagebreak pageembed permanentpen powerpaste preview quickbars save searchreplace table tableofcontents template tinycomments tinydrive tinymcespellchecker typography visualblocks visualchars wordcount",
                    "theme": "silver",
                    "toolbar_mode": "floating",
                    "menubar": "file edit view insert format tools table help",
                },
            ),
        }


class ContactForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "input-text input-text--border-radius input-text--primary-style",
                "placeholder": "name (reqired)",
                "id": "c-name",
            }
        ),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "input-text input-text--border-radius input-text--primary-style",
                "placeholder": "email (reqired)",
                "id": "c-email",
            }
        ),
    )
    subject = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "input-text input-text--border-radius input-text--primary-style",
                "placeholder": "subject (reqired)",
                "id": "c-subject",
            }
        ),
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "text-area text-area--primary-style",
                "placeholder": "your message (reqired)",
                "id": "c-message",
            }
        ),
    )

    class Meta:
        model = Contact
        fields = ["name", "email", "subject", "message"]
