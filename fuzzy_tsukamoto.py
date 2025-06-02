import numpy as np

class FuzzyTsukamoto:
    def __init__(self):
        # Variabel input dan output
        self.luas_lahan = None
        self.curah_hujan = None
        self.tinggi_wilayah = None
        
        # Batas-batas himpunan fuzzy (berdasarkan dokumen)
        # Luas Lahan
        self.ll_kecil_min = 400
        self.ll_besar_max = 6000
        
        # Curah Hujan
        self.ch_rendah_min = 1000
        self.ch_sedang_min = 1800
        self.ch_tinggi_max = 3000
        
        # Tinggi Wilayah
        self.tw_rendah_min = 300
        self.tw_tinggi_max = 1500
        
        # Hasil Panen
        self.hp_berkurang_min = 2000
        self.hp_bertambah_max = 37000
        
    def set_input(self, luas_lahan, curah_hujan, tinggi_wilayah):
        self.luas_lahan = luas_lahan
        self.curah_hujan = curah_hujan
        self.tinggi_wilayah = tinggi_wilayah
        
    # Fungsi keanggotaan untuk Luas Lahan
    def luas_lahan_kecil(self, x):
        if x <= self.ll_kecil_min:
            return 1
        elif x >= self.ll_besar_max:
            return 0
        else:
            return (self.ll_besar_max - x) / (self.ll_besar_max - self.ll_kecil_min)
            
    def luas_lahan_besar(self, x):
        if x <= self.ll_kecil_min:
            return 0
        elif x >= self.ll_besar_max:
            return 1
        else:
            return (x - self.ll_kecil_min) / (self.ll_besar_max - self.ll_kecil_min)
    
    # Fungsi keanggotaan untuk Curah Hujan
    def curah_hujan_rendah(self, x):
        if x <= self.ch_rendah_min:
            return 1
        elif x >= self.ch_sedang_min:
            return 0
        else:
            return (self.ch_sedang_min - x) / (self.ch_sedang_min - self.ch_rendah_min)
            
    def curah_hujan_sedang(self, x):
        if x <= self.ch_rendah_min or x >= self.ch_tinggi_max:
            return 0
        elif x > self.ch_rendah_min and x < self.ch_sedang_min:
            return (x - self.ch_rendah_min) / (self.ch_sedang_min - self.ch_rendah_min)
        else:
            return (self.ch_tinggi_max - x) / (self.ch_tinggi_max - self.ch_sedang_min)
            
    def curah_hujan_tinggi(self, x):
        if x <= self.ch_sedang_min:
            return 0
        elif x >= self.ch_tinggi_max:
            return 1
        else:
            return (x - self.ch_sedang_min) / (self.ch_tinggi_max - self.ch_sedang_min)
    
    # Fungsi keanggotaan untuk Tinggi Wilayah
    def tinggi_wilayah_rendah(self, x):
        if x <= self.tw_rendah_min:
            return 1
        elif x >= self.tw_tinggi_max:
            return 0
        else:
            return (self.tw_tinggi_max - x) / (self.tw_tinggi_max - self.tw_rendah_min)
            
    def tinggi_wilayah_tinggi(self, x):
        if x <= self.tw_rendah_min:
            return 0
        elif x >= self.tw_tinggi_max:
            return 1
        else:
            return (x - self.tw_rendah_min) / (self.tw_tinggi_max - self.tw_rendah_min)
    
    # Fungsi keanggotaan untuk Hasil Panen (Output)
    def hasil_panen_berkurang(self, alpha):
        # Nilai Z untuk fungsi keanggotaan berkurang
        return self.hp_bertambah_max - (alpha * (self.hp_bertambah_max - self.hp_berkurang_min))
    
    def hasil_panen_bertambah(self, alpha):
        # Nilai Z untuk fungsi keanggotaan bertambah
        return self.hp_berkurang_min + (alpha * (self.hp_bertambah_max - self.hp_berkurang_min))
    
    def inference(self):
        # Fuzzifikasi
        luas_kecil = self.luas_lahan_kecil(self.luas_lahan)
        luas_besar = self.luas_lahan_besar(self.luas_lahan)
        
        hujan_rendah = self.curah_hujan_rendah(self.curah_hujan)
        hujan_sedang = self.curah_hujan_sedang(self.curah_hujan)
        hujan_tinggi = self.curah_hujan_tinggi(self.curah_hujan)
        
        tinggi_rendah = self.tinggi_wilayah_rendah(self.tinggi_wilayah)
        tinggi_tinggi = self.tinggi_wilayah_tinggi(self.tinggi_wilayah)
        
        # Rules dan Alpha predikat (sesuai dengan aturan dalam dokumen)
        # Rule 1: Luas Lahan KECIL, Curah Hujan RENDAH, Tinggi Wilayah RENDAH -> BERKURANG
        alpha_1 = min(luas_kecil, hujan_rendah, tinggi_rendah)
        z1 = self.hasil_panen_berkurang(alpha_1)
        
        # Rule 2: Luas Lahan KECIL, Curah Hujan RENDAH, Tinggi Wilayah TINGGI -> BERKURANG
        alpha_2 = min(luas_kecil, hujan_rendah, tinggi_tinggi)
        z2 = self.hasil_panen_berkurang(alpha_2)
        
        # Rule 3: Luas Lahan KECIL, Curah Hujan SEDANG, Tinggi Wilayah RENDAH -> BERKURANG
        alpha_3 = min(luas_kecil, hujan_sedang, tinggi_rendah)
        z3 = self.hasil_panen_berkurang(alpha_3)
        
        # Rule 4: Luas Lahan KECIL, Curah Hujan SEDANG, Tinggi Wilayah TINGGI -> BERTAMBAH
        alpha_4 = min(luas_kecil, hujan_sedang, tinggi_tinggi)
        z4 = self.hasil_panen_bertambah(alpha_4)
        
        # Rule 5: Luas Lahan KECIL, Curah Hujan TINGGI, Tinggi Wilayah RENDAH -> BERTAMBAH
        alpha_5 = min(luas_kecil, hujan_tinggi, tinggi_rendah)
        z5 = self.hasil_panen_bertambah(alpha_5)
        
        # Rule 6: Luas Lahan KECIL, Curah Hujan TINGGI, Tinggi Wilayah TINGGI -> BERTAMBAH
        alpha_6 = min(luas_kecil, hujan_tinggi, tinggi_tinggi)
        z6 = self.hasil_panen_bertambah(alpha_6)
        
        # Rule 7: Luas Lahan BESAR, Curah Hujan RENDAH, Tinggi Wilayah RENDAH -> BERKURANG
        alpha_7 = min(luas_besar, hujan_rendah, tinggi_rendah)
        z7 = self.hasil_panen_berkurang(alpha_7)
        
        # Rule 8: Luas Lahan BESAR, Curah Hujan RENDAH, Tinggi Wilayah TINGGI -> BERKURANG
        alpha_8 = min(luas_besar, hujan_rendah, tinggi_tinggi)
        z8 = self.hasil_panen_berkurang(alpha_8)
        
        # Rule 9: Luas Lahan BESAR, Curah Hujan SEDANG, Tinggi Wilayah RENDAH -> BERTAMBAH
        alpha_9 = min(luas_besar, hujan_sedang, tinggi_rendah)
        z9 = self.hasil_panen_bertambah(alpha_9)
        
        # Rule 10: Luas Lahan BESAR, Curah Hujan SEDANG, Tinggi Wilayah TINGGI -> BERTAMBAH
        alpha_10 = min(luas_besar, hujan_sedang, tinggi_tinggi)
        z10 = self.hasil_panen_bertambah(alpha_10)
        
        # Rule 11: Luas Lahan BESAR, Curah Hujan TINGGI, Tinggi Wilayah RENDAH -> BERTAMBAH
        alpha_11 = min(luas_besar, hujan_tinggi, tinggi_rendah)
        z11 = self.hasil_panen_bertambah(alpha_11)
        
        # Rule 12: Luas Lahan BESAR, Curah Hujan TINGGI, Tinggi Wilayah TINGGI -> BERTAMBAH
        alpha_12 = min(luas_besar, hujan_tinggi, tinggi_tinggi)
        z12 = self.hasil_panen_bertambah(alpha_12)
        
        # Defuzzifikasi dengan metode rata-rata (Average)
        alpha_sum = alpha_1 + alpha_2 + alpha_3 + alpha_4 + alpha_5 + alpha_6 + alpha_7 + alpha_8 + alpha_9 + alpha_10 + alpha_11 + alpha_12
        
        if alpha_sum == 0:
            return 0
        
        z_sum = (alpha_1 * z1) + (alpha_2 * z2) + (alpha_3 * z3) + (alpha_4 * z4) + (alpha_5 * z5) + (alpha_6 * z6) + (alpha_7 * z7) + (alpha_8 * z8) + (alpha_9 * z9) + (alpha_10 * z10) + (alpha_11 * z11) + (alpha_12 * z12)
        
        return z_sum / alpha_sum
    
    def predict(self, luas_lahan, curah_hujan, tinggi_wilayah):
        self.set_input(luas_lahan, curah_hujan, tinggi_wilayah)
        hasil_panen = self.inference()
        return hasil_panen

# Contoh data untuk Kecamatan Tengaran tahun 2021 (sesuai dokumen)
tengaran_2021 = {
    'luas_lahan': 1136,  # dalam hektar
    'curah_hujan': 2997,  # dalam mm
    'tinggi_wilayah': 729  # dalam mdpl
}

# Fungsi untuk memprediksi hasil panen berdasarkan data kecamatan
def predict_kecamatan(data):
    fuzzy = FuzzyTsukamoto()
    hasil = fuzzy.predict(data['luas_lahan'], data['curah_hujan'], data['tinggi_wilayah'])
    return hasil

# Contoh penggunaan untuk Tengaran 2021
if __name__ == "__main__":
    hasil_tengaran = predict_kecamatan(tengaran_2021)
    print(f"Prediksi hasil panen padi Kecamatan Tengaran tahun 2021: {hasil_tengaran:.2f} ton") 