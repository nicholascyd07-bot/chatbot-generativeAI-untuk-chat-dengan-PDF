import os
import PyPDF2 # Import for PDF processing

import os

# Use environment variables or direct assignment for API keys

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', 'AIzaSyB7rUAZYwKrN2rYFAJmyhtj0jQra8xoqhM')
# Replace 'YOUR_API_KEY_HERE' with your actual API key if not using environment variables

import google.generativeai as genai
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini API
try:
    gemini_model = genai.GenerativeModel('gemini-2.5-flash') # Or the model you successfully initialized
except NameError:
    print("Gemini model not initialized. Please run the API initialization cells.")

print("Mulai percakapan dengan AI (ketik '/exit' atau '/quit' untuk keluar):")
chat = gemini_model.start_chat(history=[])

# Variable to store extracted audio path, initialized outside the loop
# This allows it to persist and be deleted only at the very end
global_extracted_audio_path = None

while True:
    user_text_input = input("Anda: ")
    print("User : "+ user_text_input)        
    if user_text_input.lower() in ['/exit', '/quit']:
        print("Percakapan selesai.")
        # Clean up temporary audio file if it was created and still exists
        if global_extracted_audio_path and os.path.exists(global_extracted_audio_path):
            try:
                os.remove(global_extracted_audio_path)
                print(f"Temporary audio file '{global_extracted_audio_path}' dihapus.")
            except Exception as e:
                print(f"Error menghapus temporary audio file: {e}")
        break

    prompt_parts = [user_text_input]
    pdf_texts_to_send = []

    # --- PDF Processing ---
    add_pdfs_str = input("Apakah Anda ingin menyertakan file PDF? (ya/tidak): ").lower()
    if add_pdfs_str == 'ya':
        # Modify the initial user query to explicitly ask for PDF text analysis
        # This ensures the model immediately understands the intent.
        original_user_query = prompt_parts[0]
        prompt_parts[0] = f"Mohon analisis teks dari dokumen PDF yang saya ekstrak. {original_user_query.strip()}"

        while True:
            pdf_dir_input = input("Masukkan nama folder PDF (misal: 'file pdf'): ")
            pdf_filename_input = input("Masukkan nama file PDF (misal: 'SuratKeterangan.pdf'): ")

            current_pdf_path = os.path.join(pdf_dir_input.strip(), pdf_filename_input.strip())
            if os.path.exists(current_pdf_path):
                try:
                    print(f"Memproses PDF '{pdf_filename_input}' dari '{pdf_dir_input}'...")
                    pdf_reader = PyPDF2.PdfReader(current_pdf_path)
                    extracted_text = ""
                    for page in pdf_reader.pages:
                        extracted_text += page.extract_text() + "\n"
                    
                    # Modified phrasing to explicitly state that the text has been extracted and is provided for analysis.
                    pdf_texts_to_send.append(f"Saya telah mengekstrak teks dari dokumen PDF '{pdf_filename_input}'. Berikut adalah isi teksnya untuk Anda analisis:\n{extracted_text}")
                    print(f"Teks dari PDF '{pdf_filename_input}' berhasil diekstrak.")

                except Exception as e:
                    print(f"Terjadi kesalahan saat memproses PDF '{pdf_filename_input}': {e}")
            else:
                print(f"File PDF tidak ditemukan di: {current_pdf_path}. Harap periksa kembali path dan nama file.")

            add_more_pdfs = input("Tambahkan PDF lain? (ya/tidak): ").lower()
            if add_more_pdfs != 'ya':
                break

    # Combine all parts of the prompt
    if pdf_texts_to_send:
        prompt_parts.extend(pdf_texts_to_send)

    try:
        print("=====================================================Jawaban AI=============================================================")
        response = chat.send_message(prompt_parts)
        print("AI:          ", response.text)
    except Exception as e:
        print(f"Terjadi kesalahan saat mengirim pesan ke model Gemini: {e}")