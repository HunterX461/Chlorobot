document.addEventListener("DOMContentLoaded", () => {
    const characterVideo = document.getElementById('character-video');
    const chatCloud = document.getElementById('chat-cloud');
    const imageFileInput = document.getElementById('imageFile');
    const uploadBtn = document.getElementById('uploadBtn');
    const detectedObjectsDiv = document.getElementById('detectedObjects');

// Show chat cloud when character is clicked
characterVideo.addEventListener('click', () => {
    chatCloud.classList.toggle('hidden');
    console.log("Chat cloud visibility toggled. Current state:", chatCloud.classList.contains('hidden') ? 'Hidden' : 'Visible');
});

    // Handle image upload
    uploadBtn.addEventListener('click', async () => {
        const file = imageFileInput.files[0];
        if (!file) {
            alert('Please select an image');
            return; // Early exit if no file is selected
        }

        const formData = new FormData();
        formData.append('file', file);

        console.log("Image upload initiated."); // Log image upload initiation

        try {
            // You may want to show a loading animation here
            const response = await fetch('/upload_image/', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            detectedObjectsDiv.textContent = 'Detected Objects: ' + data.objects_detected.join(', ');
            console.log("Response received:", data); // Log the response data

        } catch (error) {
            console.error("Error during image upload:", error); // Log any error
            detectedObjectsDiv.textContent = 'Error detecting objects';
        }
    });
});
