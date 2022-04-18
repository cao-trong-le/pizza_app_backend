from django.apps import AppConfig


class PizzaorderingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pizzaordering'

    def ready(self):
        import pizzaordering.signals
