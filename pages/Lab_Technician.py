import streamlit as st
from utils.auth import require_login

require_login(["Lab Technician"])

from database.database import (
    add_lab_report,
    search_patient,
    add_ai_prediction,
    get_latest_doctor_record
)

from utils.predict import predict_all


st.title("🧪 Laboratory Dashboard")
st.caption(
    "Record laboratory test results and generate AI-assisted disease predictions."
)


# -------------------------------------------------
# Session State
# -------------------------------------------------

if "lab_patient" not in st.session_state:
    st.session_state.lab_patient = None

if "lab_patient_id" not in st.session_state:
    st.session_state.lab_patient_id = None


def clear_loaded_patient():
    st.session_state.lab_patient = None
    st.session_state.lab_patient_id = None


# -------------------------------------------------
# Load Patient
# -------------------------------------------------

patient_id = st.number_input(
    "Patient ID",
    min_value=1,
    key="lab_patient_input",
    on_change=clear_loaded_patient
)

load_patient = st.button("Load Patient")


if load_patient:

    patient = search_patient(patient_id)

    if patient:

        st.session_state.lab_patient = patient
        st.session_state.lab_patient_id = patient_id

    else:

        st.session_state.lab_patient = None
        st.session_state.lab_patient_id = None

        st.error("❌ Patient ID not found.")


patient = None


if (
    st.session_state.lab_patient is not None
    and st.session_state.lab_patient_id == patient_id
):

    patient = st.session_state.lab_patient


# -------------------------------------------------
# Patient Information
# -------------------------------------------------

