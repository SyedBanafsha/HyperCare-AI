
import streamlit as st
from pathlib import Path
from login import login

st.set_page_config(
    page_title="HyperCare AI | Smarter Healthcare",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- PROFESSIONAL WEBSITE STYLING ----------
st.markdown("""
<style>
    .stApp {
        background: #f6f9fc;
    }

    .block-container {
        max-width: 1400px;
        padding: 2rem 3rem 3rem;
    }

    .brand {
        color: #12345a;
        font-size: 30px;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .tagline {
        color: #087e8b;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2px;
    }

    .hero {
        background: linear-gradient(135deg, #e8f5fb, #ffffff);
        padding: 35px 30px;
        border: 1px solid #dceaf2;
        border-radius: 20px;
        min-height: 310px;
    }

    .hero h1 {
        color: #12345a;
        font-size: 42px;
        line-height: 1.2;
    }

    .hero p {
        color: #536b7e;
        font-size: 16px;
        line-height: 1.8;
    }

    .eyebrow {
        color: #087e8b;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1.5px;
    }

    .section-title {
        color: #12345a;
        font-size: 29px;
        font-weight: 800;
        margin-top: 25px;
    }

    .section-description {
        color: #647789;
        font-size: 15px;
        line-height: 1.8;
    }

    .service-card {
        background: #ffffff;
        border: 1px solid #e0eaf0;
        border-radius: 16px;
        padding: 23px 20px;
        min-height: 205px;
    }

    .service-card h3 {
        color: #12345a;
        font-size: 19px;
    }

    .service-card p {
        color: #607487;
        font-size: 14px;
        line-height: 1.8;
    }

    .info-panel {
        background: #eaf5f8;
        border: 1px solid #d7e9ef;
        border-radius: 16px;
        padding: 24px;
    }

    .site-footer {
        border-top: 1px solid #dce5eb;
        margin-top: 35px;
        padding-top: 22px;
        color: #748494;
        font-size: 12px;
        line-height: 1.9;
    }

    div.stButton > button[kind="primary"] {
        background: #104b78;
        color: white;
        border: none;
        border-radius: 9px;
        min-height: 45px;
        font-weight: 700;
    }

    div.stButton > button[kind="primary"]:hover {
        background: #087e8b;
        color: white;
    }

    div.stButton > button {
        border-radius: 9px;
        min-height: 42px;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 1rem;
        }

        .hero {
            padding: 24px;
        }

        .hero h1 {
            font-size: 32px;
        }
    }
</style>
""", unsafe_allow_html=True)


# ---------- PUBLIC WEBSITE ----------
if not st.session_state.get("logged_in", False):

    show_booking = st.session_state.get(
        "show_public_booking", False
    )
    show_staff_login = st.session_state.get(
        "show_staff_login", False
    )

    # Hide the staff sidebar throughout the public experience.
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)

    # ---------- PUBLIC APPOINTMENT PAGE ----------
    if show_booking:

        st.markdown("## 📅 Book an Appointment")
        st.caption(
            "Submit your preferred appointment details. "
            "Our reception team will review your request."
        )

        if st.button("← Back to Home", key="booking_back_home"):
            st.session_state["show_public_booking"] = False
            st.session_state["show_staff_login"] = False
            st.rerun()

        public_page = (
            Path(__file__).parent
            / "pages"
            / "Public_Appointment.py"
        )

        if not public_page.exists():
            st.error(
                "Public_Appointment.py could not be found "
                "inside the pages folder."
            )
            st.stop()

        exec(compile(
            public_page.read_text(encoding="utf-8"),
            str(public_page),
            "exec"
        ))

        st.stop()

    # ---------- STAFF LOGIN PAGE ----------
    elif show_staff_login:

        st.markdown("## 🔐 Hospital Staff Portal")
        st.caption(
            "Secure sign-in for authorized hospital team members."
        )

        if st.button("← Back to Home", key="staff_back_home"):
            st.session_state["show_staff_login"] = False
            st.session_state["show_public_booking"] = False
            st.rerun()

        login()
        st.stop()

    # ---------- PUBLIC HOMEPAGE ----------
    else:

        # Header
        header_left, header_right = st.columns([3, 1])

        with header_left:
            st.markdown("""
            <div class="brand">🏥 HyperCare AI</div>
            <div class="tagline">
                SMARTER HEALTHCARE. HEALTHIER TOMORROW.
            </div>
            """, unsafe_allow_html=True)

        with header_right:
            st.write("")
            if st.button(
                "🔐 Staff Portal",
                use_container_width=True
            ):
                st.session_state["show_staff_login"] = True
                st.session_state["show_public_booking"] = False
                st.rerun()

        st.divider()

        # Hero section
        hero_left, hero_right = st.columns(
            [1.05, 0.95],
            gap="large"
        )

        with hero_left:
            st.markdown("""
            <div class="hero">
                <div class="eyebrow">
                    INTELLIGENT HEALTHCARE WORKFLOWS
                </div>
                <h1>Better Care.<br>Smarter Connections.</h1>
                <p>
                    A smarter approach to healthcare administration,
                    with appointment requests, digital patient workflows
                    and AI-assisted health-risk analysis.
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.write("")

            if st.button(
                "📅 Request an Appointment",
                type="primary",
                use_container_width=True
            ):
                st.session_state["show_public_booking"] = True
                st.session_state["show_staff_login"] = False
                st.rerun()

            st.caption(
                "Appointment requests are reviewed by reception."
            )

        with hero_right:
            st.image(
                "https://images.unsplash.com/photo-1551076805-e1869033e561"
                "?auto=format&fit=crop&w=1100&q=85",
                use_container_width=True
            )

            st.markdown("""
            <div class="info-panel">
                <h3 style="color:#12345a;margin-top:0;">
                    Healthcare, connected.
                </h3>
                <p style="color:#536b7e;line-height:1.8;">
                    Bring appointment management, patient information
                    and administrative workflows together in one
                    digital platform.
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Services section
        st.write("")
        st.markdown(
            '<div class="section-title">Our Platform Services</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<p class="section-description">'
            'Explore the capabilities available in HyperCare AI.'
            '</p>',
            unsafe_allow_html=True
        )

        c1, c2, c3 = st.columns(3, gap="medium")

        with c1:
            st.markdown("""
            <div class="service-card">
                <div style="font-size:28px;">📅</div>
                <h3>Appointment Requests</h3>
                <p>
                    Submit your preferred doctor, date and time.
                    Reception reviews your request before confirmation.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown("""
            <div class="service-card">
                <div style="font-size:28px;">🧠</div>
                <h3>AI-Assisted Analysis</h3>
                <p>
                    Explore machine-learning health-risk predictions
                    designed to support, not replace, medical judgement.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown("""
            <div class="service-card">
                <div style="font-size:28px;">🗂️</div>
                <h3>Digital Workflows</h3>
                <p>
                    Support patient records, laboratory workflows,
                    billing and staff administration.
                </p>
            </div>
            """, unsafe_allow_html=True)

        # About section
        st.write("")
        st.markdown(
            '<div class="section-title">About HyperCare AI</div>',
            unsafe_allow_html=True
        )

        about_left, about_right = st.columns(
            [1.2, 0.8],
            gap="large"
        )

        with about_left:
            st.markdown("""
            <p class="section-description">
                HyperCare AI is an AI-assisted healthcare workflow
                project focused on making routine administrative
                processes more organised and efficient. It explores
                how digital tools and machine learning can support
                appointment management, patient information and
                health-risk analysis.
            </p>
            """, unsafe_allow_html=True)

        with about_right:
            st.markdown("""
            <div class="info-panel">
                <h3 style="color:#12345a;margin-top:0;">
                    Our Priorities
                </h3>
                <p style="color:#536b7e;line-height:2;">
                    ✓ Simpler appointment requests<br>
                    ✓ Organised digital workflows<br>
                    ✓ Responsible AI-assisted analysis
                </p>
            </div>
            """, unsafe_allow_html=True)

        # For patients section
        st.write("")
        st.markdown(
            '<div class="section-title">For Patients</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<p class="section-description">'
            'Here is how to request an appointment.'
            '</p>',
            unsafe_allow_html=True
        )

        p1, p2, p3 = st.columns(3, gap="medium")

        with p1:
            st.markdown("### 01 · Submit")
            st.write(
                "Enter your contact details and preferred appointment slot."
            )

        with p2:
            st.markdown("### 02 · Review")
            st.write(
                "The reception team reviews your appointment request."
            )

        with p3:
            st.markdown("### 03 · Confirmation")
            st.write(
                "Reception checks availability and updates your request status."
            )

        # The main appointment button above is the single booking entry point.

        # Footer
        st.markdown("""
        <div class="site-footer">
            <strong style="color:#12345a;">🏥 HyperCare AI</strong><br>
            AI-Assisted Healthcare Workflow System<br>
            A healthcare technology project exploring connected
            workflows and responsible AI.<br><br>
            AI-assisted risk predictions are not a substitute
            for professional medical advice.
        </div>
        """, unsafe_allow_html=True)

        st.stop()


# ---------- PROTECTED STAFF NAVIGATION ----------
# This section runs only after login.

role = st.session_state.get("role")

patient_appointment_page = st.Page(
    "pages/Patient_Appointment.py",
    title="Book an Appointment",
    icon="📅"
)

page_options = {
    "Admin": [
        st.Page(
            "pages/Admin_Dashboard.py",
            title="Admin Dashboard",
            icon="📊"
        ),
        st.Page(
            "pages/Billing_History.py",
            title="Billing History",
            icon="🧾"
        ),
    ],
    "Reception": [
        st.Page(
            "pages/Patient_Registration.py",
            title="Patient Registration",
            icon="📝"
        ),
        st.Page(
            "pages/Search_Patient.py",
            title="Search Patient",
            icon="🔎"
        ),
        st.Page(
            "pages/Appointment.py",
            title="Appointments",
            icon="📅"
        ),
        st.Page(
            "pages/Billing.py",
            title="Billing",
            icon="💳"
        ),
        st.Page(
            "pages/Billing_History.py",
            title="Billing History",
            icon="🧾"
        ),
    ],
    "Doctor": [
        st.Page(
            "pages/Doctor_Dashboard.py",
            title="Doctor Dashboard",
            icon="🩺"
        ),
        st.Page(
            "pages/Search_Patient.py",
            title="Search Patient",
            icon="🔎"
        ),
    ],
    "Lab Technician": [
        st.Page(
            "pages/Lab_Technician.py",
            title="Lab Technician",
            icon="🧪"
        ),
    ],
    "Patient": [
        patient_appointment_page,
    ],
}

if role not in page_options:
    st.error(
        "Your account has no valid role. Please contact the administrator."
    )
    st.stop()

navigation = st.navigation(page_options[role])
navigation.run()
