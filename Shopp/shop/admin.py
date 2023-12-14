from django.contrib import admin

from .forms import SliderAdminForm, ProductAdminForm
from .models import (
    Category,
    Product,
    ProductImage,
    Specification,
    Slider,
    ProductComment,
    Contact,
)


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "parent_category", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ["parent_category"]

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",)}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent_category":
            kwargs["queryset"] = Category.objects.filter(parent_category__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SpecificationInline(admin.TabularInline):
    model = Specification
    extra = 1


class ImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ["name", "slug", "price", "available", "created", "updated", "uuid"]
    list_filter = ["available", "created", "updated"]
    list_editable = ["price", "available"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ImageInline, SpecificationInline]

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",)}


admin.site.register(Specification)


class SliderAdmin(admin.ModelAdmin):
    form = SliderAdminForm
    list_display = ["type", "image", "category", "product", "button"]

    fieldsets = [
        ("Image", {"fields": ["image"]}),
        ("Content", {"fields": ["description", "button"]}),
        (
            "Linking Options:(use category or product if you selected them in type!!!)",
            {"fields": ["type", "category", "product"]},
        ),
    ]


admin.site.register(Slider, SliderAdmin)


@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "product", "created_at", "hidden")
    list_filter = ("product", "created_at", "hidden")
    search_fields = ("name", "email", "text", "product__name")
    date_hierarchy = "created_at"
    actions = ["mark_as_hidden", "mark_as_visible"]

    def mark_as_hidden(modeladmin, request, queryset):
        queryset.update(hidden=True)

    mark_as_hidden.short_description = "Mark selected comments as hidden"

    def mark_as_visible(modeladmin, request, queryset):
        queryset.update(hidden=False)

    mark_as_visible.short_description = "Mark selected comments as visible"


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject")
    list_filter = ("name", "email", "subject")
    search_fields = ("name", "email", "subject", "message")
