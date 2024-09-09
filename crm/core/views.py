import asyncio
import datetime
import decimal
import json

from django.db.models import Q
from pytz import timezone

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import dateformat
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from django.views.generic.base import ContextMixin, TemplateView
from django.views.generic.edit import FormMixin
from django_filters.views import FilterView
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from sorl.thumbnail import get_thumbnail

from core.filters import OrderFilter, ProductFilter, DeliveryFilter, DeliveryListFilter
from core.forms import AddOrderForm, ProductForm, ProductFormSet, \
    ProductFormSetHelper, UpdateOrderForm, DeliveryAddForm, PackedImageForm, \
    LogisticImageForm, AddAccountForm, ProductNotesForm, DeliveryNotesForm, ChangeOrderDateForm, ChangeProductDateForm, \
    ChangeDeliveryDateForm, UpdateOrderFormTest, DateFilterForm, SpendingForm, InvoiceForm
from core.models import Order, Product, Logistics, ImagesProduct, PackedImagesProduct, ImagesLogistics, Account, \
    NotesProduct, NotesDelivery, Notification, FilesProduct, ReadNotification, Spendings
from core.utils import get_course, get_invoice
from crm import settings
from crm.settings import LOGIN_URL


def getcourse(request):
    crs = get_course()
    tz = timezone('Europe/Moscow')
    response = {
        'course': str(crs.course),
        'date': dateformat.format(datetime.datetime.now(tz=tz), settings.DATE_FORMAT).lstrip('0'),
    }

    return HttpResponse(json.dumps(response), content_type='application/json')


def get_notification(request):
    tz = timezone('Europe/Moscow')
    response = {'notification': [{
        'id': notification.pk,
        'owner': notification.owner.username if notification.owner else notification.subject_owner.username,
        'action': notification.action,
        'subject': notification.subject,
        'date': dateformat.format(notification.date_create, settings.DATE_FORMAT).lstrip('0'),
    } for notification in Notification.objects.filter(readed=False, subject_owner=request.user).filter(
        ~Q(notifications__readers__in=[request.user.pk]))]
    }
    return HttpResponse(json.dumps(response), content_type='application/json')


def read_notification(request):
    notification_id = request.POST.get("id").split('_')[-1]
    notification = Notification.objects.get(pk=notification_id)
    read = ReadNotification(notification=notification)
    read.save()
    read.readers.add(request.user)

    response = {'notification': Notification.objects.filter(readed=False, subject_owner=request.user).filter(
        ~Q(notifications__readers__in=[request.user.pk])).count()}
    print(response)

    return HttpResponse(json.dumps(response), content_type='application/json')


def read_all_notification(request):
    notifications = Notification.objects.filter(readed=False, subject_owner=request.user).filter(
        ~Q(notifications__readers__in=[request.user.pk]))
    for notification in notifications:
        read = ReadNotification(notification=notification)
        read.save()
        read.readers.add(request.user)
        print(read)

    response = {'notification': Notification.objects.filter(readed=False, subject_owner=request.user).filter(
        ~Q(notifications__readers__in=[request.user.pk])).count()}
    print(response)

    return HttpResponse(json.dumps(response), content_type='application/json')


class CustomHtmxMixin:
    def dispatch(self, request, *args, **kwargs):
        self.template_htmx = self.template_name
        if not self.request.META.get('HTTP_HX_REQUEST'):
            self.template_name = 'components/include_block.html'
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['template_htmx'] = self.template_htmx
        return super().get_context_data(**kwargs)


class OrderListView(LoginRequiredMixin, PermissionRequiredMixin, FilterView):
    model = Order
    paginate_by = 16
    template_name = 'core/order_list2.html'
    filterset_class = OrderFilter
    permission_required = 'core.view_order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderFilter.form
        context['title'] = 'Список заказов'
        return context

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.filter(result=False)
        elif self.request.user.has_perm('core.view_order'):
            return Order.objects.filter(result=False).filter(owner=self.request.user)


