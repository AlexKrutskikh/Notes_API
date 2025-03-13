from django.core.exceptions import ValidationError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.auth.authentication import CookieJWTAuthentication
from FreeVet.utils import save_files_to_storage

from ..models import Appointment, AppointmentFile, Treatment, Vetbook
from ..validators import validate_appointment_data, validate_treatment_data

"""Создание лечения в веткнижке"""


class CreateTreatment(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a new treatment in a vetbook.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "vetbook_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Vetbook ID"),
                "medication": openapi.Schema(type=openapi.TYPE_STRING, description="Medication name (max 20 chars)"),
                "dosage": openapi.Schema(type=openapi.TYPE_STRING, description="Dosage of medication (max 20 chars)"),
                "frequency": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Freaquency of medication (max 20 chars)"
                ),
                "start_date": openapi.Schema(
                    type=openapi.TYPE_STRING, format="date", description="Start date of treatment (YYYY-MM-DD)"
                ),
                "end_date": openapi.Schema(
                    type=openapi.TYPE_STRING, format="date", description="End date of treatment (YYYY-MM-DD)"
                ),
            },
        ),
        responses={
            201: openapi.Response(
                "Treatment created successfully",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING),
                        "treatment_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Created Treatment ID"),
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
        # Validate data
        try:
            validated_data = validate_treatment_data(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            vetbook = Vetbook.objects.get(id=validated_data["vetbook_id"])
            treatment = Treatment.objects.create(
                vetbook=vetbook,
                medication=validated_data.get("medication"),
                dosage=validated_data.get("dosage"),
                frequency=validated_data.get("frequency"),
                start_date=validated_data.get("start_date"),
                end_date=validated_data.get("end_date"),
            )
            return Response(
                {"message": "Treatment created successfully", "treatment_id": treatment.id},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


"""Изменение лечения в веткнижке"""


class EditTreatment(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update details of an existing treatment.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "treatment_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Treatment ID"),
                "medication": openapi.Schema(type=openapi.TYPE_STRING, description="Medication name (max 20 chars)"),
                "dosage": openapi.Schema(type=openapi.TYPE_STRING, description="Dosage of medication (max 20 chars)"),
                "frequency": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Frequency of medication (max 20 chars)"
                ),
                "start_date": openapi.Schema(
                    type=openapi.TYPE_STRING, format="date", description="Start date of treatment (YYYY-MM-DD)"
                ),
                "end_date": openapi.Schema(
                    type=openapi.TYPE_STRING, format="date", description="End date of treatment (YYYY-MM-DD)"
                ),
            },
        ),
        responses={
            200: openapi.Response({"message": "Treatment updated successfully"}),
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
            validated_data = validate_treatment_data(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            treatment = Treatment.objects.get(id=validated_data["treatment_id"])

            # Update fields if present in request
            for field in ["medication", "dosage", "frequency", "start_date", "end_date"]:
                if field in validated_data:
                    setattr(treatment, field, validated_data[field])

            treatment.save()

            return Response({"message": "Treatment updated successfully"}, status=status.HTTP_200_OK)
        except Treatment.DoesNotExist:
            return Response({"error": "Treatment not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


"""Создание посещения в клинике в веткнижке"""


class CreateAppointment(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a new appointment in a vetbook.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "vetbook_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Vetbook ID"),
                "clinic_name": openapi.Schema(type=openapi.TYPE_STRING, description="Clinic name (max 20 chars)"),
                "visit_date": openapi.Schema(
                    type=openapi.TYPE_STRING, format="date", description="Date of visit (YYYY-MM-DD)"
                ),
                "complaints": openapi.Schema(type=openapi.TYPE_STRING, description="Complaints (max 35 chars)"),
                "doctor_report": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Doctor's report (max 255 chars)", nullable=True
                ),
                "examination_files_ids": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING),
                    description="List of examination file IDs",
                    nullable=True,
                ),
                "other_files_ids": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING),
                    description="List of other file IDs",
                    nullable=True,
                ),
            },
            required=["vetbook_id", "clinic_name", "visit_date", "complaints"],
        ),
        responses={
            201: openapi.Response(
                "Appointment created successfully",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING),
                        "appointment_id": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="Created Appointment ID"
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
        # Validate data
        try:
            validated_data = validate_appointment_data(data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            vetbook = Vetbook.objects.get(id=validated_data["vetbook_id"])
            appointment = Appointment.objects.create(
                vetbook=vetbook,
                clinic_name=validated_data.get("clinic_name"),
                visit_date=validated_data.get("visit_date"),
                complaints=validated_data.get("complaints"),
                doctor_report=validated_data.get("doctor_report", ""),
                examination_files_ids=validated_data.get("examination_files_ids", []),
                other_files_ids=validated_data.get("other_files_ids", []),
            )

            return Response(
                {"message": "Appointment created successfully", "appointment_id": appointment.id},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AddFileToAppointment(APIView):

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "appointment_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Appointment ID"),
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

            file_paths = save_files_to_storage(request, "appointment_files")

        except ValidationError as e:

            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        appointment = Appointment.objects.get(id=request.data.get("appointment_id"))
        appointment_files = [AppointmentFile(path=path, user_id=user_id) for path in file_paths]

        AppointmentFile.objects.bulk_create(appointment_files)

        appointment_files_instances = AppointmentFile.objects.filter(path__in=file_paths)

        appointment.appointment_related_files.set(appointment_files_instances)

        created_ids = list(
            AppointmentFile.objects.filter(user_id=user_id)
            .order_by("-id")[: len(file_paths)]
            .values_list("id", flat=True)
        )

        return Response({"message": "Successfully created", "file(s) ids": created_ids}, status=201)


"""Изменение посещения в клинике в веткнижке"""


class EditAppointment(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update details of an existing appointment.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "appointment_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Appointment ID"),
                "clinic_name": openapi.Schema(type=openapi.TYPE_STRING, description="Clinic name (max 20 chars)"),
                "visit_date": openapi.Schema(
                    type=openapi.TYPE_STRING, format="date", description="Visit date (YYYY-MM-DD)"
                ),
                "complaints": openapi.Schema(type=openapi.TYPE_STRING, description="Complaints (max 35 chars)"),
                "doctor_report": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Doctor's report (max 255 chars)"
                ),
                "examination_files_ids": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING),
                    description="List of examination file IDs",
                ),
                "other_files_ids": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING),
                    description="List of other file IDs",
                ),
            },
        ),
        responses={
            200: openapi.Response({"message": "Appointment updated successfully"}),
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
            validated_data = validate_appointment_data(data)  # Reuse validation function
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            appointment = Appointment.objects.get(id=validated_data["appointment_id"])

            # Update fields if present in request
            for field in [
                "clinic_name",
                "visit_date",
                "complaints",
                "doctor_report",
                "examination_files_ids",
                "other_files_ids",
            ]:
                if field in validated_data:
                    setattr(appointment, field, validated_data[field])

            appointment.save()

            return Response({"message": "Appointment updated successfully"}, status=status.HTTP_200_OK)
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
