
import streamlit as st
from datetime import date
from utils.auth import require_login
from database.database import add_appointment, search_patient

require_login(["Patient"])

st.title("📅 Book an Appointment")
st.write("Request an appointment with your preferred doctor.")

patient_id = st.number_input(
    "Enter your Patient ID",
    min_value=1,
    step=1
)

doctor_name = st.selectbox(
    "Select Doctor",
    ["Dr. Bilal", "Dr. Asif", "Dr. Aisha"]
)

appointment_date = st.date_input(
    "Preferred Date",
    min_value=date.today()
)

appointment_time = st.time_input("Preferred Time")

if st.button("Submit Appointment Request"):
    patient = search_patient(int(patient_id))

    if patient is None:
        st.error("Patient ID not found. Please check your ID.")
    else:
        try:
            add_appointment(
                int(patient_id),
                doctor_name,
                str(appointment_date),
                str(appointment_time),
                "Pending"
            )
            st.success(
                "Appointment request submitted! "
                "Reception will review your request."
            )
        except Exception as e:
            st.error(f"Could not submit request: {e}")
