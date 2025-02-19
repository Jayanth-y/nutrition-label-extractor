🚀 Nutrition Label Extractor
🔗 Live Demo: Nutrition Label Extractor [https://jayanth-y.github.io/nutrition-label-extractor/]
To run this project, simply visit the link above. No installation required!

📌 Overview
Nutrition Label Extractor is a web-based application that allows users to extract nutritional information from food labels using Google Vision API. 
This project leverages FastAPI for backend processing and a modern, responsive frontend to provide a seamless user experience.

✅ Upload a nutrition label image
✅ Extract key nutrition values (Calories, Protein, Fats, Carbs, Vitamins, etc.)
✅ Copy extracted data easily
✅ Fully responsive & mobile-friendly

⚡ Features
✔ AI-Powered OCR Processing – Uses Google Vision API to extract text.
✔ REST API for Developers – Backend supports API requests for integration.
✔ Copy & Share Functionality – One-click "Copy All" button.
✔ Modern, Dark-Themed UI – Aesthetic and user-friendly design.
✔ Deployed on Railway & GitHub Pages – Fast, free, and cloud-based.

🛠️ Technologies Used
Frontend: HTML, CSS, JavaScript
Backend: FastAPI (Python), Uvicorn
Cloud Services: Google Vision API (OCR)
Deployment: Railway (Backend) + GitHub Pages (Frontend)

🚀 How It Works
1️⃣ Upload an image of a nutrition label.
2️⃣ Google Vision API processes the image and extracts text.
3️⃣ Regex-based text processing structures the extracted data.
4️⃣ Extracted data is displayed in a clean, formatted output.
5️⃣ Click "Copy All" to copy extracted values for easy sharing.

Response (JSON) : 
{
    "Calories": "200",
    "Total Fat": "8g",
    "Sodium": "160mg",
    "Protein": "5g"
}

📦 Installation (For Local Development)
If you want to run this project locally:
1️⃣ Clone the Repository:
    git clone https://github.com/jayanth-y/nutrition-label-extractor.git
    cd nutrition-label-extractor
2️⃣ Setup Backend (FastAPI)
    cd backend
    pip install -r requirements.txt
    uvicorn main:app --host 0.0.0.0 --port 8080
    API will be available at: http://127.0.0.1:8080
3️⃣ Setup Frontend
    Simply open index.html in a browser or use Live Server in VS Code.

