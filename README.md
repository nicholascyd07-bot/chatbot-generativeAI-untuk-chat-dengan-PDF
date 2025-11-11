# Chatbot dengan Google Generative AI

## Cara menjalankan kode

Untuk menginstal dan menjalankan kode, berikut petunjuknya:

1. Unduh folder (zip atau github)

2. Masuk ke direktori chatbot genai:

```(CMD)
cd "genai analisa gambar chatbot"
```

3. Buat lingkungan virtual:

```
python -m venv venv
```

4. Aktifkan lingkungan virtual baru:

```
venv\Scripts\activate.bat
```

5. Instal paket yang diperlukan (perintah upgrade pip terlebih dahulu):

```
python -m pip install --upgrade pip
python.exe -m pip install -r requirements.txt
```

6. Dapatkan Kunci API GOOGLE Anda

7. Buka file `.py` di root direktori repositori, lalu ganti `<your-api-key>` dengan kunci API Anda yang sebenarnya

```
GOOGLE_API_KEY=<your-api-key>
```

8. Jalankan aplikasi:

```
python ""
```

## Alat dan Pustaka (Paket) yang digunakan
google
google-generativeai

## Penggunaan

Setelah aplikasi berjalan, Anda dapat mengobrol dengan Google Generative AI di konsol atau CMD Anda