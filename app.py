from flask import Flask, render_template, request, jsonify, session
import openai
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image
from PyPDF2 import PdfReader
import docx
from PIL import ImageEnhance, ImageFilter

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Set the Flask app's secret key for session management
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')  # Use environment variable or default

# Set your Azure OpenAI credentials
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_API_BASE")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

# Ensure 'uploads' directory exists for saving uploaded files
if not os.path.exists('uploads'):
    os.makedirs('uploads')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    chat_history = request.json.get('history', [])

    # System message to guide the assistant's behavior
    messages = [{"role": "system", "content": "You are a helpful assistant."}] + chat_history

    # Include document content if available in the session
    document_text = session.get('document_text')
    if document_text:
        # Append the document text to the system message to give the LLM context
        messages.append({"role": "system", "content": f"The following document has been uploaded: {document_text[:1500]}..."})

    messages.append({"role": "user", "content": user_message})

    try:
        # Call the Azure OpenAI API to get a response
        response = openai.ChatCompletion.create(
            engine=deployment_name,
            messages=messages
        )

        # Get the assistant's message from the response
        assistant_message = response['choices'][0]['message']['content']
        return jsonify({'response': assistant_message})

    except openai.error.OpenAIError as e:
        # Log and handle errors gracefully
        print(f"OpenAI API error: {e}")
        return jsonify({'response': "Sorry, I'm having trouble accessing the AI service right now."}), 500


@app.route('/upload_document', methods=['POST'])
def upload_document():
    file = request.files['file']
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    # Save the uploaded document
    filename = secure_filename(file.filename)
    filepath = os.path.join('uploads', filename)
    file.save(filepath)

    # Extract text from the document based on its type
    extracted_text = ''
    if filename.lower().endswith('.pdf'):
        reader = PdfReader(filepath)
        for page in reader.pages:
            extracted_text += page.extract_text()
    elif filename.lower().endswith('.docx'):
        doc = docx.Document(filepath)
        for para in doc.paragraphs:
            extracted_text += para.text + '\n'
    else:
        return jsonify({'error': 'Unsupported file type'}), 400

    # Optionally, remove the uploaded file after processing
    os.remove(filepath)

    # Store the extracted text in the session for later use
    session['document_text'] = extracted_text

    return jsonify({'message': f'Document "{file.filename}" uploaded and processed successfully.'})


@app.route('/upload_image', methods=['POST'])
def upload_image():
    file = request.files['file']
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    # Save the uploaded image file
    filename = secure_filename(file.filename)
    filepath = os.path.join('uploads', filename)
    file.save(filepath)

    # Open the image using PIL
    img = Image.open(filepath)

    # Preprocess the image: convert to grayscale, enhance contrast, etc.
    img = img.convert('L')  # Convert to grayscale
    img = ImageEnhance.Contrast(img).enhance(2)  # Increase contrast
    img = img.filter(ImageFilter.SHARPEN)  # Sharpen the image

    # Perform OCR using pytesseract
    extracted_text = pytesseract.image_to_string(img)

    # Optionally, delete the file after processing
    os.remove(filepath)

    # Check if extracted text is empty and handle it
    if not extracted_text.strip():
        return jsonify({'extracted_text': 'No text could be extracted from the image.'})
    
    # Return the extracted text
    return jsonify({'extracted_text': extracted_text})


if __name__ == '__main__':
    app.run(debug=True)
