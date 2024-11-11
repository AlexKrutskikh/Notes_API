from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Profile
from .serializers import RegisterSerializer, LoginSerializer, SMSVerificationSerializer, ProfileSerializer, \
    UpdateVerifyCodeSerializer, ProfileViewSerializer
from .utils import send_sms
from django.utils import timezone
from datetime import timedelta
from rest_framework.generics import CreateAPIView
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from twilio.base.exceptions import TwilioRestException
from django.shortcuts import render

"""Render HTML"""


def updatecode_view(request):
    return render(request, 'updatecode.html')



"""The update of boolean fields"""

class UpdateProfileFieldsView(APIView):
    def post(self, request, *args, **kwargs):
        # Получаем user_id из запроса
        user_id = request.data.get('user_id')
        if user_id is None:
            return Response(
                {"detail": "Не заполнен параметр user_id."},
                status=status.HTTP_400_BAD_REQUEST)

        # Ищем профиль с указанным user_id
        profile = get_object_or_404(Profile, user_id=user_id)

        # Десериализуем и проверяем данные
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            # Устанавливаем is_active в True
            serializer.validated_data['is_active'] = True
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""Redirect after registration and authorization"""
def custom_login_redirect(request):
    redirect_url = request.session.get('redirect_url', '/default-url')
    return redirect(redirect_url)


"""Redirect for creating an API for authorization"""

def google_oauth_redirect(request):
    redirect_url = f"{settings.BASE_URL}/api/users/social-auth/login/google-oauth2/"
    return HttpResponseRedirect(redirect_url)

def facebook_oauth_redirect(request):
    redirect_url = f"{settings.BASE_URL}/api/users/social-auth/login/facebook/"
    return HttpResponseRedirect(redirect_url)




"""Authorization via Twilio"""

class RegisterView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        # Получаем данные из формы
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        photo = request.FILES.get('photo', None)

        # Проверка, переданы ли необходимые данные
        if not name or not phone:
            return Response(
                {"detail": "Необходимо указать имя и номер телефона."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Проверка, существует ли пользователь с данным номером телефона
        if Profile.objects.filter(phone=phone).exists():
            return Response(
                {"detail": "Пользователь уже зарегистрирован. Перейдите в окно входа."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Создаем новый профиль
        profile = Profile.objects.create(
            name=name,
            phone=phone,
            photo=photo  # Устанавливаем фото, если оно передано
        )
        
        # Генерируем и отправляем SMS-код
        profile.generate_sms_code()
        
        try:
            send_sms(profile.phone, f"Ваш код: {profile.sms_code}")
        except TwilioRestException:
            # Удаляем профиль, если SMS не может быть отправлено
            profile.delete()
            return Response(
                {"detail": "С текущими номерами отправителя и получателя SMS не может быть отправлено."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Возвращаем ответ об успешной регистрации
        return Response(
            {"detail": "Регистрация прошла успешно."},
            status=status.HTTP_201_CREATED
        )


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']

        try:
            profile = Profile.objects.get(phone=phone_number)
            profile.generate_sms_code()
            send_sms(phone_number, f"Your code is {profile.sms_code}")

            # Создайте токен и верните его
            token, created = Token.objects.get_or_create(user=profile.user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)  # Возвратите токен

        except Profile.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class VerifyCodeView(generics.GenericAPIView):
    serializer_class = SMSVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        code = serializer.validated_data['code']

        try:
            profile = Profile.objects.get(phone=phone_number, sms_code=code)

            # Проверка срока действия кода
            if profile.code_sent_time < timezone.now() - timedelta(seconds=90):
                return Response({"error": "Code expired"}, status=status.HTTP_400_BAD_REQUEST)

            profile.last_login_time = timezone.now()
            
            # Если у профиля нет пользователя, создаём его
            if profile.user is None:
                user = User.objects.create(username=profile.phone)
                profile.user = user
                profile.save()

            # Генерация токенов
            refresh = RefreshToken.for_user(profile.user)

            # Добавление URL для редиректа
            if not profile.user.date_joined:
                request.session['redirect_url'] = f'https://freevet.me/verification/role?user_id={profile.user.id}'
            else:
                request.session['redirect_url'] = f'https://freevet.me/main?user_id={profile.user.id}'
            
            redirect_url = request.session['redirect_url']

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "redirect_url": redirect_url,
                "message": "Logged in"
            }, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response({"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)


"""Update verify code for veterinarian"""


class UpdateVerifyCodeView(APIView):
    def post(self, request):
        # Получаем данные из запроса
        phone = request.data.get('phone')
        email = request.data.get('email')
        verify_code = request.data.get('verify_code')

        # Проверка наличия телефона или почты
        if not phone and not email:
            return Response({"error": "Either phone or email must be provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Ищем профиль по телефону или email
        profile = Profile.objects.filter(phone=phone).first() or Profile.objects.filter(email=email).first()

        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        # Обновляем только поле verify_code
        profile.verify_code = verify_code
        profile.save()

        return Response({"message": "Verify code updated successfully."}, status=status.HTTP_200_OK)



class VerifyCodeVetView(APIView):
    def post(self, request):
        # Получаем данные из запроса
        phone = request.data.get('phone')
        email = request.data.get('email')
        input_code = request.data.get('verify_code')

        # Проверка наличия телефона или email и кода
        if not (phone or email) or not input_code:
            return Response({"error": "Phone or email and verify code are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Ищем профиль по телефону или email
        profile = Profile.objects.filter(phone=phone).first() or Profile.objects.filter(email=email).first()

        # Проверка, что профиль найден
        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

         # Проверка срока действия кода
        if profile.code_sent_time < timezone.now() - timedelta(days=5):
            return Response({"error": "Code expired"}, status=status.HTTP_400_BAD_REQUEST)

        # Сравнение введенного кода с сохраненным в базе данных
        if profile.verify_code == input_code:
            return Response({"message": "Verify code is correct."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid verify code."}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    def get(self, request, pk):
        profile = Profile.objects.get(user_id=pk)
        serializer = ProfileViewSerializer(profile, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)
