import re
import os
import json
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from google.cloud import vision
from google.oauth2 import service_account

class OCRService:
    """Handles OCR extraction using Google Vision API and regex-based data extraction."""

    def __init__(self):
        # Load credentials from Railway environment variable
        credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")

        if credentials_json:
            credentials_dict = json.loads(credentials_json)  # Convert JSON string to dictionary

            # Write the JSON to a file in the /app directory
            credentials_path = "/app/service-account.json"
            with open(credentials_path, "w") as f:
                json.dump(credentials_dict, f)
        
            # Set environment variable for Google to find the file
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        
            # Load Google Cloud Vision API client
            credentials = service_account.Credentials.from_service_account_file(credentials_path)
            client = vision.ImageAnnotatorClient(credentials=credentials)
        else:
            raise ValueError("Missing GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable")
        
        self.client = vision.ImageAnnotatorClient()
        self.patterns = {
            "Calories": r"(?i)\b(?:Calories|Cal|Energy)\s*[:]?[\s]*([\d]+)[\s]*(?:kcal)?\b",
            "Serving Size": r"(?i)\bServing Size\s*[:]?[\s]*([\d]+(?:\s?[a-zA-Z]+)?(?:\s?\([\d]+[a-zA-Z]*\))?)",
            "Servings Per Container": r"(?i)\bServings Per Container\s*[:]?[\s]*([\d]+)",

            # Fat Content
            "Total Fat": r"Total Fat[\s]*[:]?[\s]*([\d]+g)",
            "Saturated Fat": r"Saturated Fat[\s]*[:]?[\s]*([\d]+g)",
            "Trans Fat": r"Trans Fat[\s]*[:]?[\s]*([\d]+g)",
            "Polyunsaturated Fat": r"Polyunsaturated Fat[\s]*[:]?[\s]*([\d]+g)",
            "Monounsaturated Fat": r"Monounsaturated Fat[\s]*[:]?[\s]*([\d]+g)",

            # Cholesterol & Sodium
            "Cholesterol": r"Cholesterol[\s]*[:]?[\s]*([\d]+mg)",
            "Sodium": r"Sodium[\s]*[:]?[\s]*([\d]+mg)",

            # Carbohydrates & Fiber
            "Total Carbohydrates": r"Total Carbohydrate[\s]*[:]?[\s]*([\d]+g)",
            "Dietary Fiber": r"Dietary Fiber[\s]*[:]?[\s]*([\d]+g)",
            "Sugars": r"Sugars[\s]*[:]?[\s]*([\d]+g)",
            "Added Sugars": r"Added Sugars[\s]*[:]?[\s]*([\d]+g)",

            # Protein & Vitamins
            "Protein": r"Protein[\s]*[:]?[\s]*([\d]+g)",
            "Vitamin D": r"Vitamin D[\s]*[:]?[\s]*([\d]+mcg)",
            "Calcium": r"Calcium[\s]*[:]?[\s]*([\d]+mg)",
            "Iron": r"Iron[\s]*[:]?[\s]*([\d]+mg)",
            "Potassium": r"Potassium[\s]*[:]?[\s]*([\d]+mg)",

            # Additional Nutrients (Optional)
            "Vitamin A": r"Vitamin A[\s]*[:]?[\s]*([\d]+mcg)",
            "Vitamin C": r"Vitamin C[\s]*[:]?[\s]*([\d]+mg)",
            "Magnesium": r"Magnesium[\s]*[:]?[\s]*([\d]+mg)"
        }

    def extract_text(self, image_bytes: bytes) -> str:
        """Extracts text from the image using Google Vision API."""
        image = vision.Image(content=image_bytes)
        response = self.client.document_text_detection(image=image)

        if response.error.message:
            raise RuntimeError(f"Google Vision API Error: {response.error.message}")

        return response.full_text_annotation.text if response.full_text_annotation.text else "No text detected."

    def extract_nutrition_data(self, text: str) -> dict:
        """Extracts structured nutrition data using regex patterns."""
        extracted_data = {}
        for label, pattern in self.patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                extracted_data[label] = match.group(1)

        return extracted_data


# FastAPI App Initialization
app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

ocr_service = OCRService()

@app.post("/extract")
async def extract_text_from_image(file: UploadFile = File(...)):
    """Handles image uploads and extracts text from nutrition labels."""
    try:
        print("🟢 Image received for processing.")
        image_content = await file.read()
        if not image_content:
            return JSONResponse(content={"error": "Empty file received."}, status_code=400)

        # Send to Google Vision API for text extraction
        extracted_text = ocr_service.extract_text(image_content)
        structured_data = ocr_service.extract_nutrition_data(extracted_text)

        print(f"🟢 Extracted Structured Data:\n{structured_data}")

        return JSONResponse(content={"raw_ocr_text": extracted_text, "structured_data": structured_data})

    except RuntimeError as re:
        print(f"🔴 API Error: {re}")
        return JSONResponse(content={"error": str(re)}, status_code=500)

    except Exception as e:
        print(f"🔴 Unexpected Error: {e}")
        return JSONResponse(content={"error": f"Internal Server Error: {str(e)}"}, status_code=500)
