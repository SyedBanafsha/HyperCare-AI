
import streamlit as st
import re
from datetime import date
from database.database import add_public_appointment

st.markdown("### Patient Details")
st.caption("Fields marked * are required.")

patient_name = st.text_input("Full Name *")
phone = st.text_input("Mobile Number *")
email = st.text_input("Email Address (optional)")

doctor_name = st.selectbox(
    "Choose a Doctor *",
    ["Select a doctor", "Dr. Bilal", "Dr. Asif", "Dr. Aisha"]
)

appointment_date = st.date_input(
    "Preferred Date *",
    min_value=date.today()
)

appointment_time = st.time_input("Preferred Time *")
reason = st.text_area("Reason for Visit (optional)")

if st.button("Submit Appointment Request", type="primary",
             use_container_width=True):

    errors = []

    if not patient_name.strip():
        errors.append("Please enter your full name.")

    if not re.fullmatch(r"[6-9]\d{9}", phone.strip()):
        errors.append("Enter a valid 10-digit Indian mobile number.")

    if email.strip() and not re.fullmatch(
        r"[^@\s]+@[^@\s]+\.[^@\s]+", email.strip()
    ):
        errors.append("Enter a valid email address.")

    if doctor_name == "Select a doctor":
        errors.append("Please select a doctor.")

    if appointment_date < date.today():
        errors.append("Please select today or a future date.")

    if errors:
        for error in errors:
            st.error(error)

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

            st.success(
                f"Appointment request submitted successfully! "
                f"Reference number: {request_id}. "
                "Reception will review your request."
            )

        except ValueError as e:
            st.warning(str(e))

        except Exception as e:
            st.error(f"Appointment could not be saved: {e}")
