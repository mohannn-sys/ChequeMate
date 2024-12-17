import streamlit as st 

def home_page():
    """Display the home page with navigation options."""
    st.markdown("""
        <h1 style='text-align: center;
                color: clr-white-a0;
                font-size: 30px;
                width: 100%;
                background-color: clr-surface-a10;
                padding: 10px;
                margin-bottom: 10px'>
                CheckMate: Automated Bank Check Processor
        </h1>
    """, unsafe_allow_html=True)
    
    # Add some descriptive text
    st.markdown("""
        <p style='text-align: center;
                color: clr-white-a0;
                font-size: 15px;
                width: 100%;
                background-color: clr-surface-a10;
                padding: 10px;
                margin-bottom: 10px'>
                Easily extract detailed information from PDF files containing cheque images, including: Bank name, IFSC code, Account number,...
        </p>
    """, unsafe_allow_html=True)

    
    # Create centered columns for buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div style='display: flex; flex-direction: column; gap: 20px; align-items: center;'>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Login", use_container_width=True):
            st.session_state.page = 'login'
            st.rerun()
            
        if st.button("Register", use_container_width=True):
            st.session_state.page = 'registration'
            st.rerun()
    
    # Add footer
    st.markdown("""
        <div style='position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; padding: 10px;'>
            <p>By <b>Mohan Kumar Limbu</b></p>
        </div>
    """, unsafe_allow_html=True)