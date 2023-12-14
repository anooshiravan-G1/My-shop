from coupons.models import Coupon
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.crypto import get_random_string
from django.db import models
import uuid
from shop.models import Product
from accounts.models import CustomUser


class Order(models.Model):
    # i want to save orders history, even if user removed.
    user = models.ForeignKey(
        CustomUser, blank=True, null=True, on_delete=models.SET_NULL
    )
    first_name = models.CharField("first name", max_length=50)
    last_name = models.CharField("last name", max_length=50)
    email = models.EmailField("e-mail")
    address = models.CharField("address", max_length=250)
    postal_code = models.CharField("postal code", max_length=20)
    city = models.CharField("city", max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    coupon = models.ForeignKey(
        Coupon, related_name="orders", null=True, blank=True, on_delete=models.SET_NULL
    )
    discount = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal(100))

    def generate_order_number(self):
        # Get the first 4 characters of the UUID
        uuid_prefix = str(self.uuid)[:4]

        # Format the created date as YYYYMMDD
        date_suffix = self.created.strftime("%Y%m%d")

        # Remove the decimal point from the price and convert to string
        price_without_decimal = str(self.get_total_cost()).replace(".", "")

        # Create the order number by combining the elements
        order_number = f"{uuid_prefix}-{price_without_decimal}-{date_suffix}"

        return order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
