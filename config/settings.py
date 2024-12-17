import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB Configuration
MONGODB_URI = os.getenv("MONGODB_URI")

# Google AI Configuration
GOOGLE_API_KEY = os.getenv("API_KEY")

# Application directories
DIRECTORIES = {
    'input': r"Files\input_pdfs",
    'images': r"Files\extracted_images",
    'processed': r"Files\processed_cheques"
}

# Extraction prompt
EXTRACTION_PROMPT = """Extract the following details from each of the provided cheque images:
1. Bank name
2. Branch name
3. IFSC code
4. MICR code
5. Account number
6. Payee name
7. Date on cheque (DD/MM/YYYY format)
8. Amount in words
9. Amount figure

Return the details in a list of JSON objects, one for each image, with the following keys:
[
  {
    "Bank name": "",
    "Branch name": "",
    "IFSC code": "",
    "MICR code": "",
    "Account number": "",
    "Payee name": "",
    "Date": "",
    "Amount in words": "",
    "Amount figure": ""
  }
]"""