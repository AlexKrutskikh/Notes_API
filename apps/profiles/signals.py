import logging

from django.core.management import call_command
from django.db.models.signals import post_migrate
from django.dispatch import receiver

logger = logging.getLogger(__name__)  # Настраиваем логгер


@receiver(post_migrate)
def load_fixtures(sender, **kwargs):
    """
    Автоматически загружает фикстуры после выполнения миграций.
    """
    if sender.name == "apps.profiles":
        logger.info("Загружаются фикстуры для приложения profiles...")
        try:
            call_command("loaddata", "perks_fixture.json")
            logger.info("Фикстуры успешно загружены.")
        except Exception as e:
            logger.error(f"Ошибка при загрузке фикстур: {e}")
