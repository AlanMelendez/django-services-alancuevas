from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

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

        obj = Prompt.objects.create(
            user=request.user,
            prompt=prompt_text,
            response=generated_response
        )

        return Response(PromptSerializer(obj).data, status=201)
