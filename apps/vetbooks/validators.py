import re
from datetime import date, datetime

from rest_framework.exceptions import ValidationError

"""Валидация данных животного"""


def validate_create_data(data):

    question_id = data.get("question_id")
    if question_id and not isinstance(question_id, int):
        raise ValidationError("InvalidQuestionId")

    files_ids = data.get("files_ids")
    if files_ids and not isinstance(files_ids, list):
        raise ValidationError("InvalidFilesIds")

    if re.search(r"\d", data.get("name", "")):
        raise ValidationError("InvalidName")

    if re.search(r"\d", data.get("species", "")):
        raise ValidationError("InvalidSpecies")

    gender = data.get("gender")
    if gender and gender not in ["male", "female"]:
        raise ValidationError("InvalidGender")

    weight_str = data.get("weight")
    if weight_str:
        try:
            weight = float(weight_str)
            if weight <= 0:
                raise ValidationError("InvalidWeight")
        except ValueError:
            raise ValidationError("InvalidWeight")

    is_homeless = data.get("is_homeless")
    if is_homeless and not isinstance(is_homeless, bool):
        raise ValidationError("InvalidIsHomeless")

    return data


"""
  Валидирует породу, окрас, дату рождения и особые приметы
"""


def validate_additional_description(data):
    vetbook_id = data.get("vetbook_id")
    additional_information_id = data.get("additional_information_id")
    breed = data.get("breed", "")
    color = data.get("color", "")
    birth_date = data.get("birth_date", "")
    special_marks = data.get("special_marks", "")

    # Validate vetbook id
    if not isinstance(vetbook_id, int):
        raise ValidationError("InvalidVetbookId")

    # Validate additional information id
    if not isinstance(additional_information_id, int):
        raise ValidationError("InvalidAdditionalInformationId")

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
    # Validate vetbook id
    vetbook_id = data.get("vetbook_id")
    if not isinstance(vetbook_id, int):
        raise ValidationError("InvalidVetbookId")
    # Validate identification id
    identification_id = data.get("identification_id")
    if identification_id and not isinstance(identification_id, int):
        raise ValidationError("InvalidIdentificationId")

    chip_number = data.get("chip_number", "")
    clinic = data.get("clinic", "")
    chip_installation_location = data.get("chip_installation_location", "")
    chip_date = data.get("chipDate", "")

    if chip_number and len(chip_number) > 35:
        raise ValidationError("Chip number cannot exceed 35 characters.")

    if clinic and len(clinic) > 20:
        raise ValidationError("Clinic name cannot exceed 20 characters.")

    if chip_installation_location and len(chip_installation_location) > 20:
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

    # Validate vetbook id
    vetbook_id = data.get("vetbook_id")
    if not isinstance(vetbook_id, int):
        raise ValidationError("InvalidVetbookId")
    # Validate vaccination id
    vaccination_id = data.get("vaccination_id")
    if vaccination_id and not isinstance(vaccination_id, int):
        raise ValidationError("InvalidVaccinationId")

    type = data.get("type", "")
    vaccine = data.get("vaccine", "")
    series = data.get("series", "")
    expiration_date = data.get("expiration_date", "")
    vaccination_clinic = data.get("vaccination_clinic", "")
    date_of_vaccination = data.get("date_of_vaccination", "")
    vaccine_expiration_date = data.get("vaccine_expiration_date", "")

    if not type or type not in ["rabies", "other"]:
        raise ValidationError("Unknown vaccine type")

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
    # Validate vetbook id
    vetbook_id = data.get("vetbook_id")
    if not isinstance(vetbook_id, int):
        raise ValidationError("InvalidVetbookId")
    # Validate deworming id
    deworming_id = data.get("deworming_id")
    if deworming_id and not isinstance(deworming_id, int):
        raise ValidationError("InvalidDewormingId")

    deworming_drug = data.get("drug", "")
    deworming_date = data.get("date", "")
    deworming_clinic = data.get("clinic", "")

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
    # Validate vetbook id
    vetbook_id = data.get("vetbook_id")
    if not isinstance(vetbook_id, int):
        raise ValidationError("InvalidVetbookId")
    # Validate ectoparasite_treatment id
    ectoparasite_treatment_id = data.get("ectoparasite_treatment_id")
    if ectoparasite_treatment_id and not isinstance(ectoparasite_treatment_id, int):
        raise ValidationError("InvalidEctoparasiteTreatmentId")

    ectoparasites_drug = data.get("drug", "")
    ectoparasites_date = data.get("date", "")
    ectoparasites_clinic = data.get("clinic", "")

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
    # Validate vetbook id
    vetbook_id = data.get("vetbook_id")
    if not isinstance(vetbook_id, int):
        raise ValidationError("InvalidVetbookId")
    # Validate clinical_examination id
    clinical_examination_id = data.get("clinical_examination_id")
    if clinical_examination_id and not isinstance(clinical_examination_id, int):
        raise ValidationError("InvalidClinicalExaminationId")

    date_value = data.get("date", "")
    result = data.get("result", "")
    files_ids = data.get("files_ids", "")

    if result and len(result) > 20:
        raise ValidationError("Result cannot exceed 20 characters.")

    if date_value:
        try:
            examination_date_obj = date.fromisoformat(date_value)
            if examination_date_obj > date.today():
                raise ValidationError("Examination date cannot be in the future.")
        except ValueError:
            raise ValidationError("Invalid examination date format. Use YYYY-MM-DD.")

    # Validate files_ids
    if files_ids:
        if not isinstance(data["files_ids"], list):
            raise ValidationError("files_ids must be a list of file IDs.")

    return data


