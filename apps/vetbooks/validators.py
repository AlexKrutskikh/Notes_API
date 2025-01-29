import re
from datetime import date

from rest_framework.exceptions import ValidationError

"""Валидация данных животного"""


def validate_create_data(data):

    if re.search(r"\d", data.get("name", "")):
        raise ValidationError("InvalidName")

    if re.search(r"\d", data.get("species", "")):
        raise ValidationError("InvalidSpecies")

    gender = data.get("gender")
    if gender not in ["male", "female"]:
        raise ValidationError("InvalidGender")

    weight_str = data.get("weight", "")
    try:
        weight = float(weight_str)
        if weight <= 0:
            raise ValidationError("InvalidWeight")
    except ValueError:
        raise ValidationError("InvalidWeight")

    is_homeless = data.get("isHomeless")
    if not isinstance(is_homeless, bool):
        raise ValidationError("InvalidIsHomeless")

    return data


"""
  Валидирует породу, окрас, дату рождения и особые приметы
"""


def validate_additional_description(data):
    breed = data.get("breed", "")
    color = data.get("color", "")
    birth_date = data.get("birthDate", "")
    special_marks = data.get("specialMarks", "")

    # Validate breed
    if breed and len(breed) > 20:
        raise ValidationError("Breed cannot exceed 20 characters.")

    # Validate color
    if color and len(color) > 20:
        raise ValidationError("Color cannot exceed 20 characters.")

    # Validate birth_date
    if birth_date:
        try:
            birth_date_obj = date.fromisoformat(birth_date)
            if birth_date_obj > date.today():
                raise ValidationError("Birth date cannot be in the future.")
        except ValueError:
            raise ValidationError("Invalid birth date format. Use YYYY-MM-DD.")

    # Validate special_marks
    if special_marks and len(special_marks) > 20:
        raise ValidationError("Special marks cannot exceed 20 characters.")

    return data


"""
  Валидирует данные идентиыикации - номер чипа, название клиники, место и дату установки чипа.
"""


def validate_identification(data):
    chip_number = data.get("chipNumber", "")
    clinic = data.get("clinic", "")
    location_install_chip = data.get("locationInstallChip", "")
    chip_date = data.get("chipDate", "")

    if chip_number and len(chip_number) > 35:
        raise ValidationError("Chip number cannot exceed 35 characters.")

    if clinic and len(clinic) > 20:
        raise ValidationError("Clinic name cannot exceed 20 characters.")

    if location_install_chip and len(location_install_chip) > 20:
        raise ValidationError("Installation location cannot exceed 20 characters.")

    if chip_date:
        try:
            chip_date_obj = date.fromisoformat(chip_date)
            if chip_date_obj > date.today():
                raise ValidationError("Chip installation date cannot be in the future.")
        except ValueError:
            raise ValidationError("Invalid chip installation date format. Use YYYY-MM-DD.")

    return data


"""
  Валидирует тип вакцины, ее имя, серию, срок годности, название клиники, дату вакцинации и срок окончания действия.
"""


def validate_vaccination(data):
    vaccine = data.get("vaccine", "")
    series = data.get("series", "")
    expiration_date = data.get("expirationDate", "")
    vaccination_clinic = data.get("vaccinationClinic", "")
    date_of_vaccination = data.get("dateOfVaccination", "")
    vaccine_expiration_date = data.get("vaccineExpirationDate", "")

    if vaccine and len(vaccine) > 20:
        raise ValidationError("Vaccine name cannot exceed 20 characters.")

    if series and len(series) > 20:
        raise ValidationError("Series cannot exceed 20 characters.")

    if vaccination_clinic and len(vaccination_clinic) > 20:
        raise ValidationError("Clinic name cannot exceed 20 characters.")

    if expiration_date:
        try:
            expiration_date_obj = date.fromisoformat(expiration_date)
            if expiration_date_obj < date.today():
                raise ValidationError("Expiration date must be in the future.")
        except ValueError:
            raise ValidationError("Invalid expiration date format. Use YYYY-MM-DD.")

    if date_of_vaccination:
        try:
            vaccination_date_obj = date.fromisoformat(date_of_vaccination)
            if vaccination_date_obj > date.today():
                raise ValidationError("Vaccination date cannot be in the future.")
        except ValueError:
            raise ValidationError("Invalid vaccination date format. Use YYYY-MM-DD.")

    if vaccine_expiration_date:
        try:
            vaccine_expiration_obj = date.fromisoformat(vaccine_expiration_date)
            if vaccine_expiration_obj < date.today():
                raise ValidationError("Vaccine expiration date must be in the future.")
        except ValueError:
            raise ValidationError("Invalid vaccine expiration date format. Use YYYY-MM-DD.")

    return data


"""
  Валидирует поля дегельминтизации - препарат, дату и название клиники.
"""


def validate_deworming(data):
    deworming_drug = data.get("dewormingDrug", "")
    deworming_date = data.get("dewormingDate", "")
    deworming_clinic = data.get("dewormingClinic", "")

    if deworming_drug and len(deworming_drug) > 35:
        raise ValidationError("Deworming drug name cannot exceed 35 characters.")

    if deworming_clinic and len(deworming_clinic) > 35:
        raise ValidationError("Deworming clinic name cannot exceed 35 characters.")

    if deworming_date:
        try:
            deworming_date_obj = date.fromisoformat(deworming_date)
            if deworming_date_obj > date.today():
                raise ValidationError("Deworming date cannot be in the future.")
        except ValueError:
            raise ValidationError("Invalid deworming date format. Use YYYY-MM-DD.")

    return data


