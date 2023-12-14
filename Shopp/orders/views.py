from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
import weasyprint

from cart.cart import Cart
from .forms import OrderCreateForm
from .models import Order
from .models import OrderItem


def send_order_notification(order_id):
    """
    Sends an e-mail notification when an order is successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = f"Order nr. {order.id}"
    message = f"Dear {order.first_name},\n\n" f"You have successfully placed an order."
    mail_sent = send_mail(
        subject, message, "admin@myshop.com", [order.email]
    )  # should be edited!!
    return mail_sent


@login_required
@transaction.atomic
def order_create(request):
    cart = Cart(request)
    # Check if the user's account is active
    if not request.user.is_active:
        return HttpResponseForbidden(
            "Your account is not active. Please contact support."
        )

    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            # Set the 'user' field to the currently logged-in user
            order.user = request.user
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            # clear the cart
            cart.clear()
            # send order notification
            send_order_notification(order.id)
            # set the order in the session
            request.session["order_id"] = order.id

            return redirect("accounts:user_dashboard")
    else:
        form = OrderCreateForm()
    return render(request, "orders/order/create.html", {"cart": cart, "form": form})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "admin/orders/order/detail.html", {"order": order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string("orders/order/pdf.html", {"order": order})
    response = HttpResponse(content_type="application/pdf")  # Common MIME types
    response[
        "Content-Disposition"
    ] = f"filename=order_{order.generate_order_number()}.pdf"
    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[
            weasyprint.CSS(str(settings.BASE_DIR) + "/staticfiles/css/pdf.css")
        ],
    )
    return response
