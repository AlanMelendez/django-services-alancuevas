from django.urls import path
from .views import PromptCreateView, PromptSimilarView

urlpatterns = [
    path("", PromptCreateView.as_view()),
    path("similar/", PromptSimilarView.as_view(), name="similar_prompt"),
]
