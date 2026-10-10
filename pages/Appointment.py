
import streamlit as st
from datetime import date

from utils.auth import require_login
from database.database import (
    add_appointment,
    get_appointments,
    update_appointment_status,
    get_public_appointment_requests,
    update_public_appointment_status,
    check_public_request_availability,
    confirm_public_request,
)

require_login(["Admin", "Reception"])

st.title("📅 Appointment Management")
st.caption("Review online requests and manage hospital appointments.")

# --------------------------------------------------
# CREATE A STAFF APPOINTMENT
# --------------------------------------------------
with st.expander("➕ Create a Hospital Appointment"):
    with st.form("appointment_form"):
        patient_id = st.number_input(
            "Registered Patient ID",
            min_value=1,
            step=1,
        )
        doctor_name = st.selectbox(
            "Select Doctor",
            ["Dr. Bilal", "Dr. Asif", "Dr. Aisha"],
        )
        appointment_date = st.date_input(
            "Appointment Date",
            min_value=date.today(),
        )
        appointment_time = st.time_input("Appointment Time")

        submitted = st.form_submit_button("Create Appointment")

    if submitted:
        try:
            add_appointment(
                int(patient_id),
                doctor_name,
                str(appointment_date),
                str(appointment_time),
                "Pending",
            )
            st.success("Appointment created successfully.")
            st.rerun()
        except Exception as e:
            st.error(f"Could not create appointment: {e}")


# --------------------------------------------------
# ONLINE APPOINTMENT REQUESTS
# --------------------------------------------------
st.divider()
st.subheader("🌐 Online Appointment Requests")
st.caption(
    "Check the requested doctor's availability before accepting. "
    "Patients can complete full registration when they arrive."
)

try:
    requests = get_public_appointment_requests()

    if not requests:
        st.info("No online appointment requests yet.")

    for request in requests:
        (
            request_id,
            patient_name,
            phone,
            email,
            doctor,
            appt_date,
            appt_time,
            reason,
            status,
        ) = request

        with st.container(border=True):
            st.markdown(f"### Request #{request_id}")

            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Patient:** {patient_name}")
                st.write(f"**Phone:** {phone}")
                st.write(f"**Email:** {email or 'Not provided'}")

            with col2:
                st.write(f"**Doctor:** {doctor}")
                st.write(f"**Requested date:** {appt_date}")
                st.write(f"**Requested time:** {appt_time}")

            st.write(f"**Reason:** {reason or 'Not provided'}")
            st.write(f"**Status:** {status}")

            if status == "Pending":
                if st.button(
                    "🔎 Check Doctor Availability",
                    key=f"check_{request_id}",
                    use_container_width=True,
                ):
                    try:
                        available, message = check_public_request_availability(
                            request_id
                        )
                        if available:
                            st.success(message)
                        else:
                            st.warning(message)
                    except Exception as e:
                        st.error(f"Availability check failed: {e}")

                confirm_col, reject_col = st.columns(2)

                with confirm_col:
                    if st.button(
                        "✅ Accept Request",
                        key=f"accept_{request_id}",
                        type="primary",
                        use_container_width=True,
                    ):
                        try:
                            appointment_id = confirm_public_request(request_id)
                            st.success(
                                f"Request accepted! Appointment ID: "
                                f"{appointment_id}. Patient registration "
                                "can be completed at the hospital."
                            )
                            st.rerun()
                        except ValueError as e:
                            st.warning(str(e))
                        except Exception as e:
                            st.error(f"Could not accept request: {e}")

                with reject_col:
                    with st.popover("❌ Reject Request"):
                        rejection_reason = st.text_area(
                            "Reason (optional)",
                            key=f"reason_{request_id}",
                        )
                        if st.button(
                            "Confirm Rejection",
                            key=f"reject_{request_id}",
                            use_container_width=True,
                        ):
                            try:
                                update_public_appointment_status(
                                    request_id,
                                    "Rejected",
                                )
                                st.success("Request rejected.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Could not reject request: {e}")

            elif status == "Confirmed":
                st.success(
                    "Accepted. The patient can visit on the scheduled date "
                    "and complete registration at reception."
                )

            elif status == "Rejected":
                st.warning("This request was rejected.")

except Exception as e:
    st.error(f"Could not load online appointment requests: {e}")


# --------------------------------------------------
# HOSPITAL APPOINTMENTS
# --------------------------------------------------
st.divider()
st.subheader("📋 Hospital Appointments")

try:
    appointments = get_appointments()

    if not appointments:
        st.info("No hospital appointments yet.")

    for appointment in appointments:
        (
            appointment_id,
            patient_id,
            doctor,
            appt_date,
            appt_time,
            status,
        ) = appointment

        with st.container(border=True):
            st.write(f"**Appointment ID:** {appointment_id}")
            st.write(
                f"**Patient ID:** "
                f"{patient_id if patient_id is not None else 'Registration pending'}"
            )
            st.write(f"**Doctor:** {doctor}")
            st.write(f"**Date:** {appt_date} | **Time:** {appt_time}")
            st.write(f"**Status:** {status}")

            if status == "Pending":
                col1, col2 = st.columns(2)

                with col1:
                    if st.button(
                        "Confirm",
                        key=f"confirm_staff_{appointment_id}",
                    ):
                        try:
                            update_appointment_status(
                                appointment_id, "Confirmed"
                            )
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))

                with col2:
                    if st.button(
                        "Reject",
                        key=f"reject_staff_{appointment_id}",
                    ):
                        try:
                            update_appointment_status(
                                appointment_id, "Rejected"
                            )
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))

except Exception as e:
    st.error(f"Could not load hospital appointments: {e}")
