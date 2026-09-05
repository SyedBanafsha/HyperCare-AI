import streamlit as st
import pandas as pd
from database.database import (
    get_total_patients,
    get_total_appointments,
    get_total_lab_reports,
    get_total_doctor_records,
    get_total_ai_predictions,
    get_total_revenue,
    get_recent_patients,
    get_recent_appointments,
    get_disease_statistics,
    get_revenue_data
)

st.title("🏥 HyperCare AI")
st.markdown("## Hospital Management Dashboard")
st.caption("Real-time Hospital Analytics & Administration")

patients = get_total_patients()
appointments = get_total_appointments()
lab_reports = get_total_lab_reports()
doctor_records = get_total_doctor_records()
ai_predictions = get_total_ai_predictions()
revenue = get_total_revenue()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("👥 Total Patients", patients)

with col2:
    st.metric("📅 Appointments", appointments)

with col3:
    st.metric("🧪 Lab Reports", lab_reports)

col4, col5, col6 = st.columns(3)

with col4:
    st.metric("👨‍⚕️ Doctor Records", doctor_records)

with col5:
    st.metric("🤖 AI Predictions", ai_predictions)

with col6:
    st.metric("💰 Total Revenue", f"₹ {revenue:.2f}")

st.divider()

st.subheader("👥 Recently Registered Patients")

patients = get_recent_patients()

if patients:
    df = pd.DataFrame(
        patients,
        columns=[
            "Patient Name",
            "Age",
            "Gender",
            "Purpose of Visit"
        ]
    )

    st.dataframe(df, use_container_width=True)

else:
    st.info("No patients available.")    

st.divider()

st.subheader("🗓️ Upcoming / Recent Appointments")

appointments = get_recent_appointments()

if appointments:

    df = pd.DataFrame(
        appointments,
        columns=[
            "Patient ID",
            "Doctor",
            "Date",
            "Time",
            "Status"
        ]
    )

    st.dataframe(df, use_container_width=True)

else:
    st.info("No appointments available.")    

st.divider()

st.subheader("🩺 Disease Distribution Overview")

disease_data = get_disease_statistics()

if disease_data:

    df = pd.DataFrame(
        disease_data,
        columns=["Disease", "Patients"]
    )

    st.bar_chart(df.set_index("Disease"))

else:
    st.info("No disease data available.")

st.divider()
st.subheader("📈 Revenue Analytics")

revenue_data = get_revenue_data()

if revenue_data:

    df = pd.DataFrame(
        revenue_data,
        columns=["Date", "Revenue"]
    )

    df = df.set_index("Date")

    st.line_chart(df)

else:
    st.info("No revenue available.")    