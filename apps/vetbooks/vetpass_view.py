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
from apps.vetbooks.models import (
    AdditionalDescription,
    ClinicalExamination,
    ClinicalExaminationFile,
    Deworming,
    EctoparasiteTreatment,
    Identification,
    Registration,
    VaccinationAgainstRabies,
    VaccinationOthers,
    Vetbook,
)
from apps.vetbooks.validators import (
    validate_additional_description,
    validate_clinical_examination,
    validate_deworming,
    validate_ectoparasite_treatment,
    validate_identification,
    validate_registration,
    validate_vaccination,
)
from FreeVet.utils import save_files_to_storage

""" Переиспользуемая функция для получения веткнижки и ветпаспорта """


def get_vetbook_and_error(request, validated_data):
    """Retrieve the vetbook and vetpass, ensuring the user is authorized."""
    user_id = request.user.id

    try:
        user = User.objects.get(id=user_id)
        vetbook = Vetbook.objects.get(id=validated_data["vetbook_id"])
    except User.DoesNotExist:
        return None, Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Vetbook.DoesNotExist:
        return None, Response({"error": "Vetbook not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check if the user is the owner of the vetbook
    if user != vetbook.owner:
        return None, Response({"error": "Not authorized to edit the vetbook"}, status=status.HTTP_403_FORBIDDEN)

    return vetbook, None


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
                "additional_information_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="Additional information ID"
                ),
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

        vetbook, error_response = get_vetbook_and_error(request, validated_data)
        if error_response:
            return error_response
        try:
            # Get AdditionalDescription
            additional_info = AdditionalDescription.objects.get(id=validated_data["additional_description_id"])

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


""" Добавление идентификации в ветпаспорте """


class CreateIdentification(APIView):

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add identification details of the vetbook.",
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
            required=["vetbook_id", "chip_number", "date"],
        ),
        responses={
            201: openapi.Response(
                description="Identification created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING, description="Success message"),
                        "identification_id": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="ID of the created identification"
                        ),
                    },
                ),
            ),
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
    def post(self, request):
        data = request.data
        try:
            validated_data = validate_identification(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        vetbook, error_response = get_vetbook_and_error(request, validated_data)
        if error_response:
            return error_response

        vetpass = vetbook.vetbooks_vetpass.first()
        try:
            # Create Identification
            identification = Identification.objects.create(
                vetpass=vetpass,
                chip_number=validated_data.get("chip_number"),
                clinic=validated_data.get("clinic"),
                chip_installation_location=validated_data.get("chip_installation_location"),
                date=validated_data.get("date"),
            )

            # Update vetbook's updated_at field
            vetbook.updated_at = now()
            vetbook.save()

            return Response(
                {"message": "Identification information updated successfully", "identification_id": identification.id},
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
                "identification_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Identification ID"),
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

        vetbook, error_response = get_vetbook_and_error(request, validated_data)
        if error_response:
            return error_response
        try:
            # Get Identification
            identification = Identification.objects.get(id=validated_data["identification_id"])

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


""" Добавление вакцинации в ветпаспорте """


class CreateVaccination(APIView):

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add vaccination details to the vetbook.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "vetbook_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Vetbook ID"),
                "type": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Type of vaccination (must be 'rabies' or 'other')",
                    enum=["rabies", "other"],
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
            required=["vetbook_id", "type", "vaccine", "date_of_vaccination"],
        ),
        responses={
            201: openapi.Response(
                description="Vaccination created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING, description="Success message"),
                        "vaccination_id": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="Created vaccination ID"
                        ),
                    },
                ),
            ),
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
    def post(self, request):
        data = request.data
        try:
            validated_data = validate_vaccination(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        vetbook, error_response = get_vetbook_and_error(request, validated_data)
        if error_response:
            return error_response
        vetpass = vetbook.vetbooks_vetpass.first()
        try:
            # Get vaccination
            if data["type"] == "rabies":
                vaccination = VaccinationAgainstRabies.objects.create(
                    vetpass=vetpass,
                    vaccine=validated_data.get("vaccine"),
                    series=validated_data.get("series"),
                    expiration_date=validated_data.get("expiration_date"),
                    vaccination_clinic=validated_data.get("vaccination_clinic"),
                    date_of_vaccination=validated_data.get("date_of_vaccination"),
                    vaccine_expiration_date=validated_data.get("vaccine_expiration_date"),
                )
            else:
                vaccination = VaccinationOthers.objects.create(
                    vetpass=vetpass,
                    vaccine=validated_data.get("vaccine"),
                    series=validated_data.get("series"),
                    expiration_date=validated_data.get("expiration_date"),
                    vaccination_clinic=validated_data.get("vaccination_clinic"),
                    date_of_vaccination=validated_data.get("date_of_vaccination"),
                    vaccine_expiration_date=validated_data.get("vaccine_expiration_date"),
                )

            # Update vetbook's updated_at field
            vetbook.updated_at = now()
            vetbook.save()

            return Response(
                {"message": "Vaccination information created successfully", "vaccination_id": vaccination.id},
                status=status.HTTP_200_OK,
            )
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
                "vaccination_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Vaccination ID"),
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

        vetbook, error_response = get_vetbook_and_error(request, validated_data)
        if error_response:
            return error_response

        try:
            # Get vaccination
            if data["type"] == "rabies":
                vaccination = VaccinationAgainstRabies.objects.get(id=validated_data["vaccination_id"])
            else:
                vaccination = VaccinationOthers.objects.get(id=validated_data["vaccination_id"])

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

            return Response({"message": "Vaccination information created successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


""" Добавление дегельминтизации в ветпаспорте """


class CreateDeworming(APIView):

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add deworming details to the vetbook.",
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
            required=["vetbook_id", "drug", "date"],
        ),
        responses={
            201: openapi.Response(
                description="Deworming created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING, description="Success message"),
                        "deworming_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Created deworming ID"),
                    },
                ),
            ),
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
    def post(self, request):
        data = request.data
        try:
            validated_data = validate_deworming(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        vetbook, error_response = get_vetbook_and_error(request, validated_data)
        if error_response:
            return error_response  # Return error if any issue is found
        vetpass = vetbook.vetbooks_vetpass.first()
        try:
            deworming = Deworming.objects.create(
                vetpass=vetpass,
                drug=validated_data.get("drug"),
                date=validated_data.get("date"),
                clinic=validated_data.get("clinic"),
            )

            # Update vetbook's updated_at field
            vetbook.updated_at = now()
            vetbook.save()

            return Response(
                {"message": "Deworming information created successfully", "deworming_id": deworming.id},
                status=status.HTTP_200_OK,
            )
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
                "deworming_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Deworming ID"),
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

        vetbook, error_response = get_vetbook_and_error(request, validated_data)
        if error_response:
            return error_response  # Return error if any issue is found
        try:
            # Get Deworming record
            deworming = Deworming.objects.get(id=validated_data["deworming_id"])

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


