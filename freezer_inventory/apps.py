from django.apps import AppConfig


class FreezerInventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'freezer_inventory'

    def ready(self):
        import freezer_inventory.signals
