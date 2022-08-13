from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import (CreateView, DetailView, UpdateView, ListView, FormView)

from .models import Payment
from . import forms

class PaymentView(LoginRequiredMixin, CreateView):
    model = Payment 
    template_name = 'payment/payment.html'
    context_object_name = 'object_list'
    form_class = forms.PaymentForm
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')






