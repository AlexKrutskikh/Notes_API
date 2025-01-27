from rest_framework import serializers

from .models import (
    Appointment,
    ClinicalExamination,
    Identification,
    Procedure,
    Registration,
    Treatment,
    Vaccination,
    Vetbook,
)

class IdentificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Identification
        fields = [
            "id",
            "chip_number",
            "clinic_name",
            "chip_installation_location",
            "chip_installation_date",
        ]


class VaccinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccination
        fields = [
            "id",
            "type",
            "vaccine_name",
            "batch_number",
            "expiration_date",
            "clinic_name",
            "administration_date",
            "validity_date",
        ]


class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = [
            "id",
            "medication",
            "processing_date",
            "clinic_name",
        ]


class ClinicalExaminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalExamination
        fields = [
            "id",
            "examination_date",
            "results",
            "files_ids",
        ]


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = [
            "id",
            "clinic_name",
            "registration_number",
        ]


class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = ["id", "medication", "dosage", "frequency", "start_date", "end_date", "calendar"]


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            "id",
            "clinic_name",
            "visit_date",
            "complaints",
            "doctor_report",
            "examination_files_ids",
            "other_files_ids",
        ]


class VetbookSerializer(serializers.ModelSerializer):
    vetbook_identifications = IdentificationSerializer(many=True, read_only=True)  # Related identifications
    vetbook_vaccinations = VaccinationSerializer(many=True, read_only=True)  # Related vaccinations
    vetbook_procedures = ProcedureSerializer(many=True, read_only=True)  # Related procedures
    vetbook_examinations = ClinicalExaminationSerializer(many=True, read_only=True)  # Related examinations
    vetbook_registration = RegistrationSerializer(read_only=True)  # Related registration
    vetbook_treatments = TreatmentSerializer(many=True, read_only=True)  # Related treatments
    vetbook_appointments = AppointmentSerializer(many=True, read_only=True)  # Related appointments

    class Meta:
        model = Vetbook
        fields = [
            "id",
            "owner",
            "name",
            "species",
            "weight",
            "gender",
            "is_homeless",
            "vetbook_identifications",
            "vetbook_vaccinations",
            "vetbook_procedures",
            "vetbook_examinations",
            "vetbook_registration",
            "vetbook_treatments",
            "vetbook_appointments",
        ]