""" Добавление обработки от паразитов в ветпаспорте """


class CreateEctoparasiteTreatment(APIView):

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add ectoparasite treatment details to the vetbook.",
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
            required=["vetbook_id", "drug", "date"],
        ),
        responses={
            201: openapi.Response(
                description="Ectoparasite treatment created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING, description="Success message"),
                        "ectoparasite_treatment_id": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="Created treatment ID"
                        ),
                    },
                ),
            ),
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
    def post(self, request):
        data = request.data
        try:
            validated_data = validate_ectoparasite_treatment(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        vetbook, error_response = get_vetbook_and_error(request, validated_data)
        if error_response:
            return error_response  # Return error if any issue is found
        vetpass = vetbook.vetbooks_vetpass.first()
        try:
            # Get Ectoparasite Treatment record
            treatment = EctoparasiteTreatment.objects.create(
                vetpass=vetpass,
                drug=validated_data.get("drug"),
                date=validated_data.get("date"),
                clinic=validated_data.get("clinic"),
            )

            # Update vetbook's updated_at field
            vetbook.updated_at = now()
            vetbook.save()

            return Response(
                {
                    "message": "Ectoparasite treatment information created successfully",
                    "ectoparasite_treatment_id": treatment.id,
                },
                status=status.HTTP_200_OK,
            )
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
                "ectoparasite_treatment_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="Ectoparasite treatment ID"
                ),
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

        vetbook, error_response = get_vetbook_and_error(request, validated_data)
        if error_response:
            return error_response  # Return error if any issue is found
        try:
            # Get Ectoparasite Treatment record
            treatment = EctoparasiteTreatment.objects.get(id=validated_data["ectoparasite_treatment_id"])

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


""" Добавление клинического осмотра в ветпаспорте """


