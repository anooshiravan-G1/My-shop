import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, JsonResponse
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.html import escape
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
import pytz
from uuid import UUID

from cart.forms import CartAddProductForm
from .forms import ProductCommentForm, ContactForm
from .models import Category, Product, ProductImage, Slider, ProductComment


def paginate_data(data, request, items_per_page):
    page = request.GET.get("page", 1)
    paginator = Paginator(data, items_per_page)
    try:
        paginated_data = paginator.page(page)
    except PageNotAnInteger:
        paginated_data = paginator.page(1)
    except EmptyPage:
        paginated_data = paginator.page(paginator.num_pages)
    return paginated_data


def product_list(request):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).order_by("-updated")[:16]

    # get slider
    sliders = Slider.objects.all()
    latest_banner = Slider.objects.filter(type="banner").order_by("-id").first()
    latest_category_banners = Slider.objects.filter(type="banner2").order_by("-id")[:3]
    # get latest discounts
    discounted_products = Product.objects.filter(
        Q(
            discount_start_date__lte=datetime.datetime.now(pytz.utc),
            discount_end_date__gte=datetime.datetime.now(pytz.utc),
        ),
        ~Q(discount_type="none"),
    ).order_by("-discount_type", "-discount_start_date")[:4]

    return render(
        request,
        "shop/product/index.html",
        {
            "category": category,
            "categories": categories,
            "sliders": sliders,
            "latest_banner": latest_banner,
            "latest_category_banners": latest_category_banners,
            "products": products,
            "discounted_products": discounted_products,
        },
    )


def product_by_category_list(request, category_path=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).order_by("-updated")

    # handle category pages
    if not category_path or not category_path == "all":
        category_slugs = category_path.split("/")
        category = get_object_or_404(Category, slug=category_slugs[-1])
        # Include products of subcategories
        subcategories = Category.objects.filter(
            Q(id=category.id) | Q(parent_category=category.id)
        )
        products = products.filter(category__in=subcategories)

    paginated_products = paginate_data(products, request, 12)
    number_of_products = products.count()

    return render(
        request,
        "shop/product/category_list.html",
        {
            "category": category,
            "categories": categories,
            "products": paginated_products,
            "number_of_products": number_of_products,
        },
    )


def product_detail(request, product_uuid, product_slug):
    product = get_object_or_404(
        Product, uuid=product_uuid, slug=product_slug, available=True
    )
    comments = product.comments.all()
    cart_product_form = CartAddProductForm()
    category = product.category
    specifications = product.specifications.all()
    images = ProductImage.objects.filter(product=product)

    if request.method == "POST":
        if request.user.is_authenticated:
            comment_form = ProductCommentForm(request.POST)
            if comment_form.is_valid():
                # Check if the same data has been submitted recently
                if not ProductComment.objects.filter(
                    product=product,
                    user=request.user,
                    text=comment_form.cleaned_data["text"],
                    name=comment_form.cleaned_data["name"],
                    email=comment_form.cleaned_data["email"],
                ).exists():
                    comment = comment_form.save(commit=False)
                    comment.product = product
                    comment.user = request.user
                    comment.save()
        else:
            # Duplicate submission, redirect to avoid form resubmission
            return redirect(
                "shop:product_detail",
                product_uuid=product_uuid,
                product_slug=product_slug,
            )
    else:
        comment_form = ProductCommentForm()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        response_data = {
            "name": product.name,
            "price": str(product.price),
            "category": product.category.name,
            "discounted_price": str(product.get_discounted_price()),
            "description": product.description,
            "image": product.image.url,
            "product_url": product.get_absolute_url(),
        }
        print("json got " + product.name)
        return JsonResponse(response_data)

    return render(
        request,
        "shop/product/detail.html",
        {
            "product": product,
            "category": category,
            "images": images,
            "specifications": specifications,
            "cart_product_form": cart_product_form,
            "comments": comments,
            "comment_form": comment_form,
        },
    )


@csrf_exempt
@xframe_options_exempt
def search(request):
    query = request.GET.get("q")
    if query:
        query = escape(query)
        products = Product.objects.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(specifications__name__icontains=query)
            | Q(specifications__value__icontains=query)
        ).distinct()
    else:
        products = Product.objects.all()
    paginated_products = paginate_data(
        products, request, 12
    )  # Adjust '12' to the desired number of items per page

    return render(
        request, "shop/search.html", {"products": paginated_products, "query": query}
    )


def about_view(request):
    return render(request, "shop/others/about.html")


def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            message = "your message is sent to us."
            return render(request, "shop/others/contact_us.html", {"message": message})
    else:
        form = ContactForm()

    return render(request, "shop/others/contact_us.html", {"form": form})
