from django.contrib.auth.models import User
from django.template import loader, Context
from utils.html2text import html2text
from django.core.mail import EmailMultiAlternatives
import os


def get_logged_user(request):
    user = request.user
    try:
        return User.objects.get(pk=user.pk)
    except User.DoesNotExist:
        return None


def send_email(template_file, context_data, subject, recepiants=[]):
    from_email = os.environ.get('DEFAULT_FROM_EMAIL')
    template = loader.get_template(template_name=template_file)
    context = Context(context_data)
    html = template.render(context)
    plain_text = html2text(html)
    msg = EmailMultiAlternatives(subject, plain_text, from_email, recepiants)
    msg.attach_alternative(html, "text/html")
    try:
        msg.send()
    except:
        pass



