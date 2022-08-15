from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import ( ListView, DetailView, UpdateView,
                    TemplateView, CreateView)

from users.models import MemberShip, Wallet, CustomeUserModel

from .models import Payment
from . import forms

class PaymentCreateView(LoginRequiredMixin, CreateView):
    model = Payment 
    template_name = 'users/deposit.html'
    form_class = forms.PaymentForm
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('payment:payment-history')

class ChangePaymentStatus(LoginRequiredMixin, UpdateView):
    model = Payment 
    form_class = forms.ChangePaymentStatusForm

    def form_valid(self, form):
        obj = self.get_object()
        if form.cleaned_data['status'] == 'Accept' and not obj.done:
            form.instance.done = True
            wallet_ = Wallet.objects.get(owner=form.instance.user)
            wallet_.amount = wallet_.amount + obj.amount
            wallet_.save()        
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('payment:payment-history')


class PaymentHistoryView(LoginRequiredMixin, TemplateView):
    model = Payment 
    template_name = 'users/payment_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_ = CustomeUserModel.objects.get(id=self.request.user.id)
        payment_ = None ;  payment_status = []
        if not self.request.user.is_admin:
            payment_ = Payment.objects.filter(user= user_)
        else:
            payment_ = Payment.objects.all()
            for i in payment_:
                payment_status.append(forms.ChangePaymentStatusForm(instance=i))
            payment_ = zip(payment_, payment_status)     
            self.template_name = 'users/payment_admin.html'
        context.update( {'payment' : payment_} )
        return context 


    










