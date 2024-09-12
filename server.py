from flask import Flask, request, jsonify
import base64
import os

app = Flask(__name__)

# Mengaktifkan CORS jika diperlukan
from flask_cors import CORS
CORS(app)

# Endpoint untuk menerima gambar base64 dan lokasi
@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Ambil data gambar base64 dan lokasi dari request
        data = request.json
        image = data.get('image')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # Hapus header 'data:image/png;base64,' dari string base64
        image_data = image.replace('data:image/png;base64,', '')

        # Konversi string base64 menjadi bytes
        image_bytes = base64.b64decode(image_data)

        # Tentukan direktori tempat menyimpan gambar
        upload_folder = 'uploads'
        
        # Membuat folder 'uploads' jika belum ada
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # Path lengkap untuk menyimpan gambar
        image_path = os.path.abspath(os.path.join(upload_folder, 'output.png'))

        # Simpan gambar ke file output.png di dalam folder 'uploads'
        with open(image_path, 'wb') as image_file:
            image_file.write(image_bytes)

        # Cek apakah file berhasil disimpan
        if os.path.exists(image_path):
            print(f"File saved successfully at {image_path}")
        else:
            print(f"Failed to save file at {image_path}")

        # Cetak lokasi yang diterima
        print(f"Image saved at {image_path}. Location: Latitude={latitude}, Longitude={longitude}")

        # Kembalikan respons sukses
        return jsonify({'message': 'Image and location received successfully'}), 200

    except Exception as e:
        # Tangani error dan kembalikan pesan error
        return jsonify({'error': str(e)}), 500

# Jalankan server Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
