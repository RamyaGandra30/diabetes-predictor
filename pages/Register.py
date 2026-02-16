import streamlit as st
from utils.auth import register_user

st.set_page_config(page_title="Register")

st.title("📝 Create Account")

username = st.text_input("Username")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Register"):
    if username and email and password:
        if register_user(username, email, password):
            st.success("Account created successfully!")
            st.switch_page("pages/Login.py")
        else:
            st.error("Username already exists!")
    else:
        st.warning("Please fill all fields.")

st.markdown("---")
if st.button("Back to Login"):
    st.switch_page("pages/Login.py")
