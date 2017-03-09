from django.apps import AppConfig


class PhiliosConfig(AppConfig):
    name = 'philios'
    verbose_name = 'Philios'

    def ready(self):
        pass
