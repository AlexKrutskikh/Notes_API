from django.contrib.auth import get_user_model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .authentication import CookieJWTAuthentication

User = get_user_model()


class GetStatusUser(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve the authenticated user's status and type.",
        responses={
            200: openapi.Response(
                "User status retrieved successfully",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "user_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Authenticated user's ID"),
                        "status": openapi.Schema(type=openapi.TYPE_STRING, description="Current status of the user"),
                        "user_type": openapi.Schema(type=openapi.TYPE_STRING, description="Type of the user"),
                    },
                ),
            ),
            400: openapi.Response("Bad Request"),
            401: openapi.Response("Unauthorized - Authentication required"),
        },
    )
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        return Response({"user_id": user_id, "status": user.status, "user_type": user.type}, status=200)
