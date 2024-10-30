import pandas as pd
import streamlit as st
import plotly.express as px

# Memuat data dari file Excel
file_path = 'sp_izin.xlsx'  # Ganti dengan path file Anda
data = pd.read_excel(file_path, sheet_name='Wialayah derivative')

# Mendefinisikan wilayah Jakarta yang ingin ditampilkan
wilayah_jakarta = ["Jakarta Timur", "Jakarta Selatan", "Jakarta Barat", "Jakarta Utara"]

# Memfilter data berdasarkan wilayah Jakarta
filtered_data = data[data['nama_kota'].isin(wilayah_jakarta)]

# Menghitung akumulasi total selesai per bidang untuk setiap wilayah Jakarta
grouped_data = filtered_data.groupby('nama_kota').sum().reset_index()

# Daftar kolom bidang yang ada
bidang_columns = ["Esdm", "Kehutanan", "Kelautan Dan Perikanan", "Kepemudaan dan Keolahragaan",
                  "Kesatuan Bangsa Dan Politik Dalam Negeri", "Kesehatan", 
                  "Ketenteraman, ketertiban Umum dan Pelindungan Masyarakat", 
                  "Lingkungan Hidup", "Pariwisata", "Pekerjaan Umum Dan Penataan Ruang", 
                  "Pelayanan Administrasi", "Pendidikan", "Perdagangan", 
                  "Perhubungan", "Pertanahan Yang Menjadi Kewenangan Daerah", 
                  "Pertanian", "Perumahan Rakyat Dan Kawasan Permukiman", "Sosial", 
                  "Tenaga Kerja"]

# Mengonversi data ke format long untuk Plotly
long_data = grouped_data.melt(id_vars="nama_kota", value_vars=bidang_columns,
                              var_name="Bidang", value_name="Total Selesai")

# Menghitung persentase untuk setiap bidang dalam wilayah
# Reset index untuk memastikan keselarasan sebelum menetapkan kolom 'Percentage'
long_data['Percentage'] = long_data.groupby('nama_kota')['Total Selesai'].transform(lambda x: (x / x.sum()) * 100) 
# long_data = long_data.reset_index(drop=True) # Reset indeks menjadi bilangan bulat berurutan

# Membuat Stack Bar Chart
fig = px.bar(long_data, y="nama_kota", x="Percentage", color="Bidang", orientation="h",
             title="Akumulasi Total Selesai per Bidang di Setiap Wilayah Jakarta",
             labels={"Percentage": "Persentase (%)", "nama_kota": "Wilayah Jakarta"})

# Menampilkan chart
st.plotly_chart(fig)