class CreateClinicalExamination(APIView):

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add clinical examination details to the vetbook.",
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
            required=["vetbook_id", "date", "result"],
        ),
        responses={
            201: openapi.Response(
                description="Clinical examination created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING, description="Success message"),
                        "clinical_examination_id": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="Created examination ID"
                        ),
                    },
                ),
            ),
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
    def post(self, request):
        data = request.data
        try:
            validated_data = validate_clinical_examination(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        vetbook, error_response = get_vetbook_and_error(request, validated_data)
        if error_response:
            return error_response  # Return error if any issue is found
        vetpass = vetbook.vetbooks_vetpass.first()
        try:
            examination = ClinicalExamination.objects.create(
                vetpass=vetpass,
                date=validated_data.get("date"),
                result=validated_data.get("result"),
                files_ids=validated_data.get("files_ids"),
            )

            # Update vetbook's updated_at field
            vetbook.updated_at = now()
            vetbook.save()

            return Response(
                {
                    "message": "Clinical examination information created successfully",
                    "clinical_examination_id": examination.id,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


"""Сохранение в БД файлов для клинического осмотра"""


class AddFileToClinicalExamination(APIView):

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "clinical_examination_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="Clinical examination ID"
                ),
                "files": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING, format="binary"),
                    description="List of files to upload",
                ),
            },
        ),
        responses={
            201: openapi.Response(
                "Successfully created",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING),
                        "file(s) ids": openapi.Schema(
                            type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER)
                        ),
                    },
                ),
            ),
            400: "Bad request - Validation error",
        },
    )
    def post(self, request):
        user_id = request.user.id

        try:

            file_paths = save_files_to_storage(request, "clinical_examination_files")

        except ValidationError as e:

            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        examination = ClinicalExamination.objects.get(id=request.data.get("clinical_examination_id"))
        clinical_examination_files = [ClinicalExaminationFile(path=path, user_id=user_id) for path in file_paths]

        ClinicalExaminationFile.objects.bulk_create(clinical_examination_files)

        clinical_examination_files_instances = ClinicalExaminationFile.objects.filter(path__in=file_paths)

        examination.examination_files.set(clinical_examination_files_instances)

        created_ids = list(
            ClinicalExaminationFile.objects.filter(user_id=user_id)
            .order_by("-id")[: len(file_paths)]
            .values_list("id", flat=True)
        )

        return Response({"message": "Successfully created", "file(s) ids": created_ids}, status=201)


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
                "clinical_examination_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="Clinical examination ID"
                ),
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

        vetbook, error_response = get_vetbook_and_error(request, validated_data)
        if error_response:
            return error_response  # Return error if any issue is found
        try:
            # Get Clinical Examination record
            examination = ClinicalExamination.objects.get(id=validated_data["clinical_examination_id"])

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


""" Добавление регистрации в ветпаспорте """


class CreateRegistration(APIView):

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add registration details to the vetbook.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "vetbook_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Vetbook ID"),
                "clinic": openapi.Schema(type=openapi.TYPE_STRING, description="Clinic name (max 20 chars)"),
                "registration_number": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Registration number (max 35 chars)"
                ),
            },
            required=["vetbook_id", "clinic", "registration_number"],
        ),
        responses={
            201: openapi.Response(
                description="Registration created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING, description="Success message"),
                        "registration_id": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="Created registration ID"
                        ),
                    },
                ),
            ),
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
    def post(self, request):
        data = request.data
        try:
            validated_data = validate_registration(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        vetbook, error_response = get_vetbook_and_error(request, validated_data)
        if error_response:
            return error_response  # Return error if any issue is found
        vetpass = vetbook.vetbooks_vetpass.first()
        try:
            registration = Registration.objects.create(
                vetpass=vetpass,
                clinic=validated_data.get("clinic"),
                registration_number=validated_data.get("registration_number"),
            )

            # Update vetbook's updated_at field
            vetbook.updated_at = now()
            vetbook.save()

            return Response(
                {"message": "Registration information created successfully", "registration_id": registration.id},
                status=status.HTTP_200_OK,
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
                "registration_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Registration ID"),
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

        vetbook, error_response = get_vetbook_and_error(request, validated_data)
        if error_response:
            return error_response  # Return error if any issue is found
        try:
            # Get Registration record
            registration = Registration.objects.get(id=validated_data["registration_id"])

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
