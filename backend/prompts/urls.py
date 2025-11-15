from django.urls import path
from .views import PromptCreateView

urlpatterns = [
    path("", PromptCreateView.as_view()),
]
