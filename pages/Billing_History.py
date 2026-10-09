import streamlit as st
from utils.auth import require_login

require_login(["Admin", "Reception"])
import pandas as pd

from database.database import get_all_bills

bills = get_all_bills()

if bills:

    df = pd.DataFrame(
        bills,
        columns=[
            "Bill ID",
            "Patient ID",
            "Consultation Fee",
            "Lab Fee",
            "Medicine Fee",
            "Total Amount",
            "Payment Status",
            "Billing Date"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:
    
    st.info("No bills generated yet.")