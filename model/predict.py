import pickle
import pandas as pd

with open('./model/model.pkl', 'rb') as f:
    model = pickle.load(f)

MODEL_VERSION = '1.0.0'

class_labels = model.classes_.tolist()

def predict_output(user_input: dict):
    user_input_df = pd.DataFrame([user_input])

    #Predict the class label
    predicted_class = model.predict(user_input_df)[0]

    #Get probabilities for each class
    probabilities = model.predict_proba(user_input_df)[0]
    confidence_score = max(probabilities)

    # Create Mapping {class_label: probability}
    class_probs = dict(zip(class_labels, map(lambda x: round(x, 4), probabilities)))


    return {
        'predicted_premium': predicted_class,
        'confidence_score': round(confidence_score, 4),
        'class_probabilities': class_probs
    }