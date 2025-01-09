from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from .models import User


class GetStatusUser(APIView):

    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        user_id = request.user.id

        user = User.objects.get(id=user_id)

        return Response({"user_id": user_id, "status": user.status, "user_type": user.type}, status=201)
