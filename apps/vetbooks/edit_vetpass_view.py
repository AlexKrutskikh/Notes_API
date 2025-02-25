from django.core.exceptions import ValidationError
from django.utils.timezone import now
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.auth.authentication import CookieJWTAuthentication
from apps.auth.models import User

from .models import (
    AdditionalDescription,
    ClinicalExamination,
    Deworming,
    EctoparasiteTreatment,
    Identification,
    Registration,
    VaccinationAgainstRabies,
    VaccinationOthers,
    Vetbook,
    Vetpass,
)
from .validators import (
    validate_additional_description,
    validate_clinical_examination,
    validate_deworming,
    validate_ectoparasite_treatment,
    validate_identification,
    validate_registration,
    validate_vaccination,
)

""" Переиспользуемая функция для получения веткнижки и ветпаспорта """


def get_vetbook_and_vetpass(request, validated_data):
    """Retrieve the vetbook and vetpass, ensuring the user is authorized."""
    user_id = request.user.id

    try:
        user = User.objects.get(id=user_id)
        vetbook = Vetbook.objects.get(id=validated_data["vetbook_id"])
    except User.DoesNotExist:
        return None, None, Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Vetbook.DoesNotExist:
        return None, None, Response({"error": "Vetbook not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check if the user is the owner of the vetbook
    if user != vetbook.owner:
        return None, None, Response({"error": "Not authorized to edit the vetbook"}, status=status.HTTP_403_FORBIDDEN)

    try:
        vetpass = Vetpass.objects.get(vetbook=vetbook)
    except Vetpass.DoesNotExist:
        return None, None, Response({"error": "Vetpass not found for this vetbook"}, status=status.HTTP_404_NOT_FOUND)

    return vetbook, vetpass, None


""" Изменение дополнительного описания в ветпаспорте """


class EditAdditionalDescription(APIView):

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update additional description details of the vetbook.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "vetbook_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Vetbook ID"),
                "breed": openapi.Schema(type=openapi.TYPE_STRING, description="Breed of the animal"),
                "color": openapi.Schema(type=openapi.TYPE_STRING, description="Color of the animal"),
                "birth_date": openapi.Schema(
                    type=openapi.TYPE_STRING, format="date", description="Birth date (YYYY-MM-DD)"
                ),
                "special_marks": openapi.Schema(type=openapi.TYPE_STRING, description="Special marks"),
            },
        ),
        responses={
            200: openapi.Response({"message": "Additional information updated successfully"}),
            400: openapi.Response(
                description="Validation error or other issue",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(type=openapi.TYPE_STRING, description="Error message"),
                    },
                ),
            ),
        },
    )
    def patch(self, request):
        # Validate data
        data = request.data
        try:
            validated_data = validate_additional_description(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        vetbook, vetpass, error_response = get_vetbook_and_vetpass(request, validated_data)
        if error_response:
            return error_response
        try:
            # Get or create AdditionalDescription
            additional_info = AdditionalDescription.objects.get(vetpass=vetpass)

            # Update fields if present in the request
            for field in ["breed", "color", "birth_date", "special_marks"]:
                if field in validated_data:
                    setattr(additional_info, field, validated_data[field])

            additional_info.save()

            # Update vetbook's updated_at field
            vetbook.updated_at = now()
            vetbook.save()

            return Response(
                {"message": "Additional information updated successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


""" Изменение идентификации в ветпаспорте """


class EditIdentification(APIView):

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update identification details of the vetbook.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "vetbook_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Vetbook ID"),
                "chip_number": openapi.Schema(type=openapi.TYPE_STRING, description="Microchip number"),
                "clinic": openapi.Schema(type=openapi.TYPE_STRING, description="Clinic where chip was installed"),
                "chip_installation_location": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Location of chip installation"
                ),
                "date": openapi.Schema(
                    type=openapi.TYPE_STRING, format="date", description="Date of chip installation (YYYY-MM-DD)"
                ),
            },
        ),
        responses={
            200: openapi.Response({"message": "Identification information updated successfully"}),
            400: openapi.Response(
                description="Validation error or other issue",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(type=openapi.TYPE_STRING, description="Error message"),
                    },
                ),
            ),
        },
    )
    def patch(self, request):
        data = request.data
        try:
            validated_data = validate_identification(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        vetbook, vetpass, error_response = get_vetbook_and_vetpass(request, validated_data)
        if error_response:
            return error_response  # Return error if any issue is found
        try:
            # Get Identification
            identification = Identification.objects.get(vetpass=vetpass)

            # Update fields if present in the request
            for field in ["chip_number", "clinic", "chip_installation_location", "date"]:
                if field in validated_data:
                    setattr(identification, field, validated_data[field])

            identification.save()

            # Update vetbook's updated_at field
            vetbook.updated_at = now()
            vetbook.save()

            return Response({"message": "Identification information updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


""" Изменение вакцинаций в ветпаспорте """


class EditVaccination(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update vaccination details for the vetbook.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "vetbook_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Vetbook ID"),
                "type": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Type of vaccination (must be 'rabies' or 'other')",
                    enum=["rabies", "other"],  # Restrict values
                ),
                "vaccine": openapi.Schema(type=openapi.TYPE_STRING, description="Vaccine name"),
                "series": openapi.Schema(type=openapi.TYPE_STRING, description="Vaccine series"),
                "expiration_date": openapi.Schema(
                    type=openapi.TYPE_STRING, format="date", description="Expiration date"
                ),
                "vaccination_clinic": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Clinic where vaccination was administered"
                ),
                "date_of_vaccination": openapi.Schema(
                    type=openapi.TYPE_STRING, format="date", description="Date of vaccination"
                ),
                "vaccine_expiration_date": openapi.Schema(
                    type=openapi.TYPE_STRING, format="date", description="Vaccine expiration date"
                ),
            },
            required=["vetbook_id", "type", "vaccine"],  # Ensure required fields
        ),
        responses={
            200: openapi.Response({"message": "Vaccination information updated successfully"}),
            400: openapi.Response(
                description="Validation error or other issue",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(type=openapi.TYPE_STRING, description="Error message"),
                    },
                ),
            ),
        },
    )
    def patch(self, request):
        data = request.data
        try:
            validated_data = validate_vaccination(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        vetbook, vetpass, error_response = get_vetbook_and_vetpass(request, validated_data)
        if error_response:
            return error_response  # Return error if any issue is found

        try:
            # Get vaccination
            if data["type"] == "rabies":
                vaccination = VaccinationAgainstRabies.objects.get(vetpass=vetpass)
            else:
                vaccination = VaccinationOthers.objects.get(vetpass=vetpass)

            # Update fields if present in the request
            for field in [
                "vaccine",
                "series",
                "expiration_date",
                "vaccination_clinic",
                "date_of_vaccination",
                "vaccine_expiration_date",
            ]:
                if field in validated_data:
                    setattr(vaccination, field, validated_data[field])

            vaccination.save()

            # Update vetbook's updated_at field
            vetbook.updated_at = now()
            vetbook.save()

            return Response({"message": "Vaccination information updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


""" Изменение данных о дегельминтизации в ветпаспорте """


class EditDeworming(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update deworming details of the vetbook.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "vetbook_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Vetbook ID"),
                "drug": openapi.Schema(type=openapi.TYPE_STRING, description="Deworming drug name"),
                "date": openapi.Schema(
                    type=openapi.TYPE_STRING, format="date", description="Date of deworming (YYYY-MM-DD)"
                ),
                "clinic": openapi.Schema(type=openapi.TYPE_STRING, description="Clinic where deworming was performed"),
            },
        ),
        responses={
            200: openapi.Response({"message": "Deworming information updated successfully"}),
            400: openapi.Response(
                description="Validation error or other issue",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(type=openapi.TYPE_STRING, description="Error message"),
                    },
                ),
            ),
        },
    )
    def patch(self, request):
        data = request.data
        try:
            validated_data = validate_deworming(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        vetbook, vetpass, error_response = get_vetbook_and_vetpass(request, validated_data)
        if error_response:
            return error_response  # Return error if any issue is found
        try:
            # Get Deworming record
            deworming = Deworming.objects.get(vetpass=vetpass)

            # Update fields if present in the request
            for field in ["drug", "date", "clinic"]:
                if field in validated_data:
                    setattr(deworming, field, validated_data[field])

            deworming.save()

            # Update vetbook's updated_at field
            vetbook.updated_at = now()
            vetbook.save()

            return Response({"message": "Deworming information updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


""" Изменение данных об обработке от паразитов в ветпаспорте """


class EditEctoparasiteTreatment(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update ectoparasite treatment details of the vetbook.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "vetbook_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Vetbook ID"),
                "drug": openapi.Schema(type=openapi.TYPE_STRING, description="Ectoparasite treatment drug name"),
                "date": openapi.Schema(
                    type=openapi.TYPE_STRING, format="date", description="Date of treatment (YYYY-MM-DD)"
                ),
                "clinic": openapi.Schema(type=openapi.TYPE_STRING, description="Clinic where treatment was performed"),
            },
        ),
        responses={
            200: openapi.Response({"message": "Ectoparasite treatment information updated successfully"}),
            400: openapi.Response(
                description="Validation error or other issue",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(type=openapi.TYPE_STRING, description="Error message"),
                    },
                ),
            ),
        },
    )
    def patch(self, request):
        data = request.data
        try:
            validated_data = validate_ectoparasite_treatment(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        vetbook, vetpass, error_response = get_vetbook_and_vetpass(request, validated_data)
        if error_response:
            return error_response  # Return error if any issue is found
        try:
            # Get Ectoparasite Treatment record
            treatment = EctoparasiteTreatment.objects.get(vetpass=vetpass)

            # Update fields if present in the request
            for field in ["drug", "date", "clinic"]:
                if field in validated_data:
                    setattr(treatment, field, validated_data[field])

            treatment.save()

            # Update vetbook's updated_at field
            vetbook.updated_at = now()
            vetbook.save()

            return Response(
                {"message": "Ectoparasite treatment information updated successfully"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


""" Изменение данных о клиническом осмотре в ветпаспорте """


class EditClinicalExamination(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update clinical examination details of the vetbook.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "vetbook_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Vetbook ID"),
                "date": openapi.Schema(
                    type=openapi.TYPE_STRING, format="date", description="Date of examination (YYYY-MM-DD)"
                ),
                "result": openapi.Schema(type=openapi.TYPE_STRING, description="Examination result (max 20 chars)"),
                "files_ids": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING),
                    description="List of file IDs",
                ),
            },
        ),
        responses={
            200: openapi.Response({"message": "Clinical examination information updated successfully"}),
            400: openapi.Response(
                description="Validation error or other issue",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(type=openapi.TYPE_STRING, description="Error message"),
                    },
                ),
            ),
        },
    )
    def patch(self, request):
        data = request.data
        try:
            validated_data = validate_clinical_examination(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        vetbook, vetpass, error_response = get_vetbook_and_vetpass(request, validated_data)
        if error_response:
            return error_response  # Return error if any issue is found
        try:
            # Get Clinical Examination record
            examination = ClinicalExamination.objects.get(vetpass=vetpass)

            # Update fields if present in the request
            for field in ["date", "result", "files_ids"]:
                if field in validated_data:
                    setattr(examination, field, validated_data[field])

            examination.save()

            # Update vetbook's updated_at field
            vetbook.updated_at = now()
            vetbook.save()

            return Response(
                {"message": "Clinical examination information updated successfully"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


""" Изменение данных о регистрации в ветпаспорте """


class EditRegistration(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update registration details of the vetbook.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "vetbook_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Vetbook ID"),
                "clinic": openapi.Schema(type=openapi.TYPE_STRING, description="Clinic name (max 20 chars)"),
                "registration_number": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Registration number (max 35 chars)"
                ),
            },
        ),
        responses={
            200: openapi.Response({"message": "Registration information updated successfully"}),
            400: openapi.Response(
                description="Validation error or other issue",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(type=openapi.TYPE_STRING, description="Error message"),
                    },
                ),
            ),
        },
    )
    def patch(self, request):
        data = request.data
        try:
            validated_data = validate_registration(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        vetbook, vetpass, error_response = get_vetbook_and_vetpass(request, validated_data)
        if error_response:
            return error_response  # Return error if any issue is found
        try:
            # Get Registration record
            registration = Registration.objects.get(vetpass=vetpass)

            # Update fields if present in the request
            for field in ["clinic", "registration_number"]:
                if field in validated_data:
                    setattr(registration, field, validated_data[field])

            registration.save()

            # Update vetbook's updated_at field
            vetbook.updated_at = now()
            vetbook.save()

            return Response({"message": "Registration information updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
