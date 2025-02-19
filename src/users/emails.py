from djoser import email
from djoser import utils
from djoser.conf import settings
from django.contrib.auth.tokens import default_token_generator

class CustomActivationEmail(email.ActivationEmail):
    template_name = 'email/activation.html'
    subject = 'Welcome! Activate your account'

    print(template_name)

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.ACTIVATION_URL.format(**context)
        context['custom_variable'] = 'Hello, this is a custom variable!'
        return context