class AllOrderListView(OrderListView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderFilter.form
        context['title'] = 'Список активных заказов'
        return context

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        elif self.request.user.has_perm('core.view_order'):
            return Order.objects.filter(owner=self.request.user)


class WaitPayOrderListView(OrderListView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderFilter.form
        context['title'] = 'Заказы - ожидают оплаты'
        return context

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.filter(status='Ожидает отправки')
        elif self.request.user.has_perm('core.view_order'):
            return Order.objects.filter(status='Ожидает отправки').filter(owner=self.request.user)


class FinishOrderListView(OrderListView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderFilter.form
        context['title'] = 'Список завершенных заказов'
        return context

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.filter(result=True)
        elif self.request.user.has_perm('core.view_order'):
            return Order.objects.filter(result=True).filter(owner=self.request.user)


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

    def get_form_kwargs(self):
        kwargs = super(AddOrder, self).get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs

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
@permission_required('core.change_order')
def update(request, order_id, *args, **kwargs):
    my_kwargs = {'current_user': request.user}
    data = get_object_or_404(Order, pk=order_id)
    form = UpdateOrderFormTest(instance=data, **my_kwargs)
    form2 = ProductForm()
    helper = ProductFormSetHelper()

    if request.method == 'POST':
        form = UpdateOrderFormTest(request.POST, instance=data, **my_kwargs)
        form2 = ProductForm(request.POST)
        files = ProductForm(request.FILES)
        print(form2.errors)
        # Проверяем валидность форм
        if form.is_valid():
            print('форма1 валидна')
            form.save()

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
    return render(request, 'core/order_upd.html', context)


def add_product(request):
    print(request.POST)
    print(request.FILES)
    order_id = request.POST.get("id")
    product_marker = request.POST.get("product_marker")
    name = request.POST.get("name")
    url = request.POST.get("url")
    number_order = request.POST.get("number_order")
    price = request.POST.get("price")
    price_company = request.POST.get("price_company")
    fraht = request.POST.get("fraht")
    fraht_company = request.POST.get("fraht_company")
    quantity = request.POST.get("quantity")
    comment = request.POST.get("comment")
    arrive = True if request.POST.get("arrive") == 'true' else False
    paid = True if request.POST.get("paid") == 'true' else False

    product = Product(product_marker=product_marker, name=name, url=url, number_order=number_order,
                      price=decimal.Decimal(price),
                      price_company=decimal.Decimal(price_company), fraht=decimal.Decimal(fraht),
                      fraht_company=decimal.Decimal(fraht_company), quantity=quantity,
                      arrive=arrive, paid=paid, owner=request.user, comment=comment
                      )
    product.save()
    print(product.full_price)
    print(product.full_price_company)
    order = Order.objects.get(pk=order_id)
    order.product.add(product)
    order.save()

    if request.FILES.getlist('image'):
        for f in request.FILES.getlist('image'):
            img = ImagesProduct(product=product, image=f)
            img.save()
    if request.FILES.getlist('file'):
        for f in request.FILES.getlist('file'):
            file = FilesProduct(product=product, file=f)
            file.save()

    total_price = sum(i.full_price for i in order.product.all())
    print(total_price)
    total_price_company = sum(i.full_price_company for i in order.product.all())
    print(total_price_company)
    response = {'product_id': product.pk,
                'product_marker': product.product_marker,
                'name': product.name,
                'total_price': float(total_price),
                'total_price_company': float(total_price_company),
                'product_image': [i.image.url for i in product.images.all() if product.images.all()],
                'image': [(prod.image.url, get_thumbnail(prod.image, '100x56', crop='center', quality=99).url) for prod
                          in product.images.all()],
                'product_url': reverse('core:upd_product', args=(product.pk,))
                }

    print(response)

    return HttpResponse(json.dumps(response), content_type='application/json')


class UpdateProduct(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    pk_url_kwarg = 'product_id'
    template_name = 'core/edit_product.html'
    permission_required = 'core.change_product'

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')
    
    
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
            if request.FILES.getlist('file'):
                for f in request.FILES.getlist('file'):
                    file = FilesProduct(product=self.object, file=f)
                    file.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.instance.id = self.object.pk
        form.instance.owner = self.object.owner
        form.instance.date_create = self.object.date_create
        form.instance.last_updater = self.request.user
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

    def handle_no_permission(self):
        # add custom message
        messages.error(self.request, 'You have no permission')
        return super(DeleteProduct, self).handle_no_permission()

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

    def handle_no_permission(self):
        # add custom message
        messages.error(self.request, 'You have no permission')
        return super(DeleteImage, self).handle_no_permission()

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


class DeliveryListView(LoginRequiredMixin, FilterView):
    model = Logistics
    paginate_by = 16
    template_name = 'core/delivery_list.html'
    filterset_class = DeliveryListFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Завершенные доставки'
        context['form'] = DeliveryListFilter.form
        return context

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.groups.filter(
                name='logist').exists() or self.request.user.groups.filter(name='china').exists():
            return Logistics.objects.filter(third_step=True)
        else:
            return Logistics.objects.filter(third_step=True).filter(product__owner=self.request.user.pk).distinct()


class AddDelivery(LoginRequiredMixin, CreateView):
    model = Logistics
    form_class = DeliveryAddForm
    template_name = 'core/add_delivery.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оформить доставку'
        context['products'] = Product.objects.prefetch_related('logistics').filter(paid=True, arrive=True).filter(
            logistics__product__isnull=True)
        return context

    def get_success_url(self):
        return reverse('core:status_delivery')

    def get_form_kwargs(self):
        kwargs = super(AddDelivery, self).get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.last_updater = self.request.user
        return super().form_valid(form)


def show_product_info(request):
    product_id = request.POST.get("id")
    product = Product.objects.get(pk=product_id)

    response = {
        'marker': product.product_marker,
        'name': product.name,
        'owner': product.owner.username if product.owner else None,
        'price_company': float(product.price_company),
        'price_client': float(product.price),
        'image': [i.image.url for i in product.images.all() if product.images.all()],
        'user': request.user.username if request.user else None,
    }

    return HttpResponse(json.dumps(response), content_type='application/json')


class UpdateDelivery(LoginRequiredMixin, UpdateView):
    model = Logistics
    form_class = DeliveryAddForm
    pk_url_kwarg = 'logistic_id'
    template_name = 'core/updatedelivery.html'

    def get_success_url(self):
        return reverse('core:update_delivery', kwargs={'logistic_id': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super(UpdateDelivery, self).get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Доставка'
        context['data'] = [{'id': i.id, 'full_price': i.full_price} for i in context['form'].fields['product'].queryset]
        context['orders'] = {product.order.first(): [product for product in product.order.first().product.filter(logistics=self.object)] for product in self.object.product.all()}
        print(context['orders'])
        return context

    def form_valid(self, form):
        form.instance.last_updater = self.request.user
        return super().form_valid(form)


class ProductStatus(LoginRequiredMixin, FormMixin, FilterView):
    model = Product
    paginate_by = 16
    template_name = 'core/productstatus.html'
    filterset_class = ProductFilter
    form_class = PackedImageForm

    def get_queryset(self):
        queryset = super(ProductStatus, self).get_queryset()
        return queryset.filter(logistics=None)

    def get_success_url(self):
        return reverse('core:status_product')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductFilter.form
        context['image_form'] = PackedImageForm
        context['notes_form'] = ProductNotesForm
        context['title'] = 'Статус товаров'
        context['logist'] = self.request.user.groups.filter(name='logist').exists()
        context['china'] = self.request.user.groups.filter(name='china').exists()
        print(get_course())
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
    print(request.user)
    product_id = request.POST.get("id")
    product = Product.objects.get(pk=product_id)
    checked = request.POST.get("checked")
    if checked == 'true':
        product.paid = True
    else:
        product.paid = False
    product.last_updater = request.user
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
    product.last_updater = request.user
    product.save()

    response = {
        'OK': 200
    }
    return JsonResponse(response)


def get_price(request):
    product_id = request.POST.get("id")
    product = Product.objects.get(pk=product_id)
    order = Order.objects.get(product=product)
    response = {
        'product_marker': product.product_marker,
        'name': product.name,
        'number_order': product.number_order,
        'price': product.price,
        'price_company': product.price_company,
        'margin_product': product.margin_product,
        'fraht': product.fraht,
        'fraht_company': product.fraht_company,
        'full_price_company': product.full_price_company,
        'full_price': product.full_price,
        'order': order.marker,
        'order_rate': order.exchange_for_client,
        'order_rate_company': order.exchange_for_company
    }

    return JsonResponse(response)


def save_image_product(request):
    image = request.FILES.get('image')
    product_id = request.POST.get("id").split('_')[-1]
    print(image)
    print(product_id)
    product = Product.objects.get(pk=product_id)
    img = PackedImagesProduct(product=product, image=image)
    img.save()
    print(img.image.url)

    response = {
        'image_mini': get_thumbnail(img.image, '64', crop='center', quality=99).url,
        'image': img.image.url,
        'image_id': img.pk,
        'product_id': product.pk,
    }

    # response = {'ok':200}
    return HttpResponse(json.dumps(response), content_type='application/json')


def delete_image_product(request):
    img_id = request.POST.get("id").split('_')[-1]
    print(img_id)
    product_id = Product.objects.get(packed_images=img_id)
    img = PackedImagesProduct.objects.get(pk=img_id)
    img.delete()
    response = {
        'image_id': img_id,
        'logistic_id': product_id.pk
    }

    # response = {'ok':200}
    return HttpResponse(json.dumps(response), content_type='application/json')


def save_notes_product(request):
    note = request.POST.get("note")
    product_id = request.POST.get("id")
    print(note)
    print(product_id)
    comment = NotesProduct(product=Product.objects.get(pk=product_id), comment=note, owner=request.user)
    comment.save()
    print(comment.date_create)
    response = {
        'note': note,
        'product': product_id,
        'comment_id': comment.pk,
        'user': request.user.username,
        'date': dateformat.format(datetime.datetime.now(tz=timezone('Europe/Moscow')), settings.DATE_FORMAT).lstrip('0'),
    }
    print(response)

    return HttpResponse(json.dumps(response), content_type='application/json')


def delete_notes_product(request):
    notes_id = request.POST.get("id").split('_')[-1]
    print(notes_id)
    comment = NotesProduct.objects.get(pk=notes_id)
    comment.delete()
    response = {
        'notes_id': notes_id,
    }
    print(response)
    return HttpResponse(json.dumps(response), content_type='application/json')


class DeletePackedImage(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = PackedImagesProduct
    permission_required = 'core.delete_packedimagesproduct'
    context_object_name = 'packed_image'
    pk_url_kwarg = "packed_image_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def handle_no_permission(self):
        # add custom message
        messages.error(self.request, 'You have no permission')
        return super(DeletePackedImage, self).handle_no_permission()

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


class DeliveryStatus(LoginRequiredMixin, FormMixin, FilterView):
    model = Logistics
    paginate_by = 16
    template_name = 'core/status_delivery.html'
    filterset_class = DeliveryFilter
    form_class = LogisticImageForm

    def get_queryset(self):
        return Logistics.objects.filter(third_step=False)

    def get_success_url(self):
        return reverse('core:status_delivery')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductFilter.form
        context['image_form'] = LogisticImageForm
        context['notes_form'] = DeliveryNotesForm
        context['title'] = 'Статус грузов'
        context['logist'] = self.request.user.groups.filter(name='logist').exists()
        context['china'] = self.request.user.groups.filter(name='china').exists()
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


def load_delivery_info(request):
    delivery_id = request.POST.get("id")
    logistic = Logistics.objects.get(pk=delivery_id)
    products = logistic.product.all()
    response = {
        'delivery_id': delivery_id,
        'product_image': {product.name: [get_thumbnail(prod.image, '64x64', crop='center', quality=99).url for prod in
                                         product.images.all()] for product in products},
        'product_packed_image': {product.name: [prod.image.url for prod in product.packed_images.all()] for product in
                                 products},
    }
    print(response)

    return HttpResponse(json.dumps(response), content_type='application/json')


def save_image(request):
    image = request.FILES.get('image')
    logistic_id = request.POST.get("id").split('_')[-1]
    print(image)
    print(logistic_id)
    logistic = Logistics.objects.get(pk=logistic_id)
    img = ImagesLogistics(logistic=logistic, image=image)
    img.save()
    print(img.image.url)

    response = {
        'image_mini': get_thumbnail(img.image, '64', crop='center', quality=99).url,
        'image': img.image.url,
        'image_id': img.pk,
        'delivery_id': logistic.pk,
    }

    # response = {'ok':200}
    return HttpResponse(json.dumps(response), content_type='application/json')


def delete_image_logistic(request):
    img_id = request.POST.get("id").split('_')[-1]
    logistic_id = Logistics.objects.get(logistic_images=img_id)
    img = ImagesLogistics.objects.get(pk=img_id)
    img.delete()
    response = {
        'image_id': img_id,
        'logistic_id': logistic_id.pk
    }

    # response = {'ok':200}
    return HttpResponse(json.dumps(response), content_type='application/json')


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
    logistic.last_updater = request.user
    logistic.save()

    response = {
        'OK': 200
    }
    return JsonResponse(response)


def save_notes_delivery(request):
    note = request.POST.get("note")
    delivery_id = request.POST.get("id")
    print(note)
    print(delivery_id)
    comment = NotesDelivery(delivery=Logistics.objects.get(pk=delivery_id), comment=note, owner=request.user)
    comment.save()
    print(comment.date_create)
    response = {
        'note': note,
        'delivery': delivery_id,
        'comment_id': comment.pk,
        'user': request.user.username,
        'date': dateformat.format(datetime.datetime.now(tz=timezone('Europe/Moscow')), settings.DATE_FORMAT).lstrip('0'),
    }
    print(response)

    return HttpResponse(json.dumps(response), content_type='application/json')


def delete_notes_delivery(request):
    notes_id = request.POST.get("id").split('_')[-1]
    print(notes_id)
    comment = NotesDelivery.objects.get(pk=notes_id)
    comment.delete()
    response = {
        'notes_id': notes_id,
    }
    print(response)
    return HttpResponse(json.dumps(response), content_type='application/json')


def change_delivery(request):
    delivery_id = request.POST.get("id").split('_')[-1]
    marker = request.POST.get("marker")
    weight = request.POST.get("weight")
    volume = request.POST.get("volume")
    density = request.POST.get("density")
    places = request.POST.get("places")
    print(request.POST)
    logistic = Logistics.objects.get(pk=delivery_id)
    logistic.marker, logistic.weight, logistic.volume, logistic.density, logistic.places = marker, weight, volume, density, places
    logistic.save()
    response = {
        'marker': marker,
        'delivery_id': delivery_id,
    }
    print(response)

    return HttpResponse(json.dumps(response), content_type='application/json')


class DeleteLogisticImage(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ImagesLogistics
    permission_required = 'core.delete_imageslogistics'
    context_object_name = 'image'
    pk_url_kwarg = "logistic_image_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def handle_no_permission(self):
        # add custom message
        messages.error(self.request, 'You have no permission')
        return super(DeleteLogisticImage, self).handle_no_permission()

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


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


class AddAccount(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Account
    permission_required = 'core.add_account'
    form_class = AddAccountForm
    template_name = 'core/add_account.html'

    # On successful form submission
    def get_success_url(self):
        return reverse('core:add_account')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить аккаунт'
        context['accounts'] = [{
            'user': i,
            'accounts': [acc for acc in i.accounts.all()]
        }
            for i in User.objects.all()]
        print(context['accounts'])
        return context


class DeleteAccount(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Account
    permission_required = 'core.delete_account'
    context_object_name = 'account'
    pk_url_kwarg = "account_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


def change_datetime(request):
    form = ChangeOrderDateForm()
    form2 = ChangeProductDateForm()
    form3 = ChangeDeliveryDateForm()

    if request.method == 'POST' and 'btnform1' in request.POST:
        form = ChangeOrderDateForm(request.POST)
        if form.is_valid():
            order = form.cleaned_data['order']
            ord = Order.objects.get(pk=order.pk)
            ord.date_create = form.cleaned_data['date']
            ord.save()
        return redirect('core:change_date')
    if request.method == 'POST' and 'btnform2' in request.POST:
        form2 = ChangeProductDateForm(request.POST)
        if form2.is_valid():
            product = form2.cleaned_data['product']
            prod = Product.objects.get(pk=product.pk)
            prod.date_create = form2.cleaned_data['date']
            prod.save()
        return redirect('core:change_date')
    if request.method == 'POST' and 'btnform3' in request.POST:
        form3 = ChangeDeliveryDateForm(request.POST)
        if form3.is_valid():
            delivery = form3.cleaned_data['delivery']
            deliv = Logistics.objects.get(pk=delivery.pk)
            deliv.date_create = form3.cleaned_data['date']
            deliv.save()
        return redirect('core:change_date')

    else:
        form = ChangeOrderDateForm()
        form2 = ChangeProductDateForm()
        form3 = ChangeDeliveryDateForm()
    context = {
        'order_form': form,
        'product_form': form2,
        'delivery_form': form3,
        'products': []
    }

    return render(request, 'core/change_date.html', context)


class ViewNotifications(FilterView):
    model = Notification
    paginate_by = 32
    template_name = 'core/notifications_list.html'

    # filterset_class = ProductFilter
    # form_class = PackedImageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Журнал событий'
        return context


class FinanceList(TemplateView):
    template_name = 'core/finance_list.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        start = request.GET.get("date_start")
        finish = request.GET.get("date_finish")
        payment_method = request.GET.get("payment_method", 'Все оплаты')
        manager = request.GET.get("user")

        if not start:
            start = '2024-05-01'
        if not finish:
            finish = datetime.date.today()

        if start is not None and finish is not None:
            orders = Order.objects.filter(date_create__range=[start, finish])
            logistics = Logistics.objects.filter(date_create__range=[start, finish])
            spendings = Spendings.objects.filter(date_create__range=[start, finish])
            context['text_message'] = f'Поиск данных с {start} по {finish}'
        else:
            orders = Order.objects.all()
            logistics = Logistics.objects.all()
            spendings = Spendings.objects.all()

        if payment_method != 'Все оплаты':
            orders = orders.filter(paid_method=payment_method)

        if manager:
            orders = orders.filter(owner=manager)
            logistics = logistics.filter(owner=manager)

        context['title'] = 'Финансы общее'
        context['order_price_client'] = sum(order.total_price for order in orders)
        context['order_price_client_rub'] = sum(order.total_price_rub for order in orders)
        context['order_price_company'] = sum(order.total_price_company for order in orders)
        context['order_price_company_rub'] = sum(order.total_price_rub_company for order in orders)
        context['order_price_profit'] = sum(order.profit for order in orders)

        context['delivery_full_price_client'] = sum(logistic.full_price for logistic in logistics)
        context['delivery_full_price_rub'] = round(
            sum(logistic.full_price * logistic.exchange_rate for logistic in logistics), 2)
        context['delivery_company_price'] = sum(logistic.company_delivery_price for logistic in logistics)
        context['delivery_company_price_rub'] = round(
            sum(logistic.company_delivery_price * logistic.exchange_rate for logistic in logistics), 2)

        context['spendings'] = sum(spending.price for spending in spendings)

        context['total_order'] = context['order_price_client'] - context['order_price_company']
        context['total_order_rub'] = context['order_price_client_rub'] - context['order_price_company_rub']
        context['total_delivery'] = context['delivery_full_price_client'] - context['delivery_company_price']
        context['total_delivery_rub'] = context['delivery_full_price_rub'] - context['delivery_company_price_rub']
        context['filter_form'] = DateFilterForm(request.GET)
        return self.render_to_response(context)


class AddSpending(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Spendings
    permission_required = 'core.add_spendings'
    form_class = SpendingForm
    template_name = 'core/add_spending.html'

    # On successful form submission
    def get_success_url(self):
        return reverse('core:finance_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить расходы'
        return context


class SpendingList(LoginRequiredMixin, PermissionRequiredMixin, FilterView):
    model = Spendings
    permission_required = 'core.add_spendings'
    template_name = 'core/list_spendings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Расходы'
        return context


class SpendingUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Spendings
    form_class = SpendingForm
    pk_url_kwarg = 'spending_id'
    template_name = 'core/update_spending.html'
    permission_required = 'core.change_spendings'

    def get_success_url(self):
        return reverse('core:list_spendings')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменить затрату'
        return context


def create_invoice(request):
    delivery_id = request.POST.get("id").split('_')[-1]
    logistic = Logistics.objects.get(pk=delivery_id)
    file = get_invoice(logistic)
    response = {
        'file_name': file.url.split('/')[-1],
        'file_url': file.url,
        'delivery_id': delivery_id,
    }
    return HttpResponse(json.dumps(response), content_type='application/json')