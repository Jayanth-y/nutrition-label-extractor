async function uploadImage() {
    const fileInput = document.getElementById("file-input").files[0];

    if (!fileInput) {
        alert("Please select an image");
        return;
    }

    // Get Elements
    const imagePreview = document.getElementById("image-preview");
    const imagePlaceholder = document.getElementById("image-placeholder");

    // Show Image Preview & Hide Placeholder
    const fileReader = new FileReader();
    fileReader.onload = function(event) {
        imagePreview.src = event.target.result;
        imagePreview.style.display = "block";
        imagePlaceholder.style.display = "none"; // Hide text
    };
    fileReader.readAsDataURL(fileInput);

    let formData = new FormData();
    formData.append("file", fileInput);

    try {
        let response = await fetch("https://nutrition-label-extractor-production.up.railway.app/extract", {
            method: "POST",
            mode: "cors",
            headers: {
                "Accept": "application/json"
            },
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        let data = await response.json();
        if (data.error) {
            alert("Error: " + data.error);
            return;
        }

        let outputDiv = document.getElementById("output");
        outputDiv.innerHTML = formatExtractedText(data.structured_data);
    } catch (error) {
        alert("Error processing image: " + error.message);
    }
}

// Order of Nutrition Labels (Same as regex patterns in backend)
const nutritionOrder = [
    "Serving Size", "Servings Per Container", "Calories",
    "Total Fat", "Saturated Fat", "Trans Fat", "Polyunsaturated Fat", "Monounsaturated Fat",
    "Cholesterol", "Sodium",
    "Total Carbohydrates", "Dietary Fiber", "Sugars", "Added Sugars",
    "Protein", "Vitamin D", "Calcium", "Iron", "Potassium",
    "Vitamin A", "Vitamin C", "Magnesium", "Zinc"
];

// Function to Format Extracted Data in Correct Order
function formatExtractedText(data) {
    let outputDiv = document.getElementById("output");
    let placeholderText = document.getElementById("extracted-text");

    if (!data || Object.keys(data).length === 0) {
        placeholderText.style.visibility = "visible";
        return "<p>No structured data found.</p>";
    }

    placeholderText.style.display = "none";

    let formattedText = "";
    for (const [key, value] of Object.entries(data)) {
        formattedText += `<p><strong>${key}:</strong> ${value}</p>`;
    }
    return formattedText;
}


// Improved Copy Function (No Alerts)
function copyText() {
    let text = document.getElementById("output").innerText;
    navigator.clipboard.writeText(text)
        .then(() => {
            let copyBtn = document.getElementById("copy-btn");
            copyBtn.innerHTML = "✔ Copied";
            setTimeout(() => {
                copyBtn.innerHTML = "Copy All";
            }, 1500);
        })
        .catch(err => console.error("🔴 Copy failed:", err));
}
