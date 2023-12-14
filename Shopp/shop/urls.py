from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("search/", views.search, name="search"),
    path("about/", views.about_view, name="about"),
    path("contact/", views.contact_us, name="contact"),
    path(
        "<uuid:product_uuid>/<slug:product_slug>/",
        views.product_detail,
        name="product_detail",
    ),
    path(
        "category/<path:category_path>/",
        views.product_by_category_list,
        name="product_by_category_list",
    ),
]
