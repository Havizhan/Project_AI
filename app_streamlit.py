import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from fuzzy_tsukamoto import FuzzyTsukamoto, predict_kecamatan
from data_kecamatan import kecamatan_semarang_by_year, get_data_by_year, available_years

# Konfigurasi halaman
st.set_page_config(
    page_title="Sistem Prediksi Hasil Panen Padi - Kabupaten Semarang",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fungsi untuk menampilkan header
def display_header():
    st.title("Sistem Prediksi Hasil Panen Padi Kabupaten Semarang")
    st.subheader("Menggunakan Metode Fuzzy Tsukamoto")
    st.markdown("---")

# Fungsi untuk melakukan prediksi manual
def predict_manual(luas_lahan, curah_hujan, tinggi_wilayah):
    fuzzy = FuzzyTsukamoto()
    hasil = fuzzy.predict(luas_lahan, curah_hujan, tinggi_wilayah)
    return hasil

# Fungsi untuk melakukan prediksi berdasarkan kecamatan dan tahun
def predict_by_kecamatan(nama_kecamatan, tahun):
    data = get_data_by_year(tahun)[nama_kecamatan]
    hasil = predict_kecamatan({
        'luas_lahan': data['luas_lahan'],
        'curah_hujan': data['curah_hujan'],
        'tinggi_wilayah': data['tinggi_wilayah']
    })
    
    # Hitung akurasi
    akurasi = None
    if 'hasil_panen_aktual' in data:
        akurasi = (1 - abs(hasil - data['hasil_panen_aktual']) / data['hasil_panen_aktual']) * 100
        if akurasi < 0:
            akurasi = 0
    
    return hasil, data, akurasi

# Fungsi untuk memprediksi semua kecamatan berdasarkan tahun
def predict_all_kecamatan(tahun):
    kecamatan_data = get_data_by_year(tahun)
    hasil_prediksi = {}
    hasil_aktual = {}
    akurasi = {}
    
    for kecamatan, data in kecamatan_data.items():
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
    
    return hasil_prediksi, hasil_aktual, akurasi

# Fungsi untuk memprediksi trend kecamatan dari tahun 2020-2022
def predict_trend_kecamatan(nama_kecamatan):
    trend_data = {
        'tahun': [],
        'prediksi': [],
        'aktual': [],
        'akurasi': []
    }
    
    for tahun in available_years:
        hasil, data, akurasi = predict_by_kecamatan(nama_kecamatan, tahun)
        trend_data['tahun'].append(tahun)
        trend_data['prediksi'].append(round(hasil, 2))
        trend_data['aktual'].append(data['hasil_panen_aktual'])
        trend_data['akurasi'].append(round(akurasi, 2) if akurasi is not None else 0)
    
    return trend_data

# Main app
def main():
    display_header()
    
    # Sidebar
    st.sidebar.title("Menu")
    menu_options = ["Prediksi Manual", "Prediksi Berdasarkan Kecamatan", "Prediksi Semua Kecamatan", "Analisis Trend 2020-2022"]
    choice = st.sidebar.radio("Pilih metode prediksi", menu_options)
    
    if choice == "Prediksi Manual":
        st.header("Prediksi Berdasarkan Input Manual")
        
        col1, col2 = st.columns(2)
        
        with col1:
            luas_lahan = st.number_input("Luas Lahan (hektar)", min_value=0.0, step=0.1)
            st.caption("Rentang: Kecil (≤ 400), Besar (≥ 6000)")
        
        with col2:
            curah_hujan = st.number_input("Curah Hujan (mm)", min_value=0.0, step=0.1)
            st.caption("Rentang: Rendah (≤ 1000), Sedang (1000-3000), Tinggi (≥ 3000)")
        
        tinggi_wilayah = st.number_input("Tinggi Wilayah (mdpl)", min_value=0.0, step=0.1)
        st.caption("Rentang: Rendah (≤ 300), Tinggi (≥ 1500)")
        
        if st.button("Prediksi"):
            if luas_lahan > 0 and curah_hujan > 0 and tinggi_wilayah > 0:
                hasil = predict_manual(luas_lahan, curah_hujan, tinggi_wilayah)
                st.success(f"Prediksi hasil panen padi: {hasil:.2f} ton")
                
                # Tampilkan informasi fuzzifikasi
                st.subheader("Detail Proses Fuzzy")
                fuzzy = FuzzyTsukamoto()
                
                st.write("**Fuzzifikasi Luas Lahan:**")
                luas_kecil = fuzzy.luas_lahan_kecil(luas_lahan)
                luas_besar = fuzzy.luas_lahan_besar(luas_lahan)
                st.write(f"- Derajat keanggotaan KECIL: {luas_kecil:.4f}")
                st.write(f"- Derajat keanggotaan BESAR: {luas_besar:.4f}")
                
                st.write("**Fuzzifikasi Curah Hujan:**")
                hujan_rendah = fuzzy.curah_hujan_rendah(curah_hujan)
                hujan_sedang = fuzzy.curah_hujan_sedang(curah_hujan)
                hujan_tinggi = fuzzy.curah_hujan_tinggi(curah_hujan)
                st.write(f"- Derajat keanggotaan RENDAH: {hujan_rendah:.4f}")
                st.write(f"- Derajat keanggotaan SEDANG: {hujan_sedang:.4f}")
                st.write(f"- Derajat keanggotaan TINGGI: {hujan_tinggi:.4f}")
                
                st.write("**Fuzzifikasi Tinggi Wilayah:**")
                tinggi_rendah = fuzzy.tinggi_wilayah_rendah(tinggi_wilayah)
                tinggi_tinggi = fuzzy.tinggi_wilayah_tinggi(tinggi_wilayah)
                st.write(f"- Derajat keanggotaan RENDAH: {tinggi_rendah:.4f}")
                st.write(f"- Derajat keanggotaan TINGGI: {tinggi_tinggi:.4f}")
            else:
                st.warning("Mohon isi semua field dengan nilai lebih dari 0.")
    
    elif choice == "Prediksi Berdasarkan Kecamatan":
        st.header("Prediksi Berdasarkan Kecamatan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_year = st.selectbox("Pilih Tahun", available_years)
        
        with col2:
            kecamatan_options = list(get_data_by_year(selected_year).keys())
            selected_kecamatan = st.selectbox("Pilih Kecamatan", kecamatan_options)
        
        if st.button("Prediksi"):
            hasil, data, akurasi = predict_by_kecamatan(selected_kecamatan, selected_year)
            
            st.success(f"Prediksi hasil panen padi untuk Kecamatan {selected_kecamatan} tahun {selected_year}: {hasil:.2f} ton")
            
            st.subheader("Data Kecamatan")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Luas Lahan", f"{data['luas_lahan']} hektar")
            with col2:
                st.metric("Curah Hujan", f"{data['curah_hujan']} mm")
            with col3:
                st.metric("Tinggi Wilayah", f"{data['tinggi_wilayah']} mdpl")
            
            if 'hasil_panen_aktual' in data:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Hasil Panen Aktual", f"{data['hasil_panen_aktual']} ton")
                with col2:
                    st.metric("Akurasi Prediksi", f"{akurasi:.2f}%")
                
                # Buat grafik perbandingan
                fig, ax = plt.subplots(figsize=(10, 5))
                values = [hasil, data['hasil_panen_aktual']]
                labels = ['Prediksi', 'Aktual']
                ax.bar(labels, values, color=['#5cb85c', '#337ab7'])
                for i, v in enumerate(values):
                    ax.text(i, v + 0.5, f"{v:.2f}", ha='center')
                ax.set_ylabel('Hasil Panen (ton)')
                ax.set_title(f'Perbandingan Hasil Panen Prediksi dan Aktual - {selected_kecamatan} ({selected_year})')
                st.pyplot(fig)
    
    elif choice == "Prediksi Semua Kecamatan":
        st.header("Prediksi Semua Kecamatan")
        
        selected_year = st.selectbox("Pilih Tahun", available_years)
        
        hasil_prediksi, hasil_aktual, akurasi = predict_all_kecamatan(selected_year)
        
        # Buat DataFrame untuk tampilan tabel
        data_table = []
        for kec in get_data_by_year(selected_year).keys():
            data_table.append({
                'Kecamatan': kec,
                'Prediksi (ton)': hasil_prediksi[kec],
                'Aktual (ton)': hasil_aktual[kec],
                'Akurasi (%)': akurasi[kec]
            })
        
        df = pd.DataFrame(data_table)
        st.dataframe(df, use_container_width=True)
        
        # Grafik perbandingan prediksi dan aktual
        st.subheader(f"Grafik Perbandingan Hasil Panen Prediksi dan Aktual ({selected_year})")
        
        kecamatan_names = list(get_data_by_year(selected_year).keys())
        prediksi_values = [hasil_prediksi[k] for k in kecamatan_names]
        aktual_values = [hasil_aktual[k] for k in kecamatan_names]
        
        fig, ax = plt.subplots(figsize=(14, 8))
        x = np.arange(len(kecamatan_names))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, prediksi_values, width, label='Prediksi')
        bars2 = ax.bar(x + width/2, aktual_values, width, label='Aktual')
        
        ax.set_xlabel('Kecamatan')
        ax.set_ylabel('Hasil Panen (ton)')
        ax.set_title(f'Perbandingan Hasil Panen Prediksi dan Aktual ({selected_year})')
        ax.set_xticks(x)
        ax.set_xticklabels(kecamatan_names, rotation=45, ha='right')
        ax.legend()
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Grafik akurasi
        st.subheader(f"Grafik Akurasi Prediksi per Kecamatan ({selected_year})")
        
        akurasi_values = [akurasi[k] for k in kecamatan_names]
        
        fig2, ax2 = plt.subplots(figsize=(14, 8))
        
        bars = ax2.bar(kecamatan_names, akurasi_values)
        ax2.set_xlabel('Kecamatan')
        ax2.set_ylabel('Akurasi (%)')
        ax2.set_title(f'Akurasi Prediksi Hasil Panen per Kecamatan ({selected_year})')
        ax2.set_xticklabels(kecamatan_names, rotation=45, ha='right')
        
        # Menambahkan nilai di atas bar
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height:.2f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        st.pyplot(fig2)
        
        # Tampilkan data kecamatan
        st.subheader(f"Data Kecamatan ({selected_year})")
        
        data_kec = []
        for kec, data in get_data_by_year(selected_year).items():
            data_kec.append({
                'Kecamatan': kec,
                'Luas Lahan (ha)': data['luas_lahan'],
                'Curah Hujan (mm)': data['curah_hujan'],
                'Tinggi Wilayah (mdpl)': data['tinggi_wilayah']
            })
        
        df_kec = pd.DataFrame(data_kec)
        st.dataframe(df_kec, use_container_width=True)
        
    elif choice == "Analisis Trend 2020-2022":
        st.header("Analisis Trend 2020-2022")
        
        kecamatan_options = list(get_data_by_year('2021').keys())
        selected_kecamatan = st.selectbox("Pilih Kecamatan", kecamatan_options)
        
        if st.button("Analisis"):
            trend_data = predict_trend_kecamatan(selected_kecamatan)
            
            # Tampilkan data trend
            st.subheader(f"Trend Data untuk Kecamatan {selected_kecamatan} (2020-2022)")
            
            # Buat tabel trend
            trend_df = pd.DataFrame({
                'Tahun': trend_data['tahun'],
                'Prediksi (ton)': trend_data['prediksi'],
                'Aktual (ton)': trend_data['aktual'],
                'Akurasi (%)': trend_data['akurasi']
            })
            
            st.dataframe(trend_df, use_container_width=True)
            
            # Buat grafik trend prediksi vs aktual
            st.subheader(f"Grafik Trend Hasil Panen Kecamatan {selected_kecamatan} (2020-2022)")
            
            fig, ax = plt.subplots(figsize=(12, 6))
            
            ax.plot(trend_data['tahun'], trend_data['prediksi'], 'o-', label='Prediksi', color='#5cb85c')
            ax.plot(trend_data['tahun'], trend_data['aktual'], 'o-', label='Aktual', color='#337ab7')
            
            # Tambahkan nilai di atas titik
            for i, (pred, act) in enumerate(zip(trend_data['prediksi'], trend_data['aktual'])):
                ax.text(trend_data['tahun'][i], pred + 0.5, f"{pred}", ha='center')
                ax.text(trend_data['tahun'][i], act - 0.5, f"{act}", ha='center')
            
            ax.set_xlabel('Tahun')
            ax.set_ylabel('Hasil Panen (ton)')
            ax.set_title(f'Trend Hasil Panen Prediksi vs Aktual - {selected_kecamatan} (2020-2022)')
            ax.legend()
            
            st.pyplot(fig)
            
            # Buat grafik trend akurasi
            st.subheader(f"Grafik Trend Akurasi Prediksi Kecamatan {selected_kecamatan} (2020-2022)")
            
            fig2, ax2 = plt.subplots(figsize=(12, 6))
            
            ax2.plot(trend_data['tahun'], trend_data['akurasi'], 'o-', color='#f0ad4e')
            
            # Tambahkan nilai di atas titik
            for i, acc in enumerate(trend_data['akurasi']):
                ax2.text(trend_data['tahun'][i], acc + 1, f"{acc}%", ha='center')
            
            ax2.set_xlabel('Tahun')
            ax2.set_ylabel('Akurasi (%)')
            ax2.set_title(f'Trend Akurasi Prediksi - {selected_kecamatan} (2020-2022)')
            
            st.pyplot(fig2)
            
            # Tampilkan data input untuk setiap tahun
            st.subheader(f"Data Input Kecamatan {selected_kecamatan} (2020-2022)")
            
            input_data = []
            for tahun in available_years:
                data = get_data_by_year(tahun)[selected_kecamatan]
                input_data.append({
                    'Tahun': tahun,
                    'Luas Lahan (ha)': data['luas_lahan'],
                    'Curah Hujan (mm)': data['curah_hujan'],
                    'Tinggi Wilayah (mdpl)': data['tinggi_wilayah']
                })
            
            input_df = pd.DataFrame(input_data)
            st.dataframe(input_df, use_container_width=True)

if __name__ == "__main__":
    main() 