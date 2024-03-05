import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
from datetime import datetime

# Membaca data dari URL
url = "https://web.meteo.bmkg.go.id//media/data/bmkg//inacawo//output.txt"
df = pd.read_csv(url)

# Fungsi untuk menentukan kategori cuaca
def categorize_weather(rr):
    if 0.1 < rr <= 5:
        return "hujan ringan.png"
    elif 5 < rr <= 10:
        return "hujan sedang.png"
    elif 10 < rr <= 20:
        return "hujan lebat.png"
    else:
        return "cerah berawan.png"

# Fungsi untuk menampilkan popup
def popup_html(data):
    return f"<b>Desa:</b> {data['desa']}<br><b>Kecamatan:</b> {data['kec']}<br><b>RR:</b> {data['rr']}<br><b>Wspd:</b> {data['wspd']}<br><b>Wdir:</b> {data['wdir']}<br><b>RH:</b> {data['rh']}<br><b>TT:</b> {data['tt']}"

# Menampilkan aplikasi
st.title("Prediksi Cuaca Kelurahan di IKN")

# Mendapatkan daftar tanggal yang tersedia dalam dataframe
available_dates = pd.to_datetime(df['time']).dt.date.unique()

# Memilih waktu yang ditampilkan (tanggal dan jam)
selected_date = st.date_input("Pilih Tanggal:", min_value=min(available_dates), max_value=datetime(2024, 12, 31))
selected_hour = st.slider("Pilih Jam (Interval per Jam):", min_value=0, max_value=23, step=1)

# Menggabungkan tanggal dan jam yang dipilih menjadi satu objek datetime
selected_datetime = datetime(selected_date.year, selected_date.month, selected_date.day, selected_hour)

# Membuat peta
m = folium.Map(location=[-1.173, 116.59], zoom_start=9.4)

# Menambahkan marker pada peta
for index, row in df.iterrows():
    data_datetime = datetime.strptime(str(row['time']), "%Y%m%d%H%M%S")
    if data_datetime.hour == selected_hour and data_datetime.date() == selected_date:
        icon_url = categorize_weather(row['rr'])
        icon = folium.features.CustomIcon(icon_url, icon_size=(30, 30))
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=folium.Popup(popup_html(row), max_width=300),
            icon=icon
        ).add_to(m)


# Menampilkan peta
st.write("### Peta Cuaca")
folium_static(m)
