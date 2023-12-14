from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
)
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.views import logout_then_login
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import ListView, DetailView

from accounts.backends import CustomUserBackend
from .forms import (
    SignUpForm,
    LoginForm,
    EditProfileForm,
    CustomPasswordChangeForm,
    PasswordResetForm,
    CustomSetPasswordForm,
)
from .models import CustomUser
from .tokens import account_activation_token
from orders.models import Order


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]
            email = form.cleaned_data["email"]

            # check password
            if password1 != password2:
                form.add_error("password2", "Passwords do not match.")
                return render(request, "users/signup.html", {"form": form})
            # check email
            if get_user_model().objects.filter(email=email).exists():
                messages.error(
                    request,
                    "This email is already registered. Please use a different email.",
                )
                return render(request, "users/signup.html", {"form": form})

            # create temp user
            user = form.save(commit=False)
            user.username = form.cleaned_data["email"]
            user.set_password(password1)
            user.is_staff = False
            user.is_active = False
            user.save()

            # Generate a secure URL-friendly base64-encoded string for user ID
            uid = urlsafe_base64_encode(force_bytes(user.id)).rstrip("=")

            # Generate a secure token for the user
            token = account_activation_token.make_token(user)

            current_site = get_current_site(request)
            activation_link = f"http://{current_site.domain}{reverse('accounts:activate_account', args=[uid, token])}"

            # send activation mail
            message = (
                f"Click the following link to activate your account: {activation_link}"
            )
            send_mail(
                "Activate Your Account",
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )

            return render(
                request,
                "accounts/sign up/activation_sent.html",
                {"email_sent": True, "email": user.email},
            )

    else:
        form = SignUpForm()

    return render(request, "accounts/sign up/signup.html", {"form": form})


# check activaiton email and active user
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, "accounts/activation/activation_success.html")
    else:
        return render(request, "accounts/activation/activation_failure.html")


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            # authenticate with custom authentication for our CustomUsers
            user = authenticate(
                request,
                username=email,
                password=password,
                backend="accounts.backends.CustomUserBackend",
            )

            if user is not None:
                # use custom backend for our CustomUser.
                login(request, user, backend="accounts.backends.CustomUserBackend")
                return redirect("shop:product_list")
            else:
                messages.error(request, "Invalid login credentials.")
                return render(request, "accounts/login.html", {"form": form})
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    return logout_then_login(request, login_url="/")


def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("accounts:user_dashboard")
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, "accounts/edit_profile.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class OrderListView(ListView):
    model = Order
    template_name = "accounts/orders/order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        # Display only orders related to the logged-in user
        return Order.objects.filter(user=self.request.user).order_by("-created")


@method_decorator(login_required, name="dispatch")
class OrderDetailView(DetailView):
    model = Order
    template_name = "accounts/orders/order_detail.html"
    context_object_name = "order"

    def get_object(self, queryset=None):
        # Retrieve the order based on the order UUID
        return Order.objects.get(uuid=self.kwargs["order_uuid"])


@method_decorator(login_required, name="dispatch")
class UserDashboardView(LoginRequiredMixin, View):
    template_name = "accounts/user_dashboard.html"
    login_url = "accounts:login"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "accounts/password/change_password.html"
    success_url = reverse_lazy("accounts:password_change_done")


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = "accounts/password/password_change_done.html"


def resend_activation_email(request):
    user = request.user

    # Check if the user is not activated
    if not user.is_active:
        # Generate a secure URL-friendly base64-encoded string for user ID
        uid = urlsafe_base64_encode(force_bytes(user.id)).rstrip("=")

        # Generate a secure token for the user
        token = account_activation_token.make_token(user)

        current_site = get_current_site(request)
        activation_link = f"http://{current_site.domain}{reverse('accounts:activate_account', args=[uid, token])}"

        # Send activation mail
        message = (
            f"Click the following link to activate your account: {activation_link}"
        )
        send_mail(
            "Resend Activation Link", message, settings.DEFAULT_FROM_EMAIL, [user.email]
        )

        return render(
            request,
            "accounts/sign up/activation_sent.html",
            {"email_sent": True, "email": user.email},
        )
    else:
        messages.info(request, "Your account is already activated.")

    return redirect("accounts:dashboard")


class ForgetPasswordView(View):
    template_name = "accounts/password/password_forget.html"
    form_class = PasswordResetForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        email = request.POST.get("email")
        user = CustomUser.objects.filter(email=email).first()
        email_sent = False

        if user:
            # Use your custom token generator
            token = account_activation_token.make_token(user)

            # Generate a unique token for password reset
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

            # Construct the reset link
            reset_link = reverse(
                "accounts:recover_password", kwargs={"uidb64": uidb64, "token": token}
            )
            reset_url = request.build_absolute_uri(reset_link)

            # Send email with the reset link
            send_mail(
                "Password Reset",
                f"Click the following link to reset your password: {reset_url}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            email_sent = True

            messages.success(request, "Password reset email sent. Check your inbox.")
        else:
            messages.error(request, "No account found with this email address.")

        return render(
            request,
            "accounts/password/password_reset_email.html",
            {"email_sent": email_sent},
        )


class RecoverPasswordView(View):
    template_name = "accounts/password/password_reset.html"

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user and account_activation_token.check_token(user, token):
            # Token is valid, show the change password form
            form = CustomSetPasswordForm(user=user)
            context = {"form": form}
            return render(request, self.template_name, context)
        else:
            # Token is invalid or expired
            messages.error(request, "Invalid or expired link. Please try again.")
            return redirect("accounts:forget_password")

    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user and account_activation_token.check_token(user, token):
            form = CustomSetPasswordForm(user=user, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Password successfully changed.")
                return redirect("accounts:forgoten_password_changed")
            else:
                messages.error(request, "Please correct the errors below.")
        else:
            messages.error(request, "Invalid or expired link. Please try again.")

        context = {"form": form}
        return render(request, self.template_name, context)


class PasswordChangedView(View):
    template_name = "accounts/password/password_reset_done.html"

    def get(self, request):
        return render(request, self.template_name)
