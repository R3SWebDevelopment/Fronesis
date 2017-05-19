import os
import djcelery


from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fronesis.settings")

application = get_wsgi_application()
application = DjangoWhiteNoise(application)

djcelery.setup_loader()
