from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ( ListView, DetailView,
                    TemplateView, CreateView)



from .forms import ChangeProfileImageForm
from .models import CustomeUserModel

from payment.models import Payment
from payment.forms import ChangePaymentStatusForm

class ProfileView(TemplateView):
    template_name = 'users/profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_ = CustomeUserModel.objects.get(id=self.request.user.id)
        slug_ = self.kwargs.get('slug')
        payment_ = None ; form_ = None; payment_status = []
        if slug_ == "payment-history":
            if not self.request.user.is_admin:
                payment_ = Payment.objects.filter(user= user_)
                self.template_name = 'users/payment_history.html'
            else:
                payment_ = Payment.objects.all()
                for i in payment_:
                    payment_status.append(ChangePaymentStatusForm(instance=i))
                payment_ = zip(payment_, payment_status)     
                self.template_name = 'users/payment_admin.html'
        if slug_ == "change-profile-image":
            form_ = ChangeProfileImageForm()
            self.template_name = 'users/change_profile_image.html'
        context.update({'user': user_, 'payment': payment_, 'form_' : form_, 'payment_status': payment_status })
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = ChangeProfileImageForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()

        return redirect('users:profile')




























