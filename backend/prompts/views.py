from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from backend.prompts.embeddings import text_to_embedding

from .models import Prompt
from .serializers import PromptSerializer
from .throttles import BurstRateThrottle, SustainedRateThrottle

class PromptCreateView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def post(self, request):
        prompt_text = request.data.get("prompt")
        if not prompt_text:
            return Response({"error": "prompts is required"}, status=400)

        generated_response = f"Mockedai response to: {prompt_text}"
        embedding_vector = text_to_embedding(prompt_text).tolist() # it's to make it JSON serializable when you use the JSONField


        obj = Prompt.objects.create(
            user=request.user,
            prompt=prompt_text,
            response=generated_response,
            embedding=embedding_vector
        )

        return Response(PromptSerializer(obj).data, status=201)
