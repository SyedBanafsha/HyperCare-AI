
import streamlit as st


def is_logged_in():
    return st.session_state.get("logged_in", False)


def require_login(allowed_roles=None):
    if not is_logged_in():
        st.title("🔐 HyperCare AI Login")
        st.info("Please log in from the Home page.")
        st.stop()

    if allowed_roles is not None:
        user_role = st.session_state.get("role")

        if user_role not in allowed_roles:
            st.error("Access denied. You do not have permission to view this page.")
            st.stop()


def logout():
    for key in ("logged_in", "role", "username"):
        st.session_state.pop(key, None)

    st.rerun()
