import os
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

from services import ChequeProcessor
from config import DIRECTORIES

def main_app():
    """Main application logic."""
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
    
    st.sidebar.markdown(f"### {st.session_state.username}!")
    
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()
    
    processor = ChequeProcessor()
    
    uploaded_file = st.file_uploader("Choose a PDF file...", type=["pdf"])
    
    if uploaded_file:
        pdf_path = os.path.join(DIRECTORIES['input'], uploaded_file.name)
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        
        if st.button("Process Cheques"):
            with st.spinner("Extracting and processing cheques..."):
                try:
                    image_paths = processor.extract_images_from_pdf(pdf_path)
                    
                    if not image_paths:
                        st.warning("No images found in the PDF.")
                        return
                    
                    # Process images
                    cheque_data_list = processor.process_cheque_images(image_paths, st.session_state.username)
                    st.success(f"Successfully processed {len(cheque_data_list)} cheques!")
                    
                except Exception as e:
                    st.error(f"Error processing PDF: {str(e)}")
    
    # Results section
    processed_data = processor.get_processed_data()
    if processed_data:
        st.markdown("### Processed Results")
        
        # Display as a table 
        df = pd.DataFrame(processed_data) 
        st.dataframe(df)
        
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
            
            if st.download_button( 
                label="Download CSV", 
                data=processor.export_data(st.session_state.username, 'csv'), 
                file_name="cheque_data.csv", 
                mime="text/csv" 
            ): 
                st.success("CSV file downloaded!")
                
        with col2:
            st.markdown(""" 
                <style> 
                    .stButton > button { 
                        width: 100%; 
                        text-align: left; 
                    } 
                </style> 
            """, unsafe_allow_html=True)
            
            if st.button("Clear All Data"):
                processor.cleanup(st.session_state.username)
                st.success("All data cleared!")
                st.rerun()
    
    # Footer
    components.html("""
        <style>
            .footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
                color: white;
                text-align: center;
                padding: 10px;
            }
        </style>
        <div class="footer">
            <p>By <b>Mohan Kumar Limbu</b></p>
        </div>
    """, height=100)