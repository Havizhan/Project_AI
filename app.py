from flask import Flask, render_template, request, jsonify
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from fuzzy_tsukamoto import FuzzyTsukamoto, predict_kecamatan
from data_kecamatan import kecamatan_semarang

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', kecamatan=list(kecamatan_semarang.keys()))

@app.route('/predict', methods=['POST'])
def predict():
    # Prediksi berdasarkan inputan user
    if request.form.get('type') == 'manual':
        try:
            luas_lahan = float(request.form.get('luas_lahan', 0))
            curah_hujan = float(request.form.get('curah_hujan', 0))
            tinggi_wilayah = float(request.form.get('tinggi_wilayah', 0))
            
            fuzzy = FuzzyTsukamoto()
            hasil = fuzzy.predict(luas_lahan, curah_hujan, tinggi_wilayah)
            
            return jsonify({
                'success': True,
                'hasil': round(hasil, 2),
                'message': f'Prediksi hasil panen padi: {hasil:.2f} ton'
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            })
    # Prediksi berdasarkan kecamatan yang dipilih
    elif request.form.get('type') == 'kecamatan':
        try:
            nama_kecamatan = request.form.get('kecamatan')
            if nama_kecamatan not in kecamatan_semarang:
                return jsonify({
                    'success': False,
                    'message': 'Kecamatan tidak ditemukan'
                })
                
            data = kecamatan_semarang[nama_kecamatan]
            hasil = predict_kecamatan({
                'luas_lahan': data['luas_lahan'],
                'curah_hujan': data['curah_hujan'],
                'tinggi_wilayah': data['tinggi_wilayah']
            })
            
            # Hitung akurasi (jika hasil_panen_aktual tersedia)
            akurasi = None
            if 'hasil_panen_aktual' in data:
                akurasi = (1 - abs(hasil - data['hasil_panen_aktual']) / data['hasil_panen_aktual']) * 100
                if akurasi < 0:
                    akurasi = 0
            
            return jsonify({
                'success': True,
                'hasil': round(hasil, 2),
                'hasil_aktual': data.get('hasil_panen_aktual'),
                'akurasi': round(akurasi, 2) if akurasi is not None else None,
                'message': f'Prediksi hasil panen padi untuk Kecamatan {nama_kecamatan}: {hasil:.2f} ton',
                'data': data
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            })

@app.route('/predict_all')
def predict_all():
    hasil_prediksi = {}
    hasil_aktual = {}
    akurasi = {}
    
    for kecamatan, data in kecamatan_semarang.items():
        hasil = predict_kecamatan({
            'luas_lahan': data['luas_lahan'],
            'curah_hujan': data['curah_hujan'],
            'tinggi_wilayah': data['tinggi_wilayah']
        })
        hasil_prediksi[kecamatan] = round(hasil, 2)
        
        if 'hasil_panen_aktual' in data:
            hasil_aktual[kecamatan] = data['hasil_panen_aktual']
            acc = (1 - abs(hasil - data['hasil_panen_aktual']) / data['hasil_panen_aktual']) * 100
            if acc < 0:
                acc = 0
            akurasi[kecamatan] = round(acc, 2)
    
    # Membuat grafik perbandingan prediksi dan aktual
    fig, ax = plt.subplots(figsize=(14, 8))
    
    kecamatan_names = list(kecamatan_semarang.keys())
    prediksi_values = [hasil_prediksi[k] for k in kecamatan_names]
    aktual_values = [hasil_aktual[k] for k in kecamatan_names]
    
    x = np.arange(len(kecamatan_names))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, prediksi_values, width, label='Prediksi')
    bars2 = ax.bar(x + width/2, aktual_values, width, label='Aktual')
    
    ax.set_xlabel('Kecamatan')
    ax.set_ylabel('Hasil Panen (ton)')
    ax.set_title('Perbandingan Hasil Panen Prediksi dan Aktual')
    ax.set_xticks(x)
    ax.set_xticklabels(kecamatan_names, rotation=45, ha='right')
    ax.legend()
    
    plt.tight_layout()
    
    # Menyimpan gambar ke BytesIO
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)
    
    # Membuat grafik akurasi
    fig2, ax2 = plt.subplots(figsize=(14, 8))
    
    akurasi_values = [akurasi[k] for k in kecamatan_names]
    
    bars = ax2.bar(kecamatan_names, akurasi_values)
    ax2.set_xlabel('Kecamatan')
    ax2.set_ylabel('Akurasi (%)')
    ax2.set_title('Akurasi Prediksi Hasil Panen per Kecamatan')
    ax2.set_xticklabels(kecamatan_names, rotation=45, ha='right')
    
    # Menambahkan nilai di atas bar
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.2f}%', ha='center', va='bottom')
    
    plt.tight_layout()
    
    # Menyimpan gambar ke BytesIO
    img2 = BytesIO()
    plt.savefig(img2, format='png')
    img2.seek(0)
    graph_url2 = base64.b64encode(img2.getvalue()).decode()
    plt.close(fig2)
    
    return render_template('hasil.html', 
                          hasil_prediksi=hasil_prediksi,
                          hasil_aktual=hasil_aktual,
                          akurasi=akurasi,
                          graph_url=graph_url,
                          graph_url2=graph_url2,
                          kecamatan=kecamatan_semarang)

if __name__ == '__main__':
    # Buat folder templates jika belum ada
    import os
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    app.run(debug=True) 