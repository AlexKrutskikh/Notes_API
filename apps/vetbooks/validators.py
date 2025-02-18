import re
from datetime import date

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
    breed = data.get("breed", "")
    color = data.get("color", "")
    birth_date = data.get("birth_date", "")
    special_marks = data.get("special_marks", "")

    # Validate vetbook id

    if not isinstance(vetbook_id, int):
        raise ValidationError("InvalidVetbookId")

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
    # Validate vetbook id
    vetbook_id = data.get("vetbook_id")
    if not isinstance(vetbook_id, int):
        raise ValidationError("InvalidVetbookId")

    clinic = data.get("clinic", "")
    registration_number = data.get("registration_number", "")

    if clinic and len(clinic) > 20:
        raise ValidationError("Clinic name cannot exceed 20 characters.")

    if registration_number and len(registration_number) > 35:
        raise ValidationError("Registration number cannot exceed 35 characters.")

    return data
