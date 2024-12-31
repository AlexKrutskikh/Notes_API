from django.core.management import call_command
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def load_fixtures(sender, **kwargs):
    """
    Автоматически загружает фикстуры после выполнения миграций.
    """
    if sender.name == "apps.profiles":
        print("Загружаются фикстуры для приложения profiles...")
        call_command("loaddata", "perks_fixture.json")
