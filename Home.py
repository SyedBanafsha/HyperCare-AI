import streamlit as st
from database.database import add_patient, search_patient

st.title("🏥 HyperCare AI")
st.set_page_config(
    page_title="HyperCare AI",
    page_icon="🏥",
    layout="wide"
)

st.subheader("Patient Registration")

with st.form("patient_registration"):

    patient_name = st.text_input("Patient Name")

    phone_number = st.text_input("Phone Number")
    email = st.text_input("Email Address")

    age = st.number_input("Age", min_value=0)

    gender = st.radio("Gender", ["Male", "Female", "Other"])

    residence = st.text_area("Residence")

    purpose_of_visit = st.text_input("Purpose of Visit")

    current_symptoms = st.text_area("Current Symptoms")

    register = st.form_submit_button("Register Patient")


if register:

    if patient_name.strip() == "":
        st.error("Please enter the patient's name.")

    elif phone_number.strip() == "":
        st.error("Please enter the phone number.")

    elif age <= 0:
        st.error("Please enter a valid age.")      

    elif residence.strip() == "":
        st.error("Please enter the residence.")

    elif purpose_of_visit.strip() == "":
        st.error("Please enter the purpose of visit.")

    elif current_symptoms.strip() == "":
        st.error("Please enter the current symptoms.")  

    else:
        add_patient(
            patient_name,
            phone_number,
            email,
            age,
            gender,
            residence,
            purpose_of_visit,
            current_symptoms
        )
        st.success("✅ Patient Registered Successfully!")