"""
  Валидирует поля обработки - препарат, дату и название клиники.
"""


def validate_ectoparasite_treatment(data):
    ectoparasites_drug = data.get("ectoparasitesDrug", "")
    ectoparasites_date = data.get("ectoparasitesDate", "")
    ectoparasites_clinic = data.get("ectoparasitesClinic", "")

    if ectoparasites_drug and len(ectoparasites_drug) > 35:
        raise ValidationError("Ectoparasite treatment drug name cannot exceed 35 characters.")

    if ectoparasites_clinic and len(ectoparasites_clinic) > 35:
        raise ValidationError("Ectoparasite treatment clinic name cannot exceed 35 characters.")

    if ectoparasites_date:
        try:
            ectoparasites_date_obj = date.fromisoformat(ectoparasites_date)
            if ectoparasites_date_obj > date.today():
                raise ValidationError("Ectoparasite treatment date cannot be in the future.")
        except ValueError:
            raise ValidationError("Invalid ectoparasite treatment date format. Use YYYY-MM-DD.")

    return data


"""
  Валидирует поля клинического осмотра - дату, результат и файлы.
"""


def validate_clinical_examination(data):
    date_value = data.get("date", "")
    result = data.get("result", "")

    if result and len(result) > 20:
        raise ValidationError("Result cannot exceed 20 characters.")

    if date_value:
        try:
            examination_date_obj = date.fromisoformat(date_value)
            if examination_date_obj > date.today():
                raise ValidationError("Examination date cannot be in the future.")
        except ValueError:
            raise ValidationError("Invalid examination date format. Use YYYY-MM-DD.")

    return data


"""
  Валидирует поля регистрации - название клиники и регистрационный номер.
"""


def validate_registration(data):
    clinic = data.get("clinic", "")
    registration_number = data.get("registrationNumber", "")

    if clinic and len(clinic) > 20:
        raise ValidationError("Clinic name cannot exceed 20 characters.")

    if registration_number and len(registration_number) > 35:
        raise ValidationError("Registration number cannot exceed 35 characters.")

    return data


# """
#   Валидирует поля лечения - препарат, дозировка, периодичность, начало и окончание приема, календарь.
# """


# def validate_treatment_data(data):
#     medication = data.get("medication", "")
#     dosage = data.get("dosage", "")
#     frequency = data.get("frequency", "")
#     start_date = data.get("start_date", "")
#     end_date = data.get("end_date", "")
#     calendar = data.get("calendar", [])

#     # Validate medication
#     if not medication or len(medication) > 255:
#         raise ValidationError("Medication must be provided and cannot exceed 255 characters.")

#     # Validate dosage
#     if not dosage or len(dosage) > 100:
#         raise ValidationError("Dosage must be provided and cannot exceed 100 characters.")

#     # Validate frequency
#     if not frequency or len(frequency) > 100:
#         raise ValidationError("Frequency must be provided and cannot exceed 100 characters.")

#     # Validate start_date
#     if start_date:
#         try:
#             parsed_start_date = date.fromisoformat(start_date)
#             if parsed_start_date > date.today():
#                 raise ValidationError("Start date cannot be in the future.")
#         except ValueError:
#             raise ValidationError("Invalid start date format. Use YYYY-MM-DD.")

#     # Validate end_date
#     if end_date:
#         try:
#             parsed_end_date = date.fromisoformat(end_date)
#             if parsed_end_date < start_date:
#                 raise ValidationError("End date must be after or equal to the start date.")
#         except ValueError:
#             raise ValidationError("Invalid end date format. Use YYYY-MM-DD.")

#     # Validate calendar (array of dates)
#     if calendar:
#         if not isinstance(calendar, list):
#             raise ValidationError("Calendar must be a list of dates.")

#     return data


# """
#   Валидирует поля посещений - название клиники, дата посещения, жалобы, заключение, выписка и др. файлы.
# """


# def validate_appointment_data(data):
#     clinic_name = data.get("clinic_name", "")
#     visit_date = data.get("visit_date", "")
#     complaints = data.get("complaints", "")
#     doctor_report = data.get("doctor_report", "")
#     examination_files_ids = data.get("examination_files_ids", [])
#     other_files_ids = data.get("other_files_ids", [])

#     # Validate clinic_name
#     if not clinic_name or len(clinic_name) > 255:
#         raise ValidationError("Clinic name must be provided and cannot exceed 255 characters.")

#     # Validate visit_date
#     if visit_date:
#         try:
#             parsed_visit_date = date.fromisoformat(visit_date)
#             if parsed_visit_date > date.today():
#                 raise ValidationError("Visit date cannot be in the future.")
#         except ValueError:
#             raise ValidationError("Invalid visit date format. Use YYYY-MM-DD.")

#     # Validate complaints
#     if complaints and len(complaints) > 255:
#         raise ValidationError("Complaints description must be provided and cannot exceed 255 characters.")

#     # Validate doctor_report
#     if doctor_report and len(doctor_report) > 255:
#         raise ValidationError("Doctor report description must be provided and cannot exceed 255 characters.")

#     # Validate examination_files_ids
#     if examination_files_ids and not isinstance(examination_files_ids, list):
#         raise ValidationError("Examination files IDs must be a list.")

#     # Validate other_files_ids
#     if other_files_ids and not isinstance(other_files_ids, list):
#         raise ValidationError("Other files IDs must be a list.")

#     return data
