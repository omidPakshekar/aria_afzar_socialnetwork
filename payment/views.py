from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import (CreateView, DetailView, UpdateView, ListView, FormView)

from users.models import Wallet

from .models import Payment
from . import forms

class PaymentCreateView(LoginRequiredMixin, CreateView):
    model = Payment 
    template_name = 'payment/payment.html'
    context_object_name = 'object_list'
    form_class = forms.PaymentForm
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users:profile')

class ChangePaymentStatus(LoginRequiredMixin, UpdateView):
    model = Payment 
    form_class = forms.ChangePaymentStatusForm

    def form_valid(self, form):
        obj = self.get_object()
        print('satus=', form.cleaned_data['status'])
        print('instance=', form.instance.user)
        
        if form.cleaned_data['status'] == 'Accept' and not obj.done:
            form.instance.done = True
            wallet_ = Wallet.objects.get(owner=form.instance.user)
            wallet_.amount = wallet_.amount + obj.amount
            wallet_.save()        
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('users:profile')






