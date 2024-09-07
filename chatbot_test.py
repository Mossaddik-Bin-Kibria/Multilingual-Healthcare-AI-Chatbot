import openai
from PyPDF2 import PdfReader

# Initialize OpenAI API
openai.api_key = 'xxxxxxx'

def extract_text_from_pdf(pdf_file_path):
    pdf_reader = PdfReader(open(pdf_file_path, "rb"))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def split_text_into_chunks(text, chunk_size=3000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def summarize_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Please summarize the following text:\n\n{text}"}
        ],
        max_tokens=500  # Adjust as necessary to fit within limits
    )
    return response['choices'][0]['message']['content'].strip()

def summarize_pdf_text_in_chunks(pdf_text):
    chunks = split_text_into_chunks(pdf_text)
    summaries = []
    for chunk in chunks:
        summary = summarize_text(chunk)
        summaries.append(summary)
    return " ".join(summaries)

def chatbot_conversation():
    print("Welcome to the PDF Chatbot. Type 'exit' to end the conversation.")
    
    pdf_text = extract_text_from_pdf("/Users/moss_kibria/Projects/autogen/chatbot/clinical_medicine_ashok_chandra.pdf")
    
    # Summarize the PDF content in chunks
    pdf_summary = summarize_pdf_text_in_chunks(pdf_text)

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Goodbye!")
            break
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Based on the following summary of the PDF content:\n\n{pdf_summary}\n\nAnswer the following question:\n\n{user_input}"}
            ],
            max_tokens=150
        )
        
        print(f"Bot: {response['choices'][0]['message']['content'].strip()}")

# Start the conversation
chatbot_conversation()