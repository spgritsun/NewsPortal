# import redis
from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        import main.signals


# red = redis.Redis(
#     host='redis-17910.c304.europe-west1-2.gce.redns.redis-cloud.com',
#     port='17910',
#     password='KV85sYlBu86ZO1bPVZDlAAsCNUvMe0Op'
# )
