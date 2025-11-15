import faiss
import numpy as np

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .embeddings import text_to_embedding

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
class PromptSimilarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query_text = request.query_params.get("prompt")

        if not query_text:
            return Response({"error": "prompt is required"}, status=400)

        # Embedding for query
        query_vec = text_to_embedding(query_text).astype("float32")

        # Get all stored prompts for this user
        prompts = Prompt.objects.filter(user=request.user)

        if not prompts.exists():
            return Response({"similar": []}, status=200)

        # Build FAISS index
        dim = len(query_vec)
        index = faiss.IndexFlatL2(dim)

        # Convert prompt embeddings to array
        embeddings = []
        items = []

        for p in prompts:
            if p.embedding:
                embeddings.append(np.array(p.embedding, dtype="float32"))
                items.append(p)

        if not embeddings:
            return Response({"similar": []}, status=200)

        matrix = np.vstack(embeddings)
        index.add(matrix)

        # Search top 5
        k = 5  
        distances, indices = index.search(np.array([query_vec]), k)

        similar_items = []
        for idx in indices[0]:
            if idx < len(items):
                similar_items.append(PromptSerializer(items[idx]).data)

        return Response({"similar": similar_items}, status=200)
