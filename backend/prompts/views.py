import faiss
import numpy as np

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .embeddings import text_to_embedding

from .models import Prompt
from .serializers import PromptSerializer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .throttles import BurstRateThrottle, SustainedRateThrottle


class PromptCreateView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def post(self, request):
        # get the data from the request
        the_prompt = request.data.get("text")
        use_ws = request.data.get("use_websocket", False)

        if not the_prompt:
            return Response({"error": "the text field is requird"}, status=status.HTTP_400_BAD_REQUEST)

        # here we simulate the AI response, to avoid spending tokens
        generated_response = f"Simulated response for: {the_prompt}"
        
        # we convert the text to an embedding vector
        embedding_vector = text_to_embedding(the_prompt).tolist() # it's to make it JSON serializable when you use the JSONField

        # create the object in the database
        new_prompt = Prompt.objects.create(
            user=request.user,
            prompt=the_prompt,
            response=generated_response,
            embedding=embedding_vector
        )

        # if requested via websocket, we send it that way
        if use_ws:
            # print("Using websocket!")
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "prompt_responses", # this is the group name
                {
                    "type": "prompt.response",
                    "response": PromptSerializer(new_prompt).data,
                },
            )
            # if ws is used, the http response is just an accepted
            return Response({"status": "the response will be sent via websocket"}, status=status.HTTP_202_ACCEPTED)

        # otherwise, return the created object as usual
        return Response(PromptSerializer(new_prompt).data, status=status.HTTP_201_CREATED)


class PromptSimilarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query_txt = request.query_params.get("prompt")

        if not query_txt:
            return Response({"error": "the prompt parameter is neccessary"}, status=400)

        # Embedding for the query
        query_vector = text_to_embedding(query_txt).astype("float32")

        # We get all the user's prompts
        user_prompts = Prompt.objects.filter(user=request.user)

        if not user_prompts.exists():
            return Response({"similars": []}, status=200)

        # We build the FAISS index, which is for searching similarities
        dimension = len(query_vector)
        the_index = faiss.IndexFlatL2(dimension)

        # Convert the prompt embeddings to an array
        embeddings_list = []
        prompt_items = []

        for p in user_prompts:
            if p.embedding:
                embeddings_list.append(np.array(p.embedding, dtype="float32"))
                prompt_items.append(p)

        if not embeddings_list:
            return Response({"similars": []}, status=200)

        embeddings_matrix = np.vstack(embeddings_list)
        the_index.add(embeddings_matrix)

        # Search for the top 5 most similar
        k = 5  
        distances, indices = the_index.search(np.array([query_vector]), k)

        similar_items = []
        for i in indices[0]:
            if i < len(prompt_items):
                similar_items.append(PromptSerializer(prompt_items[i]).data)

        return Response({"similars": similar_items}, status=200)
