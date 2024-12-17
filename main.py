import streamlit as st
from ui import login_page, registration_page, main_app, home_page

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'username' not in st.session_state:
    st.session_state.username = None
if 'current_results' not in st.session_state:
    st.session_state.current_results = []

def main():
    """Main function to handle authentication and app flow."""
    if not st.session_state.authenticated:
        if st.session_state.page == 'home':
            home_page()
        elif st.session_state.page == 'registration':
            registration_page()
        elif st.session_state.page == 'login':
            login_page()
    else:
        main_app()
        
    # Clear results on logout
    if st.session_state.get('authenticated') == False:
        if 'current_results' in st.session_state:
            st.session_state.current_results = []

if __name__ == "__main__":
    main()