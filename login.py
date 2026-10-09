
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

    username = st.text_input("Username", key="login_username")
    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.button("Login"):
        user = USERS.get(username.strip().lower())

        if user and user["password"] == password:
            st.session_state["logged_in"] = True
            st.session_state["role"] = user["role"]
            st.session_state["username"] = username.strip().lower()

            st.success("Login Successful!")
            st.rerun()
        else:
            st.error("Invalid Username or Password")


if __name__ == "__main__":
    login()
