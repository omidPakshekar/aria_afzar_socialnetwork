import random
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.sites.shortcuts import get_current_site
from users.models import ActivationKey
class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.name = data.get('name')
        user.country = data.get('country')
        user.gender = data.get('gender')
        user.year_of_birth = data.get('year_of_birth')
        user.month_of_birth = data.get('month_of_birth')
        user.day_of_birth = data.get('day_of_birth')
        
        user.save()
        return user
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        activation_code = ActivationKey.objects.create(user=emailconfirmation.email_address.user, key=random.randint(100000, 999999))   
        activation_code.save()
        
        current_site = get_current_site(request)
        activate_url = self.get_email_confirmation_url(request, emailconfirmation)
        print(activation_code)
        ctx = {
            "user": emailconfirmation.email_address.user,
            "verification_code": activation_code.key,
            "current_site": current_site,
            # "key": emailconfirmation.key,
        }
        if signup:
            email_template = "account/email/email_confirmation_signup"
        else:
            email_template = "account/email/email_confirmation"
        self.send_mail(email_template, emailconfirmation.email_address.email, ctx)