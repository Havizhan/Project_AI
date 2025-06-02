# Sistem Prediksi Hasil Panen Padi Kabupaten Semarang

Aplikasi ini menggunakan metode Fuzzy Tsukamoto untuk memprediksi hasil panen padi di kabupaten Semarang berdasarkan parameter luas lahan, curah hujan, dan tinggi wilayah.

## Daftar Isi
- [Deskripsi](#deskripsi)
- [Cara Instalasi](#cara-instalasi)
- [Cara Penggunaan](#cara-penggunaan)
- [Struktur Aplikasi](#struktur-aplikasi)

## Deskripsi
Aplikasi ini mengimplementasikan metode Fuzzy Tsukamoto untuk memprediksi hasil panen padi di berbagai kecamatan di Kabupaten Semarang. Metode ini menggunakan tiga variabel input yaitu luas lahan, curah hujan, dan tinggi wilayah untuk menghitung prediksi hasil panen padi dalam ton.

## Cara Instalasi

1. Pastikan Python versi 3.7 atau lebih baru sudah terinstal di komputer Anda
2. Clone repositori ini ke komputer Anda
3. Buat virtual environment (opsional tetapi direkomendasikan):
   ```
   python -m venv venv
   ```
4. Aktifkan virtual environment:
   - Windows:
   ```
   venv\Scripts\activate
   ```
   - MacOS/Linux:
   ```
   source venv/bin/activate
   ```
5. Install dependensi yang diperlukan:
   ```
   pip install -r requirements.txt
   ```

## Cara Penggunaan

1. Jalankan aplikasi dengan perintah:
   ```
   python app.py
   ```
2. Buka browser dan akses aplikasi di alamat `http://127.0.0.1:5000`
3. Gunakan aplikasi dengan:
   - Memasukkan nilai luas lahan, curah hujan, dan tinggi wilayah secara manual
   - Memilih kecamatan dari dropdown untuk melihat prediksi berdasarkan data kecamatan
   - Melihat prediksi untuk semua kecamatan di Kabupaten Semarang

## Struktur Aplikasi

- `app.py` - File utama aplikasi Flask
- `fuzzy_tsukamoto.py` - Implementasi metode Fuzzy Tsukamoto
- `data_kecamatan.py` - Data kecamatan di Kabupaten Semarang
- `templates/` - Folder berisi template HTML
  - `index.html` - Halaman utama aplikasi
  - `hasil.html` - Halaman hasil prediksi semua kecamatan
- `requirements.txt` - Daftar dependensi aplikasi

## Model Fuzzy Tsukamoto

Model Fuzzy Tsukamoto yang diimplementasikan menggunakan aturan-aturan sebagai berikut:

1. Jika Luas Lahan KECIL dan Curah Hujan RENDAH dan Tinggi Wilayah RENDAH maka Hasil Panen BERKURANG
2. Jika Luas Lahan KECIL dan Curah Hujan RENDAH dan Tinggi Wilayah TINGGI maka Hasil Panen BERKURANG
3. Jika Luas Lahan KECIL dan Curah Hujan SEDANG dan Tinggi Wilayah RENDAH maka Hasil Panen BERKURANG
4. Jika Luas Lahan KECIL dan Curah Hujan SEDANG dan Tinggi Wilayah TINGGI maka Hasil Panen BERTAMBAH
5. Jika Luas Lahan KECIL dan Curah Hujan TINGGI dan Tinggi Wilayah RENDAH maka Hasil Panen BERTAMBAH
6. Jika Luas Lahan KECIL dan Curah Hujan TINGGI dan Tinggi Wilayah TINGGI maka Hasil Panen BERTAMBAH
7. Jika Luas Lahan BESAR dan Curah Hujan RENDAH dan Tinggi Wilayah RENDAH maka Hasil Panen BERKURANG
8. Jika Luas Lahan BESAR dan Curah Hujan RENDAH dan Tinggi Wilayah TINGGI maka Hasil Panen BERKURANG
9. Jika Luas Lahan BESAR dan Curah Hujan SEDANG dan Tinggi Wilayah RENDAH maka Hasil Panen BERTAMBAH
10. Jika Luas Lahan BESAR dan Curah Hujan SEDANG dan Tinggi Wilayah TINGGI maka Hasil Panen BERTAMBAH
11. Jika Luas Lahan BESAR dan Curah Hujan TINGGI dan Tinggi Wilayah RENDAH maka Hasil Panen BERTAMBAH
12. Jika Luas Lahan BESAR dan Curah Hujan TINGGI dan Tinggi Wilayah TINGGI maka Hasil Panen BERTAMBAH 