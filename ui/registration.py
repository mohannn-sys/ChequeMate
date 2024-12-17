import streamlit as st
from database import DatabaseManager
from services import validate_password, validate_email

def registration_page():
    """Display the registration page."""
    st.markdown("""
        <h1 style='text-align: center;
                color: clr-white-a0;
                font-size: 40px;
                width: 100%;
                background-color: clr-surface-a10;
                padding: 10px;
                margin-bottom: 10px'>
                Register
        </h1>
    """, unsafe_allow_html=True)
    
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(""" 
            <style> 
                .stButton > button { 
                    width: 100%; 
                    text-align: left; 
                } 
            </style> 
        """, unsafe_allow_html=True)
        
        if st.button("Register", key='btn-register'):
            if not all([username, email, password, confirm_password]):
                st.error("All fields are required")
                return
                
            if not validate_email(email):
                st.error("Invalid email format")
                return
                
            is_valid_password, password_message = validate_password(password)
            if not is_valid_password:
                st.error(password_message)
                return
                
            if password != confirm_password:
                st.error("Passwords do not match")
                return
                
            db_manager = DatabaseManager()
            if db_manager.create_user(username, password, email):
                st.success("Registration successful! Please login.")
                st.session_state.page = 'login'
                st.rerun()
            else:
                st.error("Username already exists")
    
    
    with col2:
        st.markdown("""
            <style>
                .stButton > button { 
                    width: 100%; 
                    text-align: right; 
                } 
            </style>
        """, unsafe_allow_html=True)
        
        if st.button("Back", key='btn-back'):
            st.session_state.page = 'home'
            st.rerun()
        