from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from Notes.settings import logger

from .models import User
from .utils import generate_token_and_set_cookie
from .validators import validate_user_data

"""Регистрация пользователя"""


class RegistrationUser(APIView):
    def post(self, request):
        data = request.data

        try:
            validate_data = validate_user_data(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        errors = {}

        if User.objects.filter(last_name=validate_data.get("last_name")).exists():
            errors["last_name"] = "This last name is already in use"

        if User.objects.filter(first_name=validate_data.get("first_name")).exists():
            errors["first_name"] = "This first name is already in use"

        if User.objects.filter(username=validate_data.get("username")).exists():
            errors["username"] = "This username is already in use"

        if User.objects.filter(phone=validate_data.get("phone")).exists():
            errors["phone"] = "This phone number is already registered"

        if User.objects.filter(email=validate_data.get("email")).exists():
            errors["email"] = "This email is already in use"

        if errors:
            logger.warning(f"Registration errors for user data: {errors}")
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User(
                last_name=validate_data.get("last_name", ""),
                first_name=validate_data.get("first_name", ""),
                username=validate_data.get("username", ""),
                phone=validate_data.get("phone", ""),
                email=validate_data.get("email", ""),
            )
            user.set_password(validate_data.get("password", ""))
            user.save()

            logger.info(f"User {user.username} successfully registered")

            return Response({"message": "Successfully created"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


"""Вход пользователя"""


class AuthorizationUser(APIView):

    def post(self, request):

        password = request.data.get("password", "")
        user_name = request.data.get("username", "")

        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            logger.warning(f"Failed login attempt: User {user_name} does not exist")
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            logger.warning(f"Failed login attempt: Incorrect password for user {user_name}")
            return Response({"error": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)

        user.last_login = timezone.now()
        user.save()

        response = generate_token_and_set_cookie(user)
        response.data = {"message": "Successfully logged in"}

        logger.info(f"User {user.username} successfully logged in")

        return response
