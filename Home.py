
import streamlit as st
from login import login

st.set_page_config(
    page_title="HyperCare AI",
    page_icon="🏥",
    layout="wide"
)

# Show login before displaying role-specific navigation
if not st.session_state.get("logged_in", False):
    login()
    st.stop()

role = st.session_state.get("role")

# Define pages available to each role
page_options = {
    "Admin": [
        st.Page("pages/Admin_Dashboard.py", title="Admin Dashboard", icon="📊"),
        st.Page("pages/Billing_History.py", title="Billing History", icon="🧾"),
    ],
    "Reception": [
        st.Page("pages/Patient_Registration.py", title="Patient Registration", icon="📝"),
        st.Page("pages/Search_Patient.py", title="Search Patient", icon="🔎"),
        st.Page("pages/Appointment.py", title="Appointments", icon="📅"),
        st.Page("pages/Billing.py", title="Billing", icon="💳"),
        st.Page("pages/Billing_History.py", title="Billing History", icon="🧾"),
    ],
    "Doctor": [
        st.Page("pages/Doctor_Dashboard.py", title="Doctor Dashboard", icon="🩺"),
        st.Page("pages/Search_Patient.py", title="Search Patient", icon="🔎"),
    ],
    "Lab Technician": [
        st.Page("pages/Lab_Technician.py", title="Lab Technician", icon="🧪"),
    ],
}

if role not in page_options:
    st.error("Your account has no valid role. Please contact the administrator.")
    st.stop()

# Run only the pages allowed for this role
navigation = st.navigation(page_options[role])
navigation.run()
