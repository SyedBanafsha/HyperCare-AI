import re
import streamlit as st
from database.database import add_patient
from login import login
from utils.auth import require_login

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="HyperCare AI",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 HyperCare AI")
st.subheader("Patient Registration")

# --------------------------------------------------
# LOGIN PROTECTION
# --------------------------------------------------
if not st.session_state.get("logged_in", False):
    login()
    st.stop()

require_login(["Reception"])
# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "touched_fields" not in st.session_state:
    st.session_state.touched_fields = set()

if "registration_submitted" not in st.session_state:
    st.session_state.registration_submitted = False

if "registration_result" not in st.session_state:
    st.session_state.registration_result = None


def mark_touched(field):
    """Remember that the user has interacted with a field."""
    st.session_state.touched_fields.add(field)
    st.session_state.registration_result = None


# --------------------------------------------------
# PATIENT NAME
# --------------------------------------------------
patient_name = st.text_input(
    "Patient Name",
    key="patient_name",
    on_change=mark_touched,
    args=("patient_name",)
)
name_error = st.empty()


# --------------------------------------------------
# PHONE NUMBER
# --------------------------------------------------
phone_number = st.text_input(
    "Phone Number",
    key="phone_number",
    on_change=mark_touched,
    args=("phone_number",)
)
phone_error = st.empty()


# --------------------------------------------------
# EMAIL ADDRESS
# --------------------------------------------------
email = st.text_input(
    "Email Address",
    key="email",
    on_change=mark_touched,
    args=("email",)
)
email_error = st.empty()


# --------------------------------------------------
# AGE
# --------------------------------------------------
age = st.number_input(
    "Age",
    min_value=0,
    max_value=100,
    step=1,
    key="age",
    on_change=mark_touched,
    args=("age",)
)
age_error = st.empty()


# --------------------------------------------------
# GENDER
# --------------------------------------------------
gender = st.radio(
    "Gender",
    ["Male", "Female", "Other"],
    key="gender"
)


# --------------------------------------------------
# RESIDENCE
# --------------------------------------------------
residence = st.text_area(
    "Residence",
    key="residence",
    on_change=mark_touched,
    args=("residence",)
)
residence_error = st.empty()


# --------------------------------------------------
# PURPOSE OF VISIT
# --------------------------------------------------
purpose_of_visit = st.text_input(
    "Purpose of Visit",
    key="purpose_of_visit",
    on_change=mark_touched,
    args=("purpose_of_visit",)
)
purpose_error = st.empty()


# --------------------------------------------------
# CURRENT SYMPTOMS
# --------------------------------------------------
current_symptoms = st.text_area(
    "Current Symptoms",
    key="current_symptoms",
    on_change=mark_touched,
    args=("current_symptoms",)
)
symptoms_error = st.empty()


# --------------------------------------------------
# REGISTER BUTTON
# --------------------------------------------------
register = st.button(
    "Register Patient",
    type="primary"
)

if register:
    st.session_state.registration_submitted = True
    st.session_state.touched_fields.update({
        "patient_name",
        "phone_number",
        "email",
        "age",
        "residence",
        "purpose_of_visit",
        "current_symptoms"
    })
    st.session_state.registration_result = None


# --------------------------------------------------
# VALIDATION RULES
# --------------------------------------------------
values = {
    "patient_name": patient_name.strip(),
    "phone_number": phone_number.strip(),
    "email": email.strip(),
    "age": age,
    "residence": residence.strip(),
    "purpose_of_visit": purpose_of_visit.strip(),
    "current_symptoms": current_symptoms.strip()
}

validators = {
    "patient_name": (
        bool(values["patient_name"]),
        "Please enter the patient's name."
    ),
    "phone_number": (
        bool(re.fullmatch(r"[6-9]\d{9}", values["phone_number"])),
        "Enter a valid 10-digit Indian mobile number."
    ),
    "email": (
    bool(re.fullmatch(
        r"[^@\s]+@[^@\s]+\.[^@\s]+",
        values["email"]
    )),
    "Please enter a valid email address."
),
    "age": (
        1 <= values["age"] <= 100,
        "Enter an age between 1 and 100."
    ),
    "residence": (
        bool(values["residence"]),
        "Please enter the residence."
    ),
    "purpose_of_visit": (
        bool(values["purpose_of_visit"]),
        "Please enter the purpose of visit."
    ),
    "current_symptoms": (
        bool(values["current_symptoms"]),
        "Please enter the current symptoms."
    )
}

error_placeholders = {
    "patient_name": name_error,
    "phone_number": phone_error,
    "email": email_error,
    "age": age_error,
    "residence": residence_error,
    "purpose_of_visit": purpose_error,
    "current_symptoms": symptoms_error
}

errors_found = False

# Show errors only for touched fields or after Register is clicked.
for field, (is_valid, message) in validators.items():
    should_validate = (
        field in st.session_state.touched_fields
        or st.session_state.registration_submitted
    )

    if should_validate:
        if not is_valid:
            error_placeholders[field].error(message)
            errors_found = True
        else:
            error_placeholders[field].empty()


# --------------------------------------------------
# SAVE PATIENT ONLY AFTER REGISTER IS CLICKED
# --------------------------------------------------
if register:
    if errors_found:
        st.warning(
            "Please correct the highlighted fields before registering."
        )

    else:
        try:
            registered = add_patient(
                values["patient_name"],
                values["phone_number"],
                values["email"],
                int(values["age"]),
                gender,
                values["residence"],
                values["purpose_of_visit"],
                values["current_symptoms"]
            )

            if registered:
                st.session_state.registration_result = (
                    "success",
                    "Patient registered successfully!"
                )
                st.session_state.registration_submitted = False
                st.session_state.touched_fields = set()

            else:
                # Duplicate details are reported beside the phone field.
                phone_error.error(
                    "A patient with this phone number or email already exists."
                )

        except Exception:
            st.session_state.registration_result = (
                "error",
                "Registration could not be completed. Please try again."
            )


# --------------------------------------------------
# REGISTRATION RESULT
# --------------------------------------------------
if st.session_state.registration_result:
    result_type, result_message = st.session_state.registration_result

    if result_type == "success":
        st.success(result_message)
    else:
        st.error(result_message)
