import json
from datetime import timedelta

from Notes.settings import blacklist_db, whitelist_db


def add_token_to_blacklist(token, exp):
    """Добавляет токен в черный список (например, при logout или подозрительной активности)"""
    blacklist_db.setex(token, timedelta(seconds=exp), "blacklisted")


def is_token_blacklisted(token):
    """Проверяет, заблокирован ли токен"""
    return blacklist_db.exists(token)


def add_token_to_whitelist(token, user_id, exp, ip, user_agent):
    """Добавляет токен в белый список с привязкой к IP и User-Agent"""
    data = json.dumps({"user_id": user_id, "ip": ip, "ua": user_agent})
    whitelist_db.setex(token, timedelta(days=exp), data)


def is_token_whitelisted(token):
    """Проверяет, есть ли токен в белом списке"""
    return whitelist_db.exists(token)


def get_whitelist_data(token):
    """Получает данные (IP, User-Agent) по токену"""
    data = whitelist_db.get(token)
    return json.loads(data) if data else None


def remove_token_from_whitelist(token):
    """Удаляет токен из белого списка"""
    whitelist_db.delete(token)
