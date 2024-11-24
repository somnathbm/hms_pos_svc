import os
from fastapi import FastAPI
from uuid import uuid4
from requests import get, post
from models.patient import PatientInfoModel, PatientMedicalInfoModel, PatientTransferModel, PatientOnboardCompleteModel
from utils.helper import evaluate_patient_transfer_dept, evaluate_bed_availability

app = FastAPI()

@app.post("/patient-onboard-start", response_model=PatientOnboardCompleteModel)
async def patient_onboard_start(patient_info: PatientInfoModel):
  """Patient onboard service start"""
  # 1. →→ submit the info to the patient_mgnt_svc on the cluster to get the patient ID, if exists
  # otherwise, the service register the patient and return the info

  response = post(f"http://hms-patient-mgmt-svc-{os.getenv("CURR_ENV")}.{os.getenv("CURR_NS")}/patients", json=patient_info.model_dump(exclude_none=True))
  if response:
    resp = response.json()
    medical_info = resp["data"]["medical_info"]
    
    # 2. →→ evaluate what type of service is needed i.e. EMG (emergency)/IPD/OPD, and forward to the respective service
    eval_result: map = evaluate_patient_transfer_dept(PatientMedicalInfoModel(**medical_info))
    print(eval_result)

    # 3. →→ check with the BED MONITORING svc first, to see available bed for {target} department
    # bed_response = get(f"http://hms-bed-monitor-svc-{os.getenv("CURR_ENV")}.{os.getenv("CURR_NS")}/beds/bed_{eval_result['transfer_to_dept']}")
    # bed_data = bed_response.json()["data"]

    # eval_resp = evaluate_bed_availability(bed_data)

    # 4. →→ if bed is available, then queue the patient for {TARGET} department
    # use Kafka topic to publish message about admission/appointment
    # publish another message to Kafka topic / AWS SNS about onboard completion

    # 5. →→ return the onboard complete response
    onboard_complete_data = PatientOnboardCompleteModel(patient_id=medical_info["patientId"], transfer_to_dept=eval_result['transfer_to_dept'], visit_id=str(uuid4()))
    return onboard_complete_data