from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse

class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        if request.user.is_authenticated:
            return '/some-url/'
        else:
            return '/accounts/login/'

    def get_inactive_user_url(self, request, user):
        return '/accounts/inactive/'


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        url = reverse('account_confirm_email', args=[emailconfirmation.key])
        ret = request.build_absolute_uri(url)
        return ret