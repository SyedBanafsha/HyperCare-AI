import streamlit as st

USERS = {
    "admin": {
        "password": "admin123",
        "role": "Admin"
    },
    "doctor": {
        "password": "doctor123",
        "role": "Doctor"
    },
    "lab": {
        "password": "lab123",
        "role": "Lab Technician"
    },
    "reception": {
        "password": "reception123",
        "role": "Reception"
    }
}


def login():

    st.title("🔐 HyperCare AI Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if username in USERS and USERS[username]["password"] == password:

            st.session_state.logged_in = True
            st.session_state.role = USERS[username]["role"]

            st.success("Login Successful!")

            st.rerun()

        else:
            st.error("Invalid Username or Password")