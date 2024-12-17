import os
import json
import shutil
import streamlit as st
from typing import Dict, List
from PIL import Image
import fitz
import google.generativeai as genai
import pandas as pd

from config import GOOGLE_API_KEY, DIRECTORIES, EXTRACTION_PROMPT
from database import DatabaseManager

class ChequeProcessor:
    def __init__(self):
        """Initialize the ChequeProcessor."""
        self.setup_genai()
        self.initialize_directories()
        self.db_manager = DatabaseManager()
        
    def setup_genai(self):
        """Initialize the Gemini AI model."""
        if not GOOGLE_API_KEY:
            raise ValueError("API_KEY not found in environment variables")
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        
    def initialize_directories(self):
        """Create necessary directories if they don't exist."""
        for directory in DIRECTORIES.values():
            os.makedirs(directory, exist_ok=True)
            
    def extract_images_from_pdf(self, pdf_path: str) -> List[str]:
        """Extract images from PDF and save them."""
        saved_images = []
        xrefs_set = set()
        image_counter = 1

        try:
            pdf_document = fitz.open(pdf_path)
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                image_list = page.get_images()

                for img in image_list:
                    xref = img[0]
                    if xref in xrefs_set:
                        continue

                    xrefs_set.add(xref)
                    base_image = pdf_document.extract_image(xref)
                    image_bytes = base_image["image"]

                    image_filename = f"image_{image_counter:03d}.png"
                    image_path = os.path.join(DIRECTORIES['images'], image_filename)

                    with open(image_path, "wb") as img_file:
                        img_file.write(image_bytes)

                    saved_images.append(image_path)
                    image_counter += 1

            return saved_images

        except Exception as e:
            raise ValueError(f"Error processing PDF: {str(e)}")
        finally:
            if 'pdf_document' in locals():
                pdf_document.close()
    
    def process_cheque_images(self, image_paths: List[str], username: str) -> List[Dict]:
        """Process multiple cheque images and extract data."""
        try:
            images = [Image.open(path) for path in image_paths]
            response = self.model.generate_content([EXTRACTION_PROMPT] + images)
            cheque_data_list = json.loads(response.text.strip(" ```json"))
        except (json.JSONDecodeError, Exception) as e:
            raise ValueError(f"Failed to process images: {str(e)}")
        
        for data, path in zip(cheque_data_list, image_paths):
            data["Image_path"] = path
            
        self.db_manager.save_cheque_data(cheque_data_list, username)
        st.session_state.current_results = cheque_data_list
        return cheque_data_list
    
    def get_processed_data(self) -> List[Dict]:
        """Retrieve processed cheque data for the current session."""
        return st.session_state.current_results
    
    def export_data(self, username: str, format: str) -> bytes:
        """Export processed data in specified format."""
        data = self.get_processed_data()
        if format == 'csv':
            df = pd.DataFrame(data)
            return df.to_csv(index=False).encode('utf-8')
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def cleanup(self, username: str):
        """Clean up data and reset state."""
        self.db_manager.clear_user_data(username)
        st.session_state.current_results = []