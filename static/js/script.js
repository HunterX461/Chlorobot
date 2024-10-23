document.addEventListener("DOMContentLoaded", () => {
    const uploadForm = document.getElementById('uploadForm');
    const askBtn = document.getElementById('askBtn');

    // Upload image and get detected objects
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const fileInput = document.getElementById('imageFile').files[0];
        const formData = new FormData();
        formData.append('file', fileInput);

        try {
            const response = await fetch('/upload_image/', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            document.getElementById('detectedObjects').textContent = 'Detected Objects: ' + data.objects_detected.join(', ');
        } catch (error) {
            document.getElementById('detectedObjects').textContent = 'Error detecting objects';
        }
    });

    // Ask a question about detected objects
    askBtn.addEventListener('click', async () => {
        const objectsText = document.getElementById('detectedObjects').textContent;
        if (!objectsText.includes('Detected Objects:')) {
            document.getElementById('response').textContent = 'Please upload an image first!';
            return;
        }

        const objects = objectsText.split(': ')[1].split(', ');
        const question = document.getElementById('question').value;

        if (!question.trim()) {
            document.getElementById('response').textContent = 'Please enter a question!';
            return;
        }

        try {
            const response = await fetch('/ask_question/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question: question, objects: objects })
            });
            const data = await response.json();
            document.getElementById('response').textContent = 'Response: ' + data.response;
        } catch (error) {
            document.getElementById('response').textContent = 'Error getting response from chatbot';
        }
    });
});
