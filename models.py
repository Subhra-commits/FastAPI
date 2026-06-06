from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient", example=['P001'])]
    name: Annotated[str, Field(..., description = "name of the patient", examples=['John Doe'])]
    city: Annotated[str, Field(..., description = "city of the patient")]
    age: Annotated[int, Field(...,gt=0, le=120, description = 'Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description= 'Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description= 'Height of the patient (in meters)')]
    weight: Annotated[float, Field(..., gt=0, description= 'Weight of the patient (in kgs)')]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / self.height**2, 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'    
        elif self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'
        
#New model for update a patient
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(description = "name of the patient", default = None)]
    city: Annotated[Optional[str], Field(description = "city of the patient", default = None)]
    age: Annotated[Optional[int], Field(gt=0, le=120, description = 'Age of the patient', default = None)]
    gender: Annotated[Optional[Literal['male', 'female', 'others']], Field(description= 'Gender of the patient', default = None)]
    height: Annotated[Optional[float], Field(gt=0, description= 'Height of the patient (in meters)', default = None)]
    weight: Annotated[Optional[float], Field(gt=0, description= 'Weight of the patient (in kgs)', default = None)]