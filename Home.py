
import streamlit as st
from login import login

st.set_page_config(
    page_title="HyperCare AI | Smarter Healthcare",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- PROFESSIONAL STYLING ----------
st.markdown("""
<style>
    .stApp {
        background-color: #f7fafc;
    }
    .block-container {
    padding: 2rem 3rem;
    max-width: 1500px;
}
    .brand {
        font-size: 30px;
        font-weight: 800;
        color: #12345a;
        letter-spacing: -1px;
    }
    .tagline {
        color: #527087;
        font-size: 13px;
    }
    .hero {
        background: linear-gradient(120deg, #e9f7fb, #ffffff);
        padding: 42px 32px;
        border-radius: 22px;
        border: 1px solid #dcecf3;
    }
    .hero h1 {
        color: #12345a;
        font-size: 43px;
        line-height: 1.15;
    }
    .hero p {
        color: #486276;
        font-size: 17px;
        line-height: 1.7;
    }
    .section-title {
        color: #12345a;
        font-size: 27px;
        font-weight: 750;
        margin-top: 25px;
    }
   div.stButton > button[kind="primary"] {
        background: #0b4778;
        color: white;
        border: none;
}
    div.stButton > button[kind="primary"]:hover {
        background: #087e8b;
        color: white;
}
</style>
""", unsafe_allow_html=True)


# ---------- PUBLIC HOMEPAGE ----------
if not st.session_state.get("logged_in", False):

    st.markdown("""
    <div class="brand">🏥 HyperCare AI</div>
    <div class="tagline">
        SMARTER HEALTHCARE. HEALTHIER TOMORROW.
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    left, right = st.columns([1.1, 0.9], gap="large")

    with left:
        st.markdown("""
        <div class="hero">
            <h1>Advanced Healthcare,<br>
            Powered by AI.</h1>
            <p>
            Experience a smarter approach to healthcare with
            streamlined appointments, digital medical workflows
            and AI-assisted healthcare tools.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        if st.button(
            "📅  Book an Appointment",
            type="primary",
            use_container_width=True
        ):
            st.session_state["show_public_booking"] = True
            st.rerun()

        if st.button("🔐  Hospital Staff Login", use_container_width=True):
            st.session_state["show_staff_login"] = True
            st.rerun()

    with right:
        st.image(
            "https://images.unsplash.com/photo-1551076805-e1869033e561"
            "?auto=format&fit=crop&w=1000&q=85",
            use_container_width=True
        )

    st.markdown(
        '<div class="section-title">Healthcare, made simpler.</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("### 📅 Easy Appointments")
        st.write("Submit an appointment request online without staff login.")

    with c2:
        st.markdown("### 🧠 AI-Assisted Workflows")
        st.write("Explore intelligent tools designed to support healthcare workflows.")

    with c3:
        st.markdown("### 🔒 Role-Based Staff Access")
        st.write("Separate workspaces for authorized hospital team members.")

    st.divider()
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)
    st.caption(
        "HyperCare AI | AI-Assisted Healthcare Workflow System"
    )

    # Public booking form
    if st.session_state.get("show_public_booking", False):
        st.markdown("## 📅 Book a Hospital Appointment")
        if st.button("← Back to Home"):
            st.session_state["show_public_booking"] = False
            st.rerun()

        # Render your existing public form here
        from pathlib import Path
        public_page = Path(__file__).parent / "pages" / "Public_Appointment.py"
        exec(compile(
            public_page.read_text(encoding="utf-8"),
            str(public_page),
            "exec"
        ))

    # Staff login
    elif st.session_state.get("show_staff_login", False):
        st.markdown("## 🔐 Hospital Staff Login")
        if st.button("← Back to Home"):
            st.session_state["show_staff_login"] = False
            st.rerun()

        login()

    st.stop()


# ---------- PROTECTED STAFF NAVIGATION ----------
role = st.session_state.get("role")

patient_appointment_page = st.Page(
    "pages/Patient_Appointment.py",
    title="Book an Appointment",
    icon="📅"
)

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
    "Patient": [
        patient_appointment_page,
    ],
}

if role not in page_options:
    st.error("Your account has no valid role. Please contact the administrator.")
    st.stop()

navigation = st.navigation(page_options[role])
navigation.run()
