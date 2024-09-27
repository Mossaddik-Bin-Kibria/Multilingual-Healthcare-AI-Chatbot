let chatHistory = [];

document.getElementById('send-button').addEventListener('click', sendMessage);

function sendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();
    if (message === '') return;

    displayMessage(message, 'user-message');
    userInput.value = '';

    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message, history: chatHistory })
    })
    .then(response => response.json())
    .then(data => {
        displayMessage(data.response, 'assistant-message');
        chatHistory.push({ 'role': 'user', 'content': message });
        chatHistory.push({ 'role': 'assistant', 'content': data.response });
    });
}

function displayMessage(message, className) {
    const chatWindow = document.getElementById('chat-window');
    const messageElem = document.createElement('div');
    messageElem.className = `message ${className}`;
    messageElem.textContent = message;
    chatWindow.appendChild(messageElem);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function displayUploadedFile(file, type) {
  const uploadedFilesList = document.getElementById('uploaded-files-list');
  const fileElem = document.createElement('div');
  fileElem.className = 'uploaded-file';

  if (type === 'image') {
      const img = document.createElement('img');
      img.src = URL.createObjectURL(file);
      img.onload = function() {
          URL.revokeObjectURL(img.src); // Free memory
      };
      img.className = 'uploaded-image';
      fileElem.appendChild(img);
  } else if (type === 'document') {
      const link = document.createElement('span');
      link.textContent = file.name;
      fileElem.appendChild(link);
  }

  uploadedFilesList.appendChild(fileElem);
}

// Upload Document
document.getElementById('upload-document-button').addEventListener('click', () => {
    const fileInput = document.getElementById('document-input');
    const file = fileInput.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload_document', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
      alert(data.message);
      // Display the uploaded document
      displayUploadedFile(file, 'document');
  });
});

// Upload Image
document.getElementById('upload-image-button').addEventListener('click', () => {
    const fileInput = document.getElementById('image-input');
    const file = fileInput.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload_image', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
      // Display the extracted text in the chat window
      displayMessage('Extracted Text: ' + data.extracted_text, 'assistant-message');
      // Display the uploaded image
      displayUploadedFile(file, 'image');
  });
    
});
