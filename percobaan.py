import pandas as pd
import streamlit as st
import plotly.express as px

# Load data dari file Excel
file_path = 'sp_izin.xlsx'  # Ganti dengan path file yang sesuai
data = pd.read_excel(file_path, sheet_name='wilayah_derivative', skiprows=5)  # skiprows=5 agar mulai dari baris data

# Filter data hanya untuk wilayah Jakarta Timur, Jakarta Selatan, Jakarta Barat, dan Jakarta Utara
wilayah_terpilih = ["Jakarta Timur", "Jakarta Selatan", "Jakarta Barat", "Jakarta Utara"]
filtered_data = data[data["nama_kota"].isin(wilayah_terpilih)]

# Akumulasi data berdasarkan wilayah kota
grouped_data = filtered_data.groupby("nama_kota")[[
    "Esdm", "Kehutanan", "Kelautan Dan Perikanan", "Kepemudaan dan Keolahragaan",
    "Kesatuan Bangsa Dan Politik Dalam Negeri", "Kesehatan",
    "Ketenteraman, ketertiban Umum dan Pelindungan Masyarakat",
    "Lingkungan Hidup", "Pariwisata", "Pekerjaan Umum Dan Penataan Ruang",
    "Pelayanan Administrasi", "Pendidikan", "Perdagangan",
    "Perhubungan", "Pertanahan Yang Menjadi Kewenangan Daerah",
    "Pertanian", "Perumahan Rakyat Dan Kawasan Permukiman", "Sosial",
    "Tenaga Kerja"
]].sum().reset_index()

# Transformasi data untuk grafik stack bar chart
grouped_data = grouped_data.melt(id_vars="nama_kota", var_name="Bidang", value_name="Total Selesai")
grouped_data["Percentage"] = grouped_data.groupby("nama_kota")["Total Selesai"].apply(lambda x: (x / x.sum()) * 100)

# Buat grafik stack bar chart horizontal
fig = px.bar(grouped_data, y="nama_kota", x="Percentage", color="Bidang",
             title="Akumulasi Total Selesai per Bidang di Jakarta Timur, Jakarta Selatan, Jakarta Barat, dan Jakarta Utara",
             labels={"nama_kota": "Wilayah Kota", "Percentage": "Persentase (%)"},
             orientation="h", text="Percentage")

# Tampilkan grafik di Streamlit
st.plotly_chart(fig)
