from rest_framework.exceptions import ValidationError
from datetime import date

"""
  Валидирует номер чипа, название клиники, место и дату установки чипа.
  Ожидает строку меньше 50 символов, две строки меньше 255 символов и дату YYYY-MM-DD соответсвенно. 
"""

def validate_identification_data(data):
    chip_number = data.get("chip_number", "")
    clinic_name = data.get("clinic_name", "")
    chip_installation_location = data.get("chip_installation_location", "")
    chip_installation_date = data.get("chip_installation_date", "")

    # Validate chip_number
    if chip_number and len(chip_number) > 50:
        raise ValidationError("Chip number cannot exceed 50 characters.")
    
    # Validate clinic_name
    if clinic_name and len(clinic_name) > 255:
        raise ValidationError("Clinic name cannot exceed 255 characters.")
    
    # Validate chip_installation_location
    if chip_installation_location and len(chip_installation_location) > 255:
        raise ValidationError("Chip installation location cannot exceed 255 characters.")
    
    # Validate chip_installation_date
    if chip_installation_date:
        try:
            installation_date = date.fromisoformat(chip_installation_date)
            if installation_date > date.today():
                raise ValidationError("Chip installation date cannot be in the future.")
        except ValueError:
            raise ValidationError("Invalid chip installation date format. Use YYYY-MM-DD.")
    
    return data

"""
  Валидирует тип вакцины, ее имя, серию, срок годности, название клиники, дату вакцинации и срок окончания действия.
"""

def validate_vaccination_data(data):

    valid_types = ["Dehelminthization", "Rabies", "Other"]
    
    type = data.get("type", "")
    vaccine_name = data.get("vaccine_name", "")
    batch_number = data.get("batch_number", "")
    expiration_date = data.get("expiration_date", "")
    clinic_name = data.get("clinic_name", "")
    administration_date = data.get("administration_date", "")
    validity_date = data.get("validity_date", "")

    # Validate type
    if type not in valid_types:
        raise ValidationError(f"Invalid vaccine type: {type}. Expected 'Dehelminthization', 'Rabies' or 'Other'.")

    # Validate vaccine_name
    if vaccine_name and len(vaccine_name) > 255:
        raise ValidationError("Vaccine name cannot exceed 255 characters.")
    
    # Validate batch_number
    if batch_number and len(batch_number) > 50:
        raise ValidationError("Batch number cannot exceed 50 characters.")
    
    # Validate clinic_name
    if clinic_name and len(clinic_name) > 255:
        raise ValidationError("Clinic name cannot exceed 255 characters.")
    
    # Validate expiration_date
    if expiration_date:
        try:
            exp_date = date.fromisoformat(expiration_date)
            if exp_date <= date.today():
                raise ValidationError("Expiration date must be in the future.")
        except ValueError:
            raise ValidationError("Invalid expiration date format. Use YYYY-MM-DD.")
    
    # Validate administration_date
    if administration_date:
        try:
            admin_date = date.fromisoformat(administration_date)
            if admin_date > date.today():
                raise ValidationError("Administration date cannot be in the future.")
        except ValueError:
            raise ValidationError("Invalid administration date format. Use YYYY-MM-DD.")
    
    # Validate validity_date
    if validity_date:
        try:
            valid_date = date.fromisoformat(validity_date)
            if valid_date <= administration_date:
                raise ValidationError("Validity date must be after administration date.")
        except ValueError:
            raise ValidationError("Invalid validity date format. Use YYYY-MM-DD.")
    
    return data


"""
  Валидирует поля обработки - препарат, дату и название клиники, если есть.
"""

def validate_procedure_data(data):
    medication = data.get("medication", "")
    processing_date = data.get("processing_date", "")
    clinic_name = data.get("clinic_name", "")

    # Validate medication
    if medication and len(medication) > 50:
        raise ValidationError("Medication name cannot exceed 50 characters.")
    
    # Validate processing_date
    if processing_date:
        try:
            proc_date = date.fromisoformat(processing_date)
            if proc_date > date.today():
                raise ValidationError("Processing date cannot be in the future.")
        except ValueError:
            raise ValidationError("Invalid processing date format. Use YYYY-MM-DD.")
    
    # Validate clinic_name
    if clinic_name and len(clinic_name) > 255:
        raise ValidationError("Clinic name cannot exceed 255 characters.")
    
    return data


"""
  Валидирует поля клинического осмотра - дату, результат и файлы.
"""

def validate_clinical_examination_data(data):
    examination_date = data.get("examination_date", "")
    results = data.get("results", "")
    files_ids = data.get("files_ids", "")

    # Validate examination_date
    if examination_date:
        try:
            exam_date = date.fromisoformat(examination_date)
            if exam_date > date.today():
                raise ValidationError("Examination date cannot be in the future.")
        except ValueError:
            raise ValidationError("Invalid examination date format. Use YYYY-MM-DD.")
    
    # Validate results
    if results and len(results) > 255:
        raise ValidationError("Results cannot exceed 255 characters.")
    
    # Validate files_ids
    if files_ids:
        if not isinstance(files_ids, list):
            raise ValidationError("Files IDs must be a list of strings.")
    
    return data


"""
  Валидирует поля регистрации - название клиники и регистрационный номер.
"""

def validate_registration_data(data):
    clinic_name = data.get("clinic_name", "")
    registration_number = data.get("registration_number", "")

    # Validate clinic_name
    if clinic_name and len(clinic_name) > 255:
        raise ValidationError("Clinic name cannot exceed 255 characters.")
    
    # Validate registration_number
    if registration_number and len(registration_number) > 50:
        raise ValidationError("Registration number cannot exceed 50 characters.")
    
    return data