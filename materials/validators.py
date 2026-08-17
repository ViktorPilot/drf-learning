import re

from rest_framework import serializers


def check_not_youtube(value):
    """Метод проверяет наличие ссылки на youtube"""
    youtube = "https://youtube.com/"
    if not re.match(youtube, value, flags=0):
        raise serializers.ValidationError("Ссылка поддерживается только на youtube.com")
