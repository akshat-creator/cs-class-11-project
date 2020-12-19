from django.shortcuts import render, get_object_or_404
from .models import Product, OrderItem, Order,BillingAddress
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect,reverse
from django.utils import timezone
from django.contrib import messages
from .forms import CheckoutForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.



def aboutus(request):
    return render(request, 'aboutus.html')


class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {}
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context['form'] = form
            context['object'] = order
            print(context)
            return render(self.request, 'checkout.html', context)
        except ObjectDoesNotExist :
            messages.error(self.request, "You do not have an ACTIVE order")
            return redirect("/")


    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                appartment_address = form.cleaned_data.get('appartment_address')
                country = form.cleaned_data.get('country')
                state = form.cleaned_data.get('state')
                zip_code = form.cleaned_data.get('zip_code')
                name_on_card = form.cleaned_data.get('name_on_card')
                pp_card = form.cleaned_data.get('pp_card')
                expiry_date = form.cleaned_data.get('expiry_date')
                cvv = form.cleaned_data.get('cvv')
                billing_address = BillingAddress(
                    user = self.request.user,
                    street_address = street_address,
                    appartment_address = appartment_address,
                    country = country,
                    state = state,
                    zip_code = zip_code,
                    name_on_card = name_on_card,
                    pp_card = pp_card,
                    expiry_date = expiry_date,
                    cvv = cvv
                )
                billing_address.save()
                order.billingaddress = billing_address
                order.save()
                return redirect('https://www.tomorrowtides.com/sucker.html')
            messages.warning(self.request, "Failed Checkout")
            return redirect('/')


        except ObjectDoesNotExist :
            messages.error(self.request, "You do not have an ACTIVE order")
            return redirect("/")



                

def ppcards(request):
    return render(request, 'ppcards.html')

def product(request):
    return render(request,'product.html')

class HomeView(ListView):
    model = Product
    template_name = 'index.html'

class ProductView(DetailView):
    model = Product
    template_name = 'product.html'

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This Item's quantity was updated.")
        else:
            messages.info(request, "This Item was added to your cart.")
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This Item was added to your cart.")
    return redirect('product', slug=slug)
     
@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This Item was removed to your cart.")
            return redirect('product', slug=slug)
        else:
            messages.info(request, "This Item was not in your cart.")
            return redirect('product', slug=slug)
    else: 
        messages.info("You do not have an active order.")
        return redirect('product', slug=slug)
    return redirect('product', slug=slug)