if patient:

    st.success("✅ Patient Loaded Successfully!")

    st.subheader("👤 Patient Information")

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            "**Patient Name:**",
            patient[1]
        )

        st.write(
            "**Age:**",
            patient[3]
        )

        st.write(
            "**Gender:**",
            patient[4]
        )

    with col2:

        st.write(
            "**Residence:**",
            patient[5]
        )

        st.write(
            "**Purpose of Visit:**",
            patient[6]
        )

    st.divider()


    # -------------------------------------------------
    # Doctor Requested Tests
    # -------------------------------------------------

    doctor_record = get_latest_doctor_record(patient_id)

    if doctor_record and doctor_record[4]:

        required_tests = [
            test.strip()
            for test in doctor_record[4].split(",")
            if test.strip()
        ]

        st.subheader("🩺 Doctor Requested Tests")

        st.success(
            "Doctor has requested the following laboratory investigations."
        )

        for test in required_tests:

            st.success(
                f"✔ {test}"
            )


        test_name = st.selectbox(
            "Select Test to Perform",
            required_tests
        )


        st.divider()

        st.subheader("🧪 Laboratory Results")


        # -------------------------------------------------
        # Blood Test
        # -------------------------------------------------

        if "Blood Test" in required_tests:

            st.markdown("### 🩸 Blood Test")

            hemoglobin = st.number_input(
                "Hemoglobin (g/dL)",
                min_value=0.0,
                max_value=30.0,
                value=None,
                placeholder="Enter hemoglobin result"
            )

            blood_sugar = st.number_input(
                "Blood Sugar (mg/dL)",
                min_value=0,
                max_value=1000,
                value=None,
                placeholder="Enter blood sugar result"
            )

        else:

            hemoglobin = None
            blood_sugar = None


        # -------------------------------------------------
        # ECG
        # -------------------------------------------------

        if (
            "Blood Test" in required_tests
            and "ECG" in required_tests
        ):

            st.divider()


        if "ECG" in required_tests:

            st.markdown("### ❤️ ECG")

            st.write("Blood Pressure (mmHg)")

            col1, col2 = st.columns(2)

            with col1:

                systolic_bp = st.number_input(
                    "Systolic",
                    min_value=50,
                    max_value=250,
                    value=None,
                    placeholder="Enter systolic BP"
                )

            with col2:

                diastolic_bp = st.number_input(
                    "Diastolic",
                    min_value=30,
                    max_value=150,
                    value=None,
                    placeholder="Enter diastolic BP"
                )

            heart_rate = st.number_input(
                "Heart Rate (bpm)",
                min_value=0,
                max_value=300,
                value=None,
                placeholder="Enter heart rate"
            )

        else:

            systolic_bp = None
            diastolic_bp = None
            heart_rate = None


        # -------------------------------------------------
        # Cholesterol Test
        # -------------------------------------------------

        if "Cholesterol Test" in required_tests:

            st.markdown("### 🧬 Cholesterol Test")

            cholesterol = st.number_input(
                "Cholesterol (mg/dL)",
                min_value=0,
                max_value=1000,
                value=None,
                placeholder="Enter cholesterol result"
            )

        else:

            cholesterol = None


        # -------------------------------------------------
        # Imaging
        # -------------------------------------------------

        imaging_result = ""


        if (
            "X-Ray" in required_tests
            or "MRI" in required_tests
            or "CT Scan" in required_tests
        ):

            st.markdown("### 🩻 Imaging Findings")

            imaging_result = st.text_area(
                "Findings"
            )


        st.divider()

        st.subheader("👩‍🔬 Laboratory Technician")


        technician_name = st.selectbox(
            "Laboratory Technician",
            [
                "Aqsa",
                "Zahra",
                "Arifa",
                "Iqra"
            ]
        )


        report_date = st.date_input(
            "Report Date"
        )


        save = st.button(
            "💾 Generate Laboratory Report"
        )


        if save:

            # -------------------------------------------------
            # Validate Blood Test
            # -------------------------------------------------

            if (
                "Blood Test" in required_tests
                and (
                    hemoglobin is None
                    or blood_sugar is None
                )
            ):

                st.error(
                    "⚠️ Please enter all Blood Test results."
                )

                st.stop()


            # -------------------------------------------------
            # Validate ECG
            # -------------------------------------------------

            if (
                "ECG" in required_tests
                and (
                    systolic_bp is None
                    or diastolic_bp is None
                    or heart_rate is None
                )
            ):

                st.error(
                    "⚠️ Please enter all ECG results."
                )

                st.stop()


            # -------------------------------------------------
            # Validate Cholesterol
            # -------------------------------------------------

            if (
                "Cholesterol Test" in required_tests
                and cholesterol is None
            ):

                st.error(
                    "⚠️ Please enter the cholesterol result."
                )

                st.stop()


            # -------------------------------------------------
            # Get Patient Information
            # -------------------------------------------------

            age = patient[3]
            gender = patient[4]


            # -------------------------------------------------
            # Prepare Laboratory Report
            # -------------------------------------------------

            test_result = ""


            if "Blood Test" in required_tests:

                test_result += (
                    "Blood Test Results:\n"
                    f"Hemoglobin: {hemoglobin} g/dL\n"
                    f"Blood Sugar: {blood_sugar} mg/dL\n"
                )


            if "ECG" in required_tests:

                test_result += (
                    "ECG Results:\n"
                    f"Blood Pressure: "
                    f"{systolic_bp}/{diastolic_bp} mmHg\n"
                    f"Heart Rate: {heart_rate} bpm\n"
                )


            if "Cholesterol Test" in required_tests:

                test_result += (
                    f"Cholesterol: {cholesterol} mg/dL\n"
                )


            if imaging_result:

                test_result += (
                    "Imaging Findings:\n"
                    f"{imaging_result}\n"
                )


            # -------------------------------------------------
            # Save Laboratory Report
            # -------------------------------------------------

            add_lab_report(
                patient_id,
                test_name,
                test_result,
                technician_name,
                str(report_date),
                "Completed"
            )
                        # -------------------------------------------------
            # AI-Assisted Disease Screening
            # -------------------------------------------------

            st.divider()

            st.subheader(
                "🤖 AI-Assisted Disease Screening"
            )


            predictions = {}


            # -------------------------------------------------
            # Anemia
            # Requires Blood Test + ECG
            # -------------------------------------------------

            if (
                "Blood Test" in required_tests
                and "ECG" in required_tests
            ):

                predictions["anemia"] = predict_all(
                    age,
                    gender,
                    blood_sugar,
                    systolic_bp,
                    diastolic_bp,
                    hemoglobin,
                    cholesterol,
                    heart_rate
                )["anemia"]


            # -------------------------------------------------
            # Diabetes + Hypertension
            # Require Blood Test + ECG + Cholesterol Test
            # -------------------------------------------------

            if (
                "Blood Test" in required_tests
                and "ECG" in required_tests
                and "Cholesterol Test" in required_tests
            ):

                all_predictions = predict_all(
                    age,
                    gender,
                    blood_sugar,
                    systolic_bp,
                    diastolic_bp,
                    hemoglobin,
                    cholesterol,
                    heart_rate
                )


                predictions["diabetes"] = (
                    all_predictions["diabetes"]
                )

                predictions["hypertension"] = (
                    all_predictions["hypertension"]
                )


            # -------------------------------------------------
            # Display AI Predictions
            # -------------------------------------------------

            if predictions:

                for key, prediction in predictions.items():

                    disease = prediction["disease"]

                    probability = (
                        prediction["risk_probability"]
                    )


                    # -------------------------------------------------
                    # Risk Level
                    # -------------------------------------------------

                    if probability >= 80:

                        risk = "High"

                        recommendation = (
                            "Consult Physician for further evaluation."
                        )


                    elif probability >= 50:

                        risk = "Moderate"

                        recommendation = (
                            "Further clinical evaluation is recommended."
                        )


                    else:

                        risk = "Low"

                        recommendation = (
                            "Continue routine monitoring and follow-up."
                        )


                    # -------------------------------------------------
                    # Save AI Prediction
                    # -------------------------------------------------

                    add_ai_prediction(
                        patient_id,
                        disease,
                        probability,
                        risk,
                        recommendation,
                        str(report_date)
                    )


                    # -------------------------------------------------
                    # Display Prediction
                    # -------------------------------------------------

                    st.markdown(
                        f"### {disease}"
                    )


                    col1, col2, col3 = st.columns(3)


                    with col1:

                        st.metric(
                            "Screening Result",
                            prediction["result"]
                        )


                    with col2:

                        st.metric(
                            "Risk Probability",
                            f"{probability:.2f}%"
                        )


                    with col3:

                        st.metric(
                            "Risk Level",
                            risk
                        )


                    st.info(
                        f"Recommendation: {recommendation}"
                    )


                st.success(
                    "🤖 AI screening completed based on "
                    "the available laboratory results."
                )


            else:

                st.info(
                    "ℹ️ AI screening was not performed because "
                    "the required laboratory parameters were not available."
                )


            # -------------------------------------------------
            # Success Messages
            # -------------------------------------------------

            st.success(
                "✅ Laboratory report saved successfully!"
            )

            st.info(
                "📄 Laboratory report and AI screening results "
                "are now available in the Doctor Dashboard."
            )


    else:

        st.warning(
            "⚠️ No laboratory tests were requested by the doctor."
        )


else:

    st.info(
        "👆 Enter Patient ID and click "
        "'Load Patient' to begin."
    )