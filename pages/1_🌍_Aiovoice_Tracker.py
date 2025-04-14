import streamlit as st
import pandas as pd
import pymongo
import pydeck as pdk
import gridfs
from io import BytesIO
from urllib.error import URLError

st.set_page_config(page_title="Aiovoice Tracker", page_icon="🌍")

client = pymongo.MongoClient("mongodb+srv://neta_sic:neta_sic@backenddb.rfmwzg6.mongodb.net/?retryWrites=true&w=majority&appName=BackendDB")
db = client["locations"]
collection = db["realtime_location"]

# Koneksi ke GridFS untuk audio
fs = gridfs.GridFS(db)

# Ambil data lokasi dari MongoDB
data_mongo = list(collection.find({}, {"_id": 0, "device_id": 1, "lat": 1, "lon": 1}))

# Ubah ke DataFrame
df = pd.DataFrame(data_mongo)

# Ambil data audio dari MongoDB
audio_files = list(fs.find())  # Ambil semua file audio dari GridFS

# Cek apakah ada data lokasi dan audio
if not df.empty and audio_files:
    # Membuat layer scatter untuk peta
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        df,
        get_position='[lon, lat]',
        get_color='[255, 0, 0, 255]',  # Warna marker
        get_radius=50,  # Ukuran radius marker
        pickable=True,
        auto_highlight=True,
    )

    # Menentukan view state untuk peta
    view_state = pdk.ViewState(
        latitude=df["lat"].mean(),  # Rata-rata latitude
        longitude=df["lon"].mean(),  # Rata-rata longitude
        zoom=14  # Level zoom peta
    )

    # Menampilkan peta dengan pydeck
    st.title("Peta Lokasi dan Audio dari MongoDB Atlas")

    st.subheader("Daerah Rawan Penculikan")
    st.pydeck_chart(pdk.Deck(
        layers=[scatter_layer],
        initial_view_state=view_state,
        map_style='mapbox://styles/mapbox/streets-v12'
    ))

    # Menampilkan daftar file audio
    st.subheader("Daftar File Audio:")
    for audio in audio_files:
        # Ambil byte file audio
        audio_data = audio.read()
        
        # Menampilkan nama file audio
        st.markdown(f"**{audio.filename}**")

        # Memutar audio di Streamlit
        st.audio(audio_data, format="audio/mp3")  # Ganti format sesuai file audio
else:
    st.warning("Tidak ada data lokasi atau audio ditemukan di MongoDB.")

