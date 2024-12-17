import streamlit as st
from database import DatabaseManager

def login_page():
    """Display the login page."""
    st.markdown("""
        <h1 style='text-align: center;
                color: clr-white-a0;
                font-size: 40px;
                width: 100%;
                background-color: clr-surface-a10;
                padding: 10px;
                margin-bottom: 10px'>
                Login
        </h1>
    """, unsafe_allow_html=True)
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
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
        if st.button("Login"):
            db_manager = DatabaseManager()
            if db_manager.verify_user(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.current_results = []
                db_manager.update_last_login(username)
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    with col2:
        st.markdown(""" 
            <style> 
                .stButton > button { 
                    width: 100%; 
                    text-align: right; 
                } 
            </style> 
        """, unsafe_allow_html=True)
        if st.button("Back"):
            st.session_state.page = 'home'
            st.rerun()
        