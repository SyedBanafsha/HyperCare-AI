import streamlit as st
from database.database import search_patient
st.title("🔍 Patient Search")
st.caption("Search patient records using the unique Patient ID.")
patient_id = st.number_input("Enter Patient ID", min_value=1)

search = st.button("Search")
if search:
    patient = search_patient(patient_id)
    if patient:
        st.success("✅ Patient Found Successfully!")
        st.subheader("👤 Patient Information")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Patient ID:**", patient[0])
            st.write("**Patient Name:**", patient[1])
            st.write("**Phone Number:**", patient[2])
            st.write("**Age:**", patient[3])

        with col2:
            st.write("**Gender:**", patient[4])
            st.write("**Residence:**", patient[5])
            st.write("**Purpose of Visit:**", patient[6])
            st.write("**Current Symptoms:**", patient[7])
    else:
        st.error("❌ Patient ID not found.")