"""
  Валидирует поля регистрации - название клиники и регистрационный номер.
"""


def validate_registration(data):
    # Validate vetbook id
    vetbook_id = data.get("vetbook_id")
    if not isinstance(vetbook_id, int):
        raise ValidationError("InvalidVetbookId")
    # Validate registration id
    registration_id = data.get("registration_id")
    if registration_id and not isinstance(registration_id, int):
        raise ValidationError("InvalidRegistrationId")

    clinic = data.get("clinic", "")
    registration_number = data.get("registration_number", "")

    if clinic and len(clinic) > 20:
        raise ValidationError("Clinic name cannot exceed 20 characters.")

    if registration_number and len(registration_number) > 35:
        raise ValidationError("Registration number cannot exceed 35 characters.")

    return data


"""
Валидирует поля лечения
"""


def validate_treatment_data(data):
    required_fields = ["medication", "dosage", "frequency", "start_date", "end_date"]

    # Check for missing required fields
    for field in required_fields:
        if field not in data or not data[field]:
            raise ValidationError(f"{field} is required.")

    # Validate vetbook_id
    if "vetbook_id" in data and not isinstance(data["vetbook_id"], int):
        raise ValidationError("vetbook_id must be an integer.")

    # Validate treatment_id
    if "treatment_id" in data and not isinstance(data["treatment_id"], int):
        raise ValidationError("treatment_id must be an integer.")

    # Validate field length and formats if they exist in data
    if not isinstance(data["medication"], str) or len(data["medication"]) > 20:
        raise ValidationError("medication must be a string with a maximum of 20 characters.")

    if not isinstance(data["dosage"], str) or len(data["dosage"]) > 20:
        raise ValidationError("dosage must be a string with a maximum of 20 characters.")

    if not isinstance(data["frequency"], str) or len(data["frequency"]) > 20:
        raise ValidationError("frequency must be a string with a maximum of 20 characters.")

    try:
        datetime.strptime(data["start_date"], "%Y-%m-%d")
    except ValueError:
        raise ValidationError("start_date must be in YYYY-MM-DD format.")

    try:
        datetime.strptime(data["end_date"], "%Y-%m-%d")
    except ValueError:
        raise ValidationError("end_date must be in YYYY-MM-DD format.")

    return data


"""
Валидирует поля посещения в клинике
"""


def validate_appointment_data(data):
    required_fields = ["clinic_name", "visit_date", "complaints"]

    # Check for missing required fields
    for field in required_fields:
        if field not in data or not data[field]:
            raise ValidationError(f"{field} is required.")

    # Validate vetbook_id
    if "vetbook_id" in data and not isinstance(data["vetbook_id"], int):
        raise ValidationError("vetbook_id must be an integer.")

    # Validate appointment_id
    if "appointment_id" in data and not isinstance(data["appointment_id"], int):
        raise ValidationError("appointment_id must be an integer.")

    # Validate clinic_name
    if not isinstance(data["clinic_name"], str) or len(data["clinic_name"]) > 20:
        raise ValidationError("clinic_name must be a string with a maximum of 20 characters.")

    # Validate visit_date
    try:
        datetime.strptime(data["visit_date"], "%Y-%m-%d")
    except ValueError:
        raise ValidationError("visit_date must be in YYYY-MM-DD format.")

    # Validate complaints
    if not isinstance(data["complaints"], str) or len(data["complaints"]) > 35:
        raise ValidationError("complaints must be a string with a maximum of 35 characters.")

    # Validate doctor_report
    if "doctor_report" in data and data["doctor_report"]:
        if not isinstance(data["doctor_report"], str) or len(data["doctor_report"]) > 255:
            raise ValidationError("doctor_report must be a string with a maximum of 255 characters.")

    # Validate examination_files_ids
    if "examination_files_ids" in data and data["examination_files_ids"]:
        if not isinstance(data["examination_files_ids"], list):
            raise ValidationError("examination_files_ids must be a list of file IDs.")

    # Validate other_files_ids
    if "other_files_ids" in data and data["other_files_ids"]:
        if not isinstance(data["other_files_ids"], list):
            raise ValidationError("other_files_ids must be a list of file IDs.")

    return data
