from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from .models import VipOrder


class VipOrderCreateView(CreateView):
    model = VipOrder
    template_name = 'vip/create_vip_order.html'
    fields = ['name', 'email', 'phone', 'address', 'item_description',
              'item_image1', 'item_image2', 'item_image3']
    
    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        # return redirect('vip:vip-order')
        print(kwargs)


class VipOrderDetailView(DetailView):
    model = VipOrder
    template_name = 'vip/vip_order.html'
    context_object_name = 'vip_order'
