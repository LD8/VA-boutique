from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView
from .models import VipOrder
from .forms import VipOrderForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from random import choice
from string import ascii_uppercase
from datetime import date


def vip_ref_number_generator():
    date_str = date.today().strftime('%d%m%y')
    random_str = "".join([choice(ascii_uppercase) for x in range(3)])
    return "VIP{}-{}".format(date_str, random_str)


def create_vip_order(request, **kwargs):
    
    # form = VipOrderForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        form = VipOrderForm(request.POST, request.FILES)
        print('form filled with POST data')
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            new_vip_order = form.save(commit=False)
            print('order created')
            new_vip_order.active = True
            print('order activated')
            new_vip_order.ref_number = vip_ref_number_generator()
            print('order ref number generated')
            new_vip_order.save()
            print('order saved')
            messages.info(request, _(
                "Thanks for your purchase, we will contact you soon!"))
            return redirect('vip:vip-order', new_vip_order.pk)
   

    form = VipOrderForm()
    print('form initiated')
    return render(request, "vip/create_vip_order.html", {'form': form})


# class VipOrderCreateView(CreateView):
#     model = VipOrder
#     template_name = 'vip/create_vip_order.html'
#     fields = ['name', 'email', 'phone', 'address', 'item_description',
#               'item_image1', 'item_image2', 'item_image3']

#     def post(self, *args, **kwargs):
#         super().post(*args, **kwargs)
#         # return redirect('vip:vip-order')
#         print(kwargs)


class VipOrderDetailView(DetailView):
    model = VipOrder
    template_name = 'vip/vip_order.html'
    context_object_name = 'vip_order'
