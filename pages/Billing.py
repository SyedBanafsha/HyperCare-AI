import streamlit as st
from utils.auth import require_login

require_login(["Admin", "Reception"])
from database.database import (
    add_bill,
    search_patient,
    generate_bill_pdf
)

st.title("💳 Billing Dashboard")

# ----------------------------------
# Session State
# ----------------------------------

if "billing_patient" not in st.session_state:
    st.session_state.billing_patient = None

if "billing_patient_id" not in st.session_state:
    st.session_state.billing_patient_id = None


def clear_loaded_patient():
    st.session_state.billing_patient = None
    st.session_state.billing_patient_id = None


# ----------------------------------
# Patient ID
# ----------------------------------

patient_id = st.number_input(
    "Patient ID",
    min_value=1,
    key="billing_patient_input",
    on_change=clear_loaded_patient
)

load_patient = st.button("Load Patient")

if load_patient:
    patient = search_patient(patient_id)

    if patient:
        st.session_state.billing_patient = patient
        st.session_state.billing_patient_id = patient_id
    else:
        st.session_state.billing_patient = None
        st.session_state.billing_patient_id = None


patient = None

if (
    st.session_state.billing_patient is not None
    and st.session_state.billing_patient_id == patient_id
):
    patient = st.session_state.billing_patient


# ----------------------------------
# Main Screen
# ----------------------------------

if patient:

    st.success("✅ Patient Loaded Successfully!")

    st.subheader("👤 Patient Information")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Patient Name:**", patient[1])
        st.write("**Age:**", patient[3])
        st.write("**Gender:**", patient[4])

    with col2:
        st.write("**Residence:**", patient[5])
        st.write("**Purpose of Visit:**", patient[6])

    st.divider()

    st.subheader("💳 Billing Details")

    consultation_fee = 500

    st.number_input(
        "Consultation Fee",
        value=consultation_fee,
        disabled=True
    )

    lab_fee = st.number_input(
        "Lab Fee",
        min_value=0,
        value=0,
        step=1
    )

    medicine_fee = st.number_input(
        "Medicine Fee",
        min_value=0,
        value=0,
        step=1
    )

    payment_status = st.selectbox(
        "Payment Status",
        ["Paid", "Pending"]
    )

    billing_date = st.date_input("Billing Date")

    total_amount = consultation_fee + lab_fee + medicine_fee

    st.subheader("💰 Total Bill")

    st.success(f"₹ {total_amount}")

    save = st.button("Generate Bill")

    if save:

        add_bill(
            patient_id,
            consultation_fee,
            lab_fee,
            medicine_fee,
            total_amount,
            payment_status,
            str(billing_date)
        )

        pdf_file = generate_bill_pdf(
            patient_id,
            patient[1],
            patient[3],
            patient[4],
            patient[5],
            consultation_fee,
            lab_fee,
            medicine_fee,
            total_amount,
            payment_status,
            str(billing_date)
        )

        st.success("✅ Bill generated successfully!")

        with open(pdf_file, "rb") as file:

            st.download_button(
                label="📄 Download Bill",
                data=file,
                file_name=pdf_file,
                mime="application/pdf"
            )

elif load_patient:

    st.error("❌ Patient Not Found!")

else:

    st.info("👆 Enter Patient ID and click 'Load Patient'.")                 