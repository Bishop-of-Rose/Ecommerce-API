from redis import from_url

from .config import settings

client = from_url(
    settings.REDIS_URL,
    encoding = 'utf-8',
    decode_responses = True
)