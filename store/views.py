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
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.all().filter(is_available=True)
        ordering = self.get_ordering()
        queryset = queryset.order_by(ordering)
        return queryset

    def get_ordering(self):
        sort_dict = {
            'id': 'id',
            'popular': '-count_orders',
            'newest': '-created_date',
            'low-price': 'price',
            'high-price': '-price'
        }
        if self.request.GET.get('orderby'):
            ordering = self.request.GET.get('orderby')
            ordering = sort_dict.get(ordering)
        else:
            ordering = sort_dict.get('id')
        return ordering

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


class SearchListView(ListView):
    """Find products by keyword"""

    template_name = 'store/store.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.products = None
        self.product_count = 0

    def get_queryset(self):
        if 'keyword' in self.request.GET:
            keyword = self.request.GET['keyword']
            self.products = Product.objects.order_by(
                '-created_date').filter(Q(product_name__icontains=keyword) |
                                        Q(description__icontains=keyword))
            self.product_count = self.products.count()
        return self.products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.products
        context['product_count'] = self.product_count
        return context
