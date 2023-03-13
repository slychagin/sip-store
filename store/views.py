import json

from crispy_forms.utils import render_crispy_form
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.context_processors import csrf
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import ModelFormMixin

from category.models import Category
from orders.models import OrderItem
from store.forms import ReviewRatingForm
from store.models import Product, ProductGallery, ProductInfo, ReviewRating
from telebot.telegram import (
    send_to_telegram_moderate_new_review_message,
    send_to_telegram_moderate_updated_review_message
)


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


class ProductDetailView(ModelFormMixin, DetailView):
    """Render a single product details page with ReviewRating form"""
    template_name = 'store/product_details.html'
    form_class = ReviewRatingForm

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None
        self.category_slug = None
        self.product_slug = None
        self.single_product = None

    def get_object(self, **kwargs):
        """Return single product by category and product slugs"""
        self.single_product = get_object_or_404(
            Product,
            category__slug=self.kwargs['category_slug'],
            slug=self.kwargs['product_slug']
        )
        return self.single_product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_gallery = ProductGallery.objects.filter(product_id=self.single_product.id)
        images = [i for i in product_gallery if i.image != '']
        videos = [i for i in product_gallery if i.video != '']

        related_products = Product.related_products.through.objects.filter(from_product_id=self.single_product.id)
        reviews = ReviewRating.objects.filter(product=self.get_object(), is_moderated=True)

        context['single_product'] = self.single_product
        context['images'] = images
        context['videos'] = videos
        context['related_products'] = [item.to_product for item in related_products]
        context['reviews'] = reviews
        context['form'] = ReviewRatingForm()

        try:
            context['info'] = ProductInfo.objects.all()[0].description
        except IndexError:
            context['info'] = ''
        return context

    def post(self, request, *args, **kwargs):
        is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        if is_ajax:
            form = self.get_form()
            self.object = self.get_object()

            if form.is_valid():
                return self.form_valid(form)
            else:
                resp = {'success': False}
                csrf_context = {}
                csrf_context.update(csrf(request))
                review_form = render_crispy_form(form, context=csrf_context)
                resp['html'] = review_form
            return HttpResponse(json.dumps(resp), content_type='application/json')

    def form_valid(self, form):
        """
        Checks if the user has bought the given product.
        If yes, it saves the review in the database,
        if it is a new review, and overwrites it if there was already.
        """
        product = self.get_object()

        # Check the user
        email = form.cleaned_data['email']
        ordered_products = [item.product for item in OrderItem.objects.filter(user_email=email)]

        if product not in ordered_products:
            resp = {'info': True}
            return HttpResponse(json.dumps(resp), content_type='application/json')
        else:
            try:
                # Update exists review
                review = ReviewRating.objects.get(product=product, email=email)
                review.is_moderated = False
                form = ReviewRatingForm(self.request.POST, instance=review)
                form.save()
                resp = {'update': True}

                # Send message to telegram
                send_to_telegram_moderate_updated_review_message()

                return HttpResponse(json.dumps(resp), content_type='application/json')

            except ObjectDoesNotExist:
                # Save new review
                review_form = form.save(commit=False)
                review_form.product = product
                review_form.ip = self.request.META.get('REMOTE_ADDR')
                form.save()
                resp = {'success': True}

                # Send message to telegram
                send_to_telegram_moderate_new_review_message()

                return HttpResponse(json.dumps(resp), content_type='application/json')

    def get_success_url(self):
        return HttpResponseRedirect(reverse('product_details', args=[
            self.kwargs['category_slug'],
            self.kwargs['product_slug']
        ]))


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
