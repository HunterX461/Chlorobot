document.addEventListener("DOMContentLoaded", () => {
    const characterVideo = document.getElementById('character-video');
    const chatCloud = document.getElementById('chat-cloud');
    const imageFileInput = document.getElementById('imageFile');
    const uploadBtn = document.getElementById('uploadBtn');
    const loadingAnimation = document.getElementById('loadingAnimation');
    const detectedObjectsDiv = document.getElementById('detectedObjectsCloud'); // Updated to match HTML
    const dropArea = document.getElementById('drop-area');
    const fileUploadText = document.getElementById('file-upload-text');
    const questionInput = document.getElementById('questionInput'); // New ID for the question input
    const askButton = document.getElementById('askButton'); // New ID for the ask button
    const responseDiv = document.getElementById('response'); // For displaying the chatbot response

    // Show chat cloud when character is clicked
    characterVideo.addEventListener('click', () => {
        chatCloud.classList.toggle('hidden');
    });

    // Handle file selection when clicking the upload text
    fileUploadText.addEventListener('click', () => {
        imageFileInput.click(); // Trigger file input click
    });

    // Handle image file selection
    imageFileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            dropArea.textContent = file.name; // Display the file name
        }
    });

    // Drag and drop functionality
    dropArea.addEventListener('dragover', (event) => {
        event.preventDefault(); // Prevent default to allow drop
        dropArea.classList.add('hover'); // Add hover effect
    });

    dropArea.addEventListener('dragleave', () => {
        dropArea.classList.remove('hover'); // Remove hover effect
    });

    dropArea.addEventListener('drop', (event) => {
        event.preventDefault(); // Prevent default behavior
        dropArea.classList.remove('hover'); // Remove hover effect
        const files = event.dataTransfer.files; // Get dropped files
        if (files.length > 0) {
            imageFileInput.files = files; // Assign files to input
            dropArea.textContent = files[0].name; // Display the file name
        }
    });

    // Handle image upload
    uploadBtn.addEventListener('click', async () => {
        const file = imageFileInput.files[0];
        if (!file) return alert('Please select an image');

        const formData = new FormData();
        formData.append('file', file);

        loadingAnimation.classList.remove('hidden');

        try {
            characterVideo.src = '/static/videos/thinking.mp4'; // Thinking animation

            const response = await fetch('/upload_image/', {
                method: 'POST',
                body: formData,
            });
            const data = await response.json();

            detectedObjectsDiv.textContent = 'Detected Objects: ' + data.objects_detected.join(', ');
            detectedObjectsDiv.classList.remove('hidden');

            // Adjust character video position after image upload
            characterVideo.style.bottom = '20%'; // Change the bottom position
            characterVideo.style.left = '10%';   // Change the left position

            characterVideo.src = '/static/videos/upload.mp4'; // Success animation
            loadingAnimation.classList.add('hidden');
        } catch (error) {
            detectedObjectsDiv.textContent = 'Error detecting objects';
            detectedObjectsDiv.classList.remove('hidden');
            loadingAnimation.classList.add('hidden');
        }
    });

    // Handle asking a question
    askButton.addEventListener('click', async () => {
        const question = questionInput.value.trim();
        if (!question) return alert('Please ask a question.');

        // Logic to send the question to the server and display the response
        try {
            const response = await fetch('/ask_question/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question }),
            });
            const data = await response.json();
            responseDiv.textContent = 'Response: ' + data.answer; // Update with the actual response structure
            responseDiv.classList.remove('hidden');
        } catch (error) {
            responseDiv.textContent = 'Error asking the question';
            responseDiv.classList.remove('hidden');
        }
    });
});
