from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import ( ListView, DetailView,
                    TemplateView, CreateView)

from .forms import *
from .models import *


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_ = CustomeUserModel.objects.get(id=self.request.user.id)
        slug_ = self.kwargs.get('slug'); form_ = None
        if slug_ == "change-profile-image":
            form_ = ChangeProfileImageForm()
            self.template_name = 'users/change_profile_image.html'
        context.update({'user': user_, 'form_' : form_})
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = ChangeProfileImageForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
        return redirect('users:profile')



class WalletView(LoginRequiredMixin, TemplateView):
    model = Wallet
    template_name = 'users/wallet.html'

class MemberShipView(LoginRequiredMixin, CreateView):
    template_name = 'users/membership.html'
    model = MemberShip
    form_class = MemberShipCreateForm

    




















