import json

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from django.views.generic.base import ContextMixin
from django.views.generic.edit import FormMixin
from django_filters.views import FilterView
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

from time import time

from core.filters import OrderFilter, ProductFilter
from core.forms import AddOrderForm, ProductForm, ProductFormSet, \
    ProductFormSetHelper, UpdateOrderForm, DeliveryAddForm, ProductImageInlineFormset, PackedImageForm, \
    LogisticImageForm
from core.models import Order, Product, Logistics, ImagesProduct, PackedImagesProduct, ImagesLogistics
from crm.settings import LOGIN_URL


class CustomHtmxMixin:
    def dispatch(self, request, *args, **kwargs):
        self.template_htmx = self.template_name
        if not self.request.META.get('HTTP_HX_REQUEST'):
            self.template_name = 'components/include_block.html'
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['template_htmx'] = self.template_htmx
        return super().get_context_data(**kwargs)


class OrderListView(LoginRequiredMixin, FilterView):
    model = Order
    paginate_by = 16
    template_name = 'core/order_list2.html'
    filterset_class = OrderFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderFilter.form
        context['title'] = 'Список заказов'
        return context


class ActiveOrderListView(OrderListView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderFilter.form
        context['title'] = 'Список активных заказов'
        return context

    def get_queryset(self):
        return Order.objects.filter(result=False)


class WaitPayOrderListView(OrderListView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderFilter.form
        context['title'] = 'Заказы - ожидают оплаты'
        return context

    def get_queryset(self):
        return Order.objects.filter(status='На оплату')


class FinishOrderListView(OrderListView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderFilter.form
        context['title'] = 'Список завершенных заказов'
        return context

    def get_queryset(self):
        return Order.objects.filter(result=True)


class AddOrder(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Order
    permission_required = 'core.add_order'
    form_class = AddOrderForm
    template_name = 'core/addorder.html'

    # On successful form submission
    def get_success_url(self):
        return reverse('core:upd', args=(self.object.pk,))

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оформить заказ'
        return context


class DeleteOrder(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Order
    permission_required = 'core.delete_order'
    context_object_name = 'order'
    pk_url_kwarg = "order_id"
    success_url = reverse_lazy("core:home")


def _get_form(request, formcls, prefix):
    data = request.POST if prefix in request.POST else None
    return formcls(data, prefix=prefix)


@login_required(login_url=LOGIN_URL)
@permission_required('core.update_order')
def update(request, order_id):
    data = get_object_or_404(Order, pk=order_id)
    form = UpdateOrderForm(instance=data)
    form2 = ProductForm()
    helper = ProductFormSetHelper()

    if request.method == 'POST':
        form = UpdateOrderForm(request.POST, instance=data)
        form2 = ProductForm(request.POST, request.FILES)

        # Проверяем валидность форм
        if form.is_valid():
            print('форма1 валидна')
            form.save()

        if form2.is_valid():
            print('форма2 валидна')
            form2.save()
            product = Product.objects.get(id=form2.instance.id)
            data.product.add(product)
            data.save()
        return redirect('core:upd', order_id=order_id)

    context = {
        'data': data,
        'title': data.marker,
        'order_form': form,
        'product_form': form2,
        'helper': helper,
        'products': []

    }
    for prod in data.product.all():
        context['products'].append({'product': prod, 'images': prod.images.all()})
    return render(request, 'core/update_order.html', context)


class AddProduct(LoginRequiredMixin, CreateView):
    form_class = ProductForm
    template_name = 'core/add_product.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оформить заказ'
        context['ord'] = kwargs.get('pk')
        return context


class UpdateProduct(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    pk_url_kwarg = 'product_id'
    template_name = 'core/edit_product.html'

    def get_success_url(self):
        return reverse('core:upd', kwargs={'order_id': Order.objects.get(product=self.object).pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Продавец'
        context['photos'] = ImagesProduct.objects.filter(product=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ProductForm(request.POST)
        files = request.FILES.getlist('image')
        if form.is_valid():
            if files:
                for f in files:
                    img = ImagesProduct(product=self.object, image=f)
                    img.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.instance.id = self.object.pk
        self.object = form.save()
        return super().form_valid(form)


class DeleteProduct(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = 'core.delete_product'
    context_object_name = 'product'
    pk_url_kwarg = "product_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


class DeleteImage(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ImagesProduct
    permission_required = 'core.delete_imagesproduct'
    context_object_name = 'image'
    pk_url_kwarg = "image_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('core:upd_product', kwargs={'product_id': self.object.product.pk})


class DeliveryListView(LoginRequiredMixin, FilterView):
    model = Logistics
    paginate_by = 16
    template_name = 'core/delivery_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Доставки'
        return context


class AddDelivery(LoginRequiredMixin, CreateView):
    model = Logistics
    form_class = DeliveryAddForm
    template_name = 'core/add_delivery.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оформить доставку'
        return context


class UpdateDelivery(LoginRequiredMixin, UpdateView):
    model = Logistics
    form_class = DeliveryAddForm
    pk_url_kwarg = 'logistic_id'
    template_name = 'core/updatedelivery.html'

    def get_success_url(self):
        return reverse('core:update_delivery', kwargs={'logistic_id': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Доставка'
        context['data'] = [{'id': i.id, 'full_price': i.full_price} for i in context['form'].fields['product'].queryset]
        return context


class ProductStatus(LoginRequiredMixin, FormMixin, FilterView):
    model = Product
    paginate_by = 16
    template_name = 'core/productstatus.html'
    filterset_class = ProductFilter
    form_class = PackedImageForm

    def get_queryset(self):
        return Product.objects.filter(logistics=None)

    def get_success_url(self):
        return reverse('core:status_product')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductFilter.form
        context['image_form'] = PackedImageForm
        context['title'] = 'Статус товаров'
        return context

    def post(self, request, *args, **kwargs):
        image_form = PackedImageForm(request.POST or None, request.FILES or None)
        prod_id = request.POST.get('id')
        if image_form.is_valid():
            return self.form_valid(image_form, prod_id)
        else:
            return self.form_invalid(image_form)

    def form_valid(self, form, prod_id):
        """If the form is valid, save the associated model."""
        files = form.cleaned_data["image"]
        for img in files:
            img = PackedImagesProduct(product=Product.objects.get(pk=prod_id), image=img)
            img.save()
        return super().form_valid(form)


def change_status_paid(request):
    """Проверка доступности логина"""
    product_id = request.POST.get("id")
    product = Product.objects.get(pk=product_id)
    checked = request.POST.get("checked")
    if checked == 'true':
        product.paid = True
    else:
        product.paid = False
    product.save()

    response = {
        'OK': 200
    }
    return JsonResponse(response)


def change_status_arrive(request):
    """Проверка доступности логина"""
    product_id = request.POST.get("id")
    product = Product.objects.get(pk=product_id)
    checked = request.POST.get("checked")
    if checked == 'true':
        product.arrive = True
    else:
        product.arrive = False
    product.save()

    response = {
        'OK': 200
    }
    return JsonResponse(response)


def get_price(request):
    product_id = request.POST.get("id")
    product = Product.objects.get(pk=product_id)
    response = {
        'price': product.full_price
    }

    return JsonResponse(response)


# Временно не работает, отключил в productstatus.html

def save_image(request):
    print('Работает')
    image = request.FILES.get('image')

    print(image)
    product_id = request.POST.get("id")
    print(product_id)
    product = Product.objects.get(pk=product_id)
    img = PackedImagesProduct(product=product, image=image)
    img.save()

    response = {
        'image': img.image.url,
        'product': product_id
    }

    return HttpResponse(json.dumps(response), content_type='application/json')


class DeliveryStatus(LoginRequiredMixin, FormMixin, FilterView):
    model = Logistics
    paginate_by = 16
    template_name = 'core/status_delivery.html'
    filterset_class = ProductFilter
    form_class = LogisticImageForm

    def get_queryset(self):
        return Logistics.objects.all()

    def get_success_url(self):
        return reverse('core:status_delivery')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductFilter.form
        context['image_form'] = LogisticImageForm
        context['title'] = 'Статус грузов'
        return context

    def post(self, request, *args, **kwargs):
        image_form = LogisticImageForm(request.POST or None, request.FILES or None)
        logistic_id = request.POST.get('id')
        if image_form.is_valid():
            return self.form_valid(image_form, logistic_id)
        else:
            return self.form_invalid(image_form)

    def form_valid(self, form, logistic_id):
        """If the form is valid, save the associated model."""
        files = form.cleaned_data["image"]
        for img in files:
            img = ImagesLogistics(logistic=Logistics.objects.get(pk=logistic_id), image=img)
            img.save()
        return super().form_valid(form)


def change_logistic_status(request):
    """Проверка доступности логина"""
    logistic_id = request.POST.get("id")
    logistic = Logistics.objects.get(pk=logistic_id)
    checked = request.POST.get("checked")
    attribut = request.POST.get("attribut").split('-')[0]
    if checked == 'true':
        result = True
    else:
        result = False
    if attribut == 'first_step':
        logistic.first_step = result
    elif attribut == 'second_step':
        logistic.second_step = result
    else:
        logistic.third_step = result
    logistic.save()

    response = {
        'OK': 200
    }
    return JsonResponse(response)


class DeleteDelivery(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Logistics
    permission_required = 'core.delete_logistics'
    context_object_name = 'logistic'
    pk_url_kwarg = "logistic_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')