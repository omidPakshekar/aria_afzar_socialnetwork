from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ( ListView, DetailView,
                    TemplateView, CreateView)


from .forms import ChangeProfileImageForm
from .models import CustomeUserModel

from payment.models import Payment

class ProfileView(TemplateView):
    template_name = 'users/profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_ = CustomeUserModel.objects.get(id=self.request.user.id)
        slug_ = self.kwargs.get('slug')
        payment_ = None
        form_ = None
        if slug_ == "payment-history":
            if not self.request.user.is_admin:
                payment_ = Payment.objects.filter(user= user_)
            else:
                payment_ = Payment.objects.all()     
            self.template_name = 'users/payment_history.html'
        if slug_ == "change-profile-image":
            form_ = ChangeProfileImageForm()
            self.template_name = 'users/change_profile_image.html'
        context.update({'user': user_, 'payment': payment_, 'form_' : form_})
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = ChangeProfileImageForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()

        return redirect('users:profile')




























