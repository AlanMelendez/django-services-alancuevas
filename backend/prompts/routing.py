from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/prompt_responses/$', consumers.PromptConsumer.as_asgi()),
]
