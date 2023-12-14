from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
import uuid


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    parent_category = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="subcategories",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url_last(self):
        return reverse("shop:product_by_category_list", args=[self.slug])

    def get_absolute_url(self):
        slugs = [self.slug]
        parent = self.parent_category
        while parent:
            slugs.insert(0, parent.slug)
            parent = parent.parent_category
        return "/".join(slugs)


class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    smallDescription = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # fields for discount
    discount_type = models.CharField(
        max_length=10,
        choices=[
            ("percentage", "Percentage"),
            ("fixed", "Fixed"),
            ("none", "None"),
        ],
        default="none",
    )
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Enter the discount value. If Percentage, enter a value between 0 and 100. If Fixed, enter a fixed discount amount.",
    )
    discount_start_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The date and time when the discount starts.",
    )
    discount_end_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The date and time when the discount ends.",
    )

    class Meta:
        ordering = ("name",)
        index_together = (("id", "slug"),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.uuid, self.slug])

    def is_discount_active(self):
        now = timezone.now()
        start_date = self.discount_start_date
        end_date = self.discount_end_date

        if start_date is not None and end_date is not None:
            return start_date <= now <= end_date

        return False

    def get_discounted_price(self):
        if not self.is_discount_active():
            return self.price
        if self.discount_type == "percentage":
            discount_amount = (self.discount_value / 100) * self.price
        elif self.discount_type == "fixed":
            discount_amount = self.discount_value
        else:
            discount_amount = 0

        discounted_price = self.price - discount_amount
        return max(discounted_price, 0)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_images"
    )
    image = models.ImageField(upload_to="products/%Y/%m/%d")
    is_active = models.BooleanField(default=True, help_text="Check this for 'Active'")


class Specification(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="specifications"
    )
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.product}: {self.value}"


class Slider(models.Model):
    TYPE_CHOICES = [
        ("category", "Category"),
        ("product", "Product"),
        ("banner", "Prdouct - Banner"),
        ("banner2", "Category - Banner"),
        ("no url image", "no url image"),
    ]

    image = models.ImageField(upload_to="slider/")
    type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL
    )
    product = models.ForeignKey(
        Product, null=True, blank=True, on_delete=models.SET_NULL
    )
    description = models.TextField(blank=True)
    button = models.CharField(max_length=200, null=True, blank=True)

    def get_absolute_url(self):
        if self.type == "category" or self.type == "banner2":
            return reverse("shop:product_by_category_list", args=[self.category.slug])
        elif self.type == "product" or self.type == "banner":
            return reverse(
                "shop:product_detail", args=[str(self.product.uuid), self.product.slug]
            )
        elif self.type == "no url image":
            return "#"
        else:
            return "#"


class ProductComment(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()
    name = models.CharField(max_length=255)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    hidden = models.BooleanField(default=False)
    reply_to = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )

    def __str__(self):
        return f"Comment by {self.name} on {self.product}"

    def get_visible_replies(self):
        return self.replies.filter(hidden=False)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
