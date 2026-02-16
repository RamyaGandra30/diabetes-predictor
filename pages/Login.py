import streamlit as st
from utils.auth import login_user

st.set_page_config(page_title="Login")

st.title("🔐 Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    user = login_user(username, password)
    
    if user:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.success("Login successful!")
        st.switch_page("pages/Diabetes_Predictor.py")
    else:
        st.error("Invalid credentials")

st.markdown("---")
st.write("Don't have an account?")
if st.button("Go to Register"):
    st.switch_page("pages/Register.py")
