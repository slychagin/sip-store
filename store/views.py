from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView

from category.models import Category
from store.models import Product


class StorePageView(ListView):
    """Rendering all products in store page"""
    template_name = 'store/store.html'
    queryset = Product.objects.all().filter(is_available=True).order_by('id')
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_count'] = context['products'].count()
        return context


class ProductsByCategoryListView(ListView):
    """Rendering products by category in store page"""
    template_name = 'store/store.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.products = None
        self.categories = None
        self.category_slug = None

    def get_queryset(self):
        """Return products by category"""
        self.categories = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        self.products = Product.objects.filter(category=self.categories, is_available=True)
        return self.products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.products
        context['product_count'] = self.products.count()
        return context


class ProductDetailView(DetailView):
    """Render a single product details page"""
    template_name = 'store/product_details.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.category_slug = None
        self.product_slug = None
        self.single_product = None

    def get_object(self, **kwargs):
        """Return single product by category and product slugs"""
        try:
            self.single_product = Product.objects.get(
                category__slug=self.kwargs['category_slug'],
                slug=self.kwargs['product_slug']
            )
        except ObjectDoesNotExist:
            raise Http404('Сторінку не знайдено')

        return self.single_product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['single_product'] = self.single_product
        return context


def search(request):
    """Find products by keyword"""
    # TODO: Настроить поиск в Postgres с использованием  расширения unaccent
    # TODO: Также проблема с поиском слов после кавычек в lower case.
    #  Например "Фітнес" находит если вводить Фітнес, по фітнес не ищет.

    products = None
    product_count = None
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by(
                '-created_date').filter(Q(product_name__icontains=keyword) |
                                        Q(description__icontains=keyword))
            product_count = products.count()

    context = {
        'product_count': product_count,
        'products': products
    }
    return render(request, 'store/store.html', context)
