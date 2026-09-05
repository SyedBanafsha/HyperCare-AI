import streamlit as st
from database.database import add_appointment

st.title("📅 Appointment Scheduling")

patient_id = st.number_input("Patient ID", min_value=1)

doctor_name = st.selectbox(
    "Select Doctor",
    ["Dr. Bilal", "Dr. Asif", "Dr. Aisha"]
)

appointment_date = st.date_input("Appointment Date")

appointment_time = st.time_input("Appointment Time")

book = st.button("Book Appointment")
if book:
    add_appointment(
        patient_id,
        doctor_name,
        str(appointment_date),
        str(appointment_time),
        "Scheduled"
    )

    st.success("✅ Appointment booked successfully!")