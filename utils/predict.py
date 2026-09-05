import joblib
import pandas as pd

diabetes_model = joblib.load("models/diabetes_model.pkl")
hypertension_model = joblib.load("models/hypertension_model.pkl")
anemia_model = joblib.load("models/anemia_model.pkl")


def predict_diabetes(
    age,
    gender,
    glucose,
    systolic_bp,
    diastolic_bp,
    cholesterol,
    heart_rate
):

    male = 1 if str(gender).lower() == "male" else 0

    data = pd.DataFrame([{
        "male": male,
        "age": age,
        "glucose": glucose,
        "sysBP": systolic_bp,
        "diaBP": diastolic_bp,
        "totChol": cholesterol,
        "heartRate": heart_rate
    }])

    probability = diabetes_model.predict_proba(data)[0][1]
    prediction = diabetes_model.predict(data)[0]

    result = (
        "Diabetes Risk Detected"
        if prediction == 1
        else "No Diabetes Risk Detected"
    )

    confidence = probability if prediction == 1 else (1 - probability)

    return {
        "disease": "Diabetes",
        "result": result,
        "confidence": round(confidence * 100, 2),
        "risk_probability": round(probability * 100, 2)
    }


def predict_hypertension(
    age,
    gender,
    glucose,
    systolic_bp,
    diastolic_bp,
    cholesterol,
    heart_rate
):

    male = 1 if str(gender).lower() == "male" else 0

    data = pd.DataFrame([{
        "male": male,
        "age": age,
        "glucose": glucose,
        "sysBP": systolic_bp,
        "diaBP": diastolic_bp,
        "totChol": cholesterol,
        "heartRate": heart_rate
    }])

    probability = hypertension_model.predict_proba(data)[0][1]
    prediction = hypertension_model.predict(data)[0]

    result = (
        "Hypertension Risk Detected"
        if prediction == 1
        else "No Hypertension Risk Detected"
    )

    confidence = probability if prediction == 1 else (1 - probability)

    return {
        "disease": "Hypertension",
        "result": result,
        "confidence": round(confidence * 100, 2),
        "risk_probability": round(probability * 100, 2)
    }


def predict_anemia(
    age,
    blood_pressure,
    glucose,
    hemoglobin
):

    data = pd.DataFrame([{
        "age": age,
        "bp": blood_pressure,
        "bgr": glucose,
        "hemo": hemoglobin
    }])

    probability = anemia_model.predict_proba(data)[0][1]
    prediction = anemia_model.predict(data)[0]

    result = (
        "Anemia Risk Detected"
        if prediction == 1
        else "No Anemia Risk Detected"
    )

    confidence = probability if prediction == 1 else (1 - probability)

    return {
        "disease": "Anemia",
        "result": result,
        "confidence": round(confidence * 100, 2),
        "risk_probability": round(probability * 100, 2)
    }


def predict_all(
    age,
    gender,
    glucose,
    systolic_bp,
    diastolic_bp,
    hemoglobin,
    cholesterol,
    heart_rate
):

    diabetes = predict_diabetes(
        age,
        gender,
        glucose,
        systolic_bp,
        diastolic_bp,
        cholesterol,
        heart_rate
    )

    hypertension = predict_hypertension(
        age,
        gender,
        glucose,
        systolic_bp,
        diastolic_bp,
        cholesterol,
        heart_rate
    )

    anemia = predict_anemia(
        age,
        diastolic_bp,
        glucose,
        hemoglobin
    )

    return {
        "diabetes": diabetes,
        "hypertension": hypertension,
        "anemia": anemia
    }