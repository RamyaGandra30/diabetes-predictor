import streamlit as st

st.set_page_config(page_title="Diabetes App", initial_sidebar_state="collapsed")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Automatic routing
if not st.session_state.logged_in:
    st.switch_page("pages/Login.py")
else:
    st.title("Welcome to Diabetes Predictor app")
    if st.button("Go to Diabetes predictior"):
        #st.switch_page("pages/Register.py")
        st.switch_page("pages/Diabetes_Predictor.py")
