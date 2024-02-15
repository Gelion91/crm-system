from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.views.generic import CreateView, DeleteView, UpdateView
from django_filters.views import FilterView

from core.filters import OrderFilter
from core.forms import AddOrderForm, ProductForm, ProductFormSet, \
    ProductFormSetHelper, UpdateOrderForm, DeliveryAddForm
from core.models import Order, Product, Logistics


class CustomHtmxMixin:
    def dispatch(self, request, *args, **kwargs):
        self.template_htmx = self.template_name
        if not self.request.META.get('HTTP_HX_REQUEST'):
            self.template_name = 'components/include_block.html'
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['template_htmx'] = self.template_htmx
        return super().get_context_data(**kwargs)


class OrderListView(FilterView):
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


@login_required(login_url='login.LoginUser')
@permission_required('core.update_order')
def update(request, order_id):
    data = get_object_or_404(Order, pk=order_id)
    form = UpdateOrderForm(instance=data)
    form2 = ProductForm()
    formset = ProductFormSet(queryset=data.product.all())
    helper = ProductFormSetHelper()

    if request.method == 'POST':
        form = AddOrderForm(request.POST, instance=data)
        form2 = ProductForm(request.POST, request.FILES)
        formset = ProductFormSet(request.POST, request.FILES)

        # Проверяем валидность форм
        if form.is_valid():
            form.save()

        if form2.is_valid():
            form2.save()
            product = Product.objects.get(id=form2.instance.id)
            data.product.add(product)
            data.save()

        if formset.is_valid():
            formset.save()
        return redirect('core:upd', order_id=order_id)

    context = {
        'data': data,
        'title': data.marker,
        'order_form': form,
        'product_form': form2,
        'formset': formset,
        'helper': helper,

    }
    return render(request, 'core/update_order.html', context)


# def delete_product(request, order, product_id):
#     order.product.remove(product_id.name)
#     Product.objects.get(pk=id).delete()
#     return redirect('upd', order_id=order.pk)


class AddProduct(LoginRequiredMixin, CreateView):
    form_class = ProductForm
    template_name = 'core/addorder.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        product_form = self.form_class(request.POST)
        if product_form.is_valid():
            return self.render_to_response(
                self.get_context_data(success=True)
            )
        else:
            return self.render_to_response(
                self.get_context_data(product_form=product_form)
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оформить заказ'
        return context


class DeliveryListView(FilterView):
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


class UpdateDelivery(UpdateView):
    model = Logistics
    form_class = DeliveryAddForm
    pk_url_kwarg = 'logistic_id'
    template_name = 'core/updatedelivery.html'

    def get_success_url(self):
        return reverse('core:update_delivery', kwargs={'logistic_id': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Доставка'
        return context
