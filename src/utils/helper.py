from json import dumps
from boto3 import resource, client
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


# Notify Emergency/IPD/OPD department to process further
def notify_internal_patient_dept(medical_info: map):
  sqs_client = resource("sqs")
  # list of queues
  emg_svc_queue = sqs_client.Queue("https://sqs.us-east-1.amazonaws.com/691685274845/hms-emg-svc")
  ipd_svc_queue = sqs_client.Queue("https://sqs.us-east-1.amazonaws.com/691685274845/hms-ipd-svc")
  opd_svc_queue = sqs_client.Queue("https://sqs.us-east-1.amazonaws.com/691685274845/hms-opd-svc")

  # enqeue the message to the respective queue
  if medical_info["transfer_to_dept"] == "emg":
    emg_svc_queue.send_message(
      MessageBody=dumps(medical_info)
    )
    return True
  elif medical_info["transfer_to_dept"] == "ipd":
    ipd_svc_queue.send_message(
      MessageBody=dumps(medical_info)
    )
    return True
  elif medical_info["transfer_to_dept"] == "opd":
    opd_svc_queue.send_message(
      MessageBody=dumps(medical_info)
    )
    return True
  else:
    return False