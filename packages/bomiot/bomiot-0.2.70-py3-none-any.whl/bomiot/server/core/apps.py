from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'bomiot.server.core'

    def ready(self):
        from .watchfile import run
        run()
