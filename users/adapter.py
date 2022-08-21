from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.country = data.get('country')
        user.gender = data.get('gender')
        user.year_of_birth = data.get('year_of_birth')
        user.month_of_birth = data.get('month_of_birth')
        user.day_of_birth = data.get('day_of_birth')
        
        user.save()
        return user