from redis import from_url

from .config import settings

client = from_url(settings.REDIS_URL)