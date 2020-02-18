from django.apps import AppConfig


class BoutiqueConfig(AppConfig):
    name = 'boutique'

    def ready(self):
        import boutique.signals # noqa
