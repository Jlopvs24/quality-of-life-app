import pandas as pd, numpy as np, joblib, os

def prediction(input, path):

    model = joblib.load(os.path.join(path, "pkl", "rf_model.pkl"))
    label_encoder = joblib.load(os.path.join(path, "pkl", "label_encoder.pkl"))
    education, jobs, income, safety, health, environment, civic, access, housing, community = input

    user_input = pd.DataFrame([{'Education': education,
                                                'Jobs': jobs,
                                                'Income': income,
                                                'Safety': safety,
                                                'Health': health,
                                                'Environment': environment,
                                                'Civic engagement': civic,
                                                'Accessibility to services': access,
                                                'Housing': housing,
                                                'Community': community}])

    # Predicción
    probs = model.predict_proba(user_input)[0]
    top_3_idx = np.argsort(probs)[::-1][:3]
    top = [label_encoder.inverse_transform([idx])[0] for idx in top_3_idx]
    
    return top, probs, user_input