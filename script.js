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
        let response = await fetch("http://127.0.0.1:8000/extract", {
            method: "POST",
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
    "Calories", "Serving Size", "Servings Per Container",
    "Total Fat", "Saturated Fat", "Trans Fat", "Polyunsaturated Fat", "Monounsaturated Fat",
    "Cholesterol", "Sodium",
    "Total Carbohydrates", "Dietary Fiber", "Sugars", "Added Sugars",
    "Protein", "Vitamin D", "Calcium", "Iron", "Potassium",
    "Vitamin A", "Vitamin C", "Magnesium"
];

// Function to Format Extracted Data in Correct Order
function formatExtractedText(data) {
    if (!data || Object.keys(data).length === 0) {
        return "<p>No structured data found.</p>";
    }

    let formattedText = "";
    for (const key of nutritionOrder) {
        if (data[key]) {  // Only print if data exists
            formattedText += `<p><strong>${key}:</strong> ${data[key]}</p>`;
        }
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
