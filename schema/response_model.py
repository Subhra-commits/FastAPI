from pydantic import BaseModel, Field
from typing import Dict

class PredictedResponse(BaseModel):
    predicted_premium : str = Field(..., description= "Predited insurance premium category", examples='High')
    confidence_score : float = Field(..., description= "Model's confidence score for the predicted class (in range of o to 1)", examples=0.74)
    class_probabilities : Dict[str, float] = Field(..., description= "Probability distribution across all classes", examples= {"Low": 0.10, "Medium": 0.25, "High": 0.74}) 