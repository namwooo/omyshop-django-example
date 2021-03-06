from django.shortcuts import render, get_object_or_404

from cart.forms import CartAddProductForm
from .recommender import Recommender
from .models import Category, Product


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category, available=True)
    return render(request, 'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_add_form = CartAddProductForm()

    r = Recommender()
    recommend_products = r.suggest_products([product])
    return render(request, 'shop/product/detail.html',
                  {'product': product,
                   'cart_add_form': cart_add_form,
                   'recommend_products': recommend_products})
