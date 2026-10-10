
import streamlit as st
import re
from datetime import date
from database.database import add_public_appointment

st.set_page_config(page_title="Book an Appointment", page_icon="📅")

st.title("📅 Book a Hospital Appointment")
st.write("Submit your appointment request. Our reception team will review it.")

with st.form("public_appointment_form"):
    patient_name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email (optional)")

    doctor_name = st.selectbox(
        "Select Doctor",
        ["Dr. Bilal", "Dr. Asif", "Dr. Aisha"]
    )

    appointment_date = st.date_input(
        "Preferred Date",
        min_value=date.today()
    )
    appointment_time = st.time_input("Preferred Time")
    reason = st.text_area("Reason for Visit (optional)")

    submitted = st.form_submit_button("Request Appointment")

if submitted:
    if not patient_name.strip():
        st.error("Please enter your full name.")
    elif not re.fullmatch(r"[6-9]\d{9}", phone.strip()):
        st.error("Enter a valid 10-digit Indian mobile number.")
    elif email.strip() and not re.fullmatch(
        r"[^@\s]+@[^@\s]+\.[^@\s]+", email.strip()
    ):
        st.error("Enter a valid email address.")
    else:
        try:
            request_id = add_public_appointment(
                patient_name=patient_name.strip(),
                phone=phone.strip(),
                email=email.strip(),
                doctor_name=doctor_name,
                appointment_date=str(appointment_date),
                appointment_time=str(appointment_time),
                reason=reason.strip()
            )
            st.success(f"Your appointment request has been submitted successfully! Request ID: {request_id}")
        except Exception as e:
            st.error(f"An error occurred while submitting your request: {e}")
