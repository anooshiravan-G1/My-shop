from django.urls import path
from .views import (
    signup,
    activate_account,
    user_login,
    logout_view,
    edit_profile,
    resend_activation_email,
    OrderListView,
    OrderDetailView,
    UserDashboardView,
    CustomPasswordChangeView,
    CustomPasswordChangeDoneView,
    ForgetPasswordView,
    RecoverPasswordView,
    PasswordChangedView,
)


app_name = "accounts"

urlpatterns = [
    path(
        "activate/<str:uidb64>/<str:token>/", activate_account, name="activate_account"
    ),
    path("resend_activation/", resend_activation_email, name="resend_activation"),
    path("login/", user_login, name="login"),
    path("signup/", signup, name="signup"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", UserDashboardView.as_view(), name="user_dashboard"),
    path("edit_profile/", edit_profile, name="edit_profile"),
    path(
        "change_password/", CustomPasswordChangeView.as_view(), name="change_password"
    ),
    path(
        "password_change_done/",
        CustomPasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("orders/", OrderListView.as_view(), name="order_list"),
    path("orders/<uuid:order_uuid>/", OrderDetailView.as_view(), name="order_detail"),
    path("forget_password/", ForgetPasswordView.as_view(), name="forget_password"),
    path(
        "recover_password/<str:uidb64>/<str:token>/",
        RecoverPasswordView.as_view(),
        name="recover_password",
    ),
    path(
        "forgoten_password_changed/",
        PasswordChangedView.as_view(),
        name="forgoten_password_changed",
    ),
]
