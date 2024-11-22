from fastapi import FastAPI
from requests import get, post
from models.patient import PatientInfoModel, PatientMedicalInfoModel, PatientTransferModel
from utils.helper import evaluate_patient_transfer_dept

app = FastAPI()

@app.post("/patient_onboard_start")
async def patient_onboard_start(patient_info: PatientInfoModel):
  """Patient onboard service start"""
  # submit the info to the patient_mgnt_svc on the cluster to get the patient ID, if exists
  # otherwise, the service register the patient and return the info

  # response = post("http://hms_patient_mgmt_svc/patients", json=patient_info)
  response = post("http://localhost:8080/patients", json=patient_info.model_dump(exclude_none=True))
  if response:
    resp = response.json()
    medical_info = resp["data"]["medical_info"]
    # print(medical_info)
    # send onboarding completed msg
    
    # evaluate what type of service is needed i.e. EMG (emergency)/IPD/OPD, and forward to the respective service
    eval_result: PatientTransferModel = evaluate_patient_transfer_dept(PatientMedicalInfoModel(**medical_info))
    return {
      "error": False,
      "data": eval_result
    }