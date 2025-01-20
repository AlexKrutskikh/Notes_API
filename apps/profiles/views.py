from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from apps.auth.models import User
from FreeVet.utils import save_files_to_storage

from .models import Perks, Profile
from .validators import validate_perk, validate_user_data

"""Сохранение в БД данных профиля"""


class ChangeAvatareProfile(APIView):

    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user_id = request.user.id

        try:

            avatar_file = save_files_to_storage(request, "profile_avatar")

        except ValidationError as e:

            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        existing_profile = Profile.objects.get(user_id=user_id)

        if existing_profile:

            existing_profile.path_photo = avatar_file
            existing_profile.save()

        else:

            return Response(
                {
                    "error": "ProfileNotFound",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"message": "Profile updated photo"}, status=201)


class EditProfile(APIView):

    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user_id = request.user.id
        data = request.data

        try:
            validate_data = validate_user_data(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        existing_profile = Profile.objects.get(user_id=user_id)

        if existing_profile:

            name = validate_data.get("name", "")
            if name:
                existing_profile.name = name

            phone = validate_data.get("phone", "")
            if phone:
                existing_profile.phone = phone

            email = validate_data.get("email", "")
            if email:
                existing_profile.email = email

            telegram = validate_data.get("telegram", "")
            if telegram:
                existing_profile.telegram = telegram

            existing_profile.updated_at = timezone.now()
            existing_profile.save()

            user = User.objects.get(id=user_id)
            if user.status == "Profile_prefill":
                user.status = "Status_select"
                user.save()

        else:

            return Response(
                {
                    "error": "ProfileNotFound",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"message": "Profile updated successfully"}, status=201)


class UpdatePerks(APIView):

    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user_id = request.user.id
        data = request.data

        # user = User.objects.get(id=user_id)
        # if user.status!="Status_select":
        #     return Response({"error":"Perks selected"} , status=status.HTTP_400_BAD_REQUEST)

        try:
            valid_perk, role = validate_perk(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        existing_profile = Profile.objects.get(user_id=user_id)

        perks_to_add = Perks.objects.filter(name__in=valid_perk)

        existing_profile.perks.add(*perks_to_add)

        user = User.objects.get(id=user_id)
        user.status = "Vetbook_creation"
        user.type = role
        user.save()

        return Response({"message": "Perks updated successfully"}, status=status.HTTP_200_OK)
