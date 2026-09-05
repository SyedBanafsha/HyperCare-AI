import streamlit as st
from utils.pdf_generator import generate_prescription_pdf
from utils.email_sender import send_prescription_email 
from database.database import (
    add_doctor_record,
    search_patient,
    get_latest_lab_report,
    get_all_ai_predictions
)

st.title("👨‍⚕️ Doctor Dashboard")
st.caption("Review patient information, laboratory reports, AI predictions, and record the doctor's consultation.")

if "doctor_patient" not in st.session_state:
    st.session_state.doctor_patient = None

if "doctor_patient_id" not in st.session_state:
    st.session_state.doctor_patient_id = None


def clear_loaded_patient():
    st.session_state.doctor_patient = None
    st.session_state.doctor_patient_id = None


patient_id = st.number_input(
    "Patient ID",
    min_value=1,
    key="doctor_patient_input",
    on_change=clear_loaded_patient
)

load_patient = st.button("Load Patient")

if load_patient:

    patient = search_patient(patient_id)

    if patient:

        st.session_state.doctor_patient = patient
        st.session_state.doctor_patient_id = patient_id

    else:

        st.session_state.doctor_patient = None
        st.session_state.doctor_patient_id = None
        patient = None

        st.error("❌ Patient not found.")

patient = st.session_state.doctor_patient

if patient is None:
    st.session_state.doctor_patient_id = None

elif st.session_state.doctor_patient_id != patient_id:
    patient = None

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
            st.write("**Current Symptoms:**", patient[7])
            st.write("**Purpose of Visit:**", patient[6])

    st.divider()
        # --------------------------------------------------
    # Latest Laboratory Report
    # --------------------------------------------------

    st.subheader("🧪 Latest Laboratory Report")

    lab = get_latest_lab_report(patient_id)

    if lab:

        st.write("**Test Name:**", lab[2])

        st.text(lab[3])

        st.write(
            "**Laboratory Technician:**",
            lab[4]
        )

        st.write(
            "**Report Date:**",
            lab[5]
        )

    else:

        st.info(
            "🧪 No laboratory report is available for this patient yet."
        )

    st.divider()

    # --------------------------------------------------
    # AI-Assisted Disease Screening
    # --------------------------------------------------

    st.subheader("🤖 AI-Assisted Disease Screening")

    predictions = get_all_ai_predictions(patient_id)

    if predictions:

        for prediction in predictions:

            disease = prediction[2]
            probability = prediction[3]
            risk = prediction[4]
            recommendation = prediction[5]

            st.markdown(f"### {disease}")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Risk Probability",
                    f"{probability:.2f}%"
                )

            with col2:
                st.metric(
                    "Risk Level",
                    risk
                )

            st.info(
                f"Recommendation: {recommendation}"
            )

    else:

        st.info(
            "🤖 AI screening results will appear here after "
            "the required laboratory investigations are completed."
        )

    st.warning(
        "⚠️ AI screening is for clinical decision support only. "
        "The final diagnosis and treatment decision remains with the doctor."
    )

    st.divider()
    st.subheader("🩺 Doctor Consultation")
    doctor_name = st.selectbox(
        "Consulting Doctor",
        [
            "Dr. Bilal",
            "Dr. Asif",
            "Dr. Mehak",
            "Dr. Ayesha"
        ]
    )

    visit_date = st.date_input("Visit Date")
    lab_required = st.checkbox("🧪 Laboratory Investigation Required")

    required_tests = []

    if lab_required:
        required_tests = st.multiselect(
        "Select Required Laboratory Tests",
        [
            "Blood Test",
            "Urine Test",
            "X-Ray",
            "ECG",
            "Cholesterol Test",
            "MRI",
            "CT Scan"
        ]
    )
    diagnosis = st.text_area("Diagnosis *")

    prescription = st.text_area("Prescription *")

    doctor_notes = st.text_area("Doctor Notes")
    if required_tests:
            st.info(
            "Selected Tests: " + ", ".join(required_tests)
        )

save = st.button("💾 Save Doctor Record")

if save:

    if not patient:
            st.error("❌ Please load a patient first.")

    elif diagnosis.strip() == "":
        st.error("⚠ Diagnosis is required.")

    elif prescription.strip() == "":
        st.error("⚠ Prescription is required.")

    else:

        add_doctor_record(
            patient_id,
            doctor_name,
            diagnosis,
            ", ".join(required_tests),
            prescription,
            doctor_notes,
            str(visit_date),
            "Pending"
        )

        st.success("✅ Doctor record saved successfully!")
        st.balloons()
        st.divider()

# --------------------------------------------------
# Generate Prescription PDF
# --------------------------------------------------

if st.button("📄 Generate Prescription PDF"):

    if patient is None:
        st.error("❌ Please load a patient first.")

    else:

        pdf_filename = f"Prescription_{patient_id}.pdf"

        generate_prescription_pdf(
            pdf_filename,
            patient_id,
            patient[1],
            patient[3],
            patient[4],
            doctor_name,
            diagnosis,
            prescription,
            doctor_notes,
            str(visit_date)
        )

        with open(pdf_filename, "rb") as pdf_file:

            st.download_button(
                label="⬇ Download Prescription PDF",
                data=pdf_file,
                file_name=pdf_filename,
                mime="application/pdf"
            )

        st.success("✅ Prescription PDF generated successfully!")


# --------------------------------------------------
# Email Prescription
# --------------------------------------------------

if st.button("📧 Email Prescription"):

    if patient is None:
        st.error("❌ Please load a patient first.")

    else:

        pdf_filename = f"Prescription_{patient_id}.pdf"

        try:

            send_prescription_email(
                receiver_email=patient[8],
                patient_name=patient[1],
                pdf_path=pdf_filename
            )

            st.success("✅ Prescription emailed successfully!")

        except Exception as e:

            st.error(f"❌ Email failed: {e}")


# --------------------------------------------------
# Initial Message
# --------------------------------------------------

if patient is None:
    st.info("👆 Enter Patient ID and click 'Load Patient' to begin.")