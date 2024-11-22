from pydantic import BaseModel, EmailStr
from typing import Optional

class PatientBaseInfoModel(BaseModel):
  name: str
  sex: str
  age: int
  phone: str
  email: EmailStr
  address: str

class PatientMedicalInfoModel(BaseModel):
  patientId: Optional[str] = None
  illness_primary: str
  department: str
  serious: bool = False
  planned: bool = False

class PatientInfoModel(BaseModel):
  basic_info: PatientBaseInfoModel
  medical_info: PatientMedicalInfoModel

class PatientTransferModel(BaseModel):
  patient_id: str
  transfer_to_dept: str