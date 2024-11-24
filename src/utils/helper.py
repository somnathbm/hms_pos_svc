from models.patient import PatientMedicalInfoModel, PatientTransferModel

# Evaluate in which department the patient shall be transferred prior to admission, just right after onboard completion
def evaluate_patient_transfer_dept(patient_medical_info: PatientMedicalInfoModel) -> map:
  """Evaluate in which department the patient shall be transferred prior to admission, 
    just right after onboard completion
  """
  pt_data: PatientTransferModel
  if patient_medical_info.serious:
    pt_data = PatientTransferModel(patient_id=patient_medical_info.patientId, transfer_to_dept="emg")
  elif patient_medical_info.planned:
    pt_data = PatientTransferModel(patient_id=patient_medical_info.patientId, transfer_to_dept="ipd")
  else:
    pt_data = PatientTransferModel(patient_id=patient_medical_info.patientId, transfer_to_dept="opd")
  return pt_data.model_dump()


# Evaluate bed availabiity
def check_bed_availability(bed_info: map):
  """Check bed availabiity"""
  # at least 1 bed should be available for patient transfer to admission
  return True if int(bed_info["available"]["Value"]) >= 1 else False