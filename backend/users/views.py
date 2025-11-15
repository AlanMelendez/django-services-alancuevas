from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "username and password are required"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "username already taken"}, status=400)

        user = User.objects.create(
            username=username,
            password=make_password(password)
        )

        return Response({"message": "user created successfully"}, status=status.HTTP_201_CREATED)
