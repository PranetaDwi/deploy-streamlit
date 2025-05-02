import streamlit as st
import pandas as pd
import pymongo
import pydeck as pdk
import gridfs
from io import BytesIO
from urllib.error import URLError

st.set_page_config(page_title="Aiovoice Tracker", page_icon="🌍")

if 'device_id' not in st.session_state:
    st.session_state['device_id'] = None

if st.session_state['device_id'] is None:
    st.warning("Silahkan login dahulu untuk melanjutkan")
    st.stop() 

client = pymongo.MongoClient("mongodb+srv://neta_sic:neta_sic@backenddb.rfmwzg6.mongodb.net/?retryWrites=true&w=majority&appName=BackendDB")
db = client["locations"]

realtime_location_collection = db["realtime_location"]
vulnerable_location_collection = db["vulnerable_location"]

# Koneksi ke GridFS untuk audio
fs = gridfs.GridFS(db)

# Ambil data lokasi dari MongoDB
data_realtime = list(realtime_location_collection.find({}, {"_id": 0, "device_id": 1, "lat": 1, "lon": 1}))
data_vulnerable = list(vulnerable_location_collection.find({}, {"_id": 0, "device_id": 1, "lat": 1, "lon": 1}))

# Ubah ke DataFrame
df_realtime = pd.DataFrame(data_realtime)
df_vulnerable = pd.DataFrame(data_vulnerable)

# Ambil data audio dari MongoDB
audio_files = list(fs.find())  # Ambil semua file audio dari GridFS

st.title("Aiovoice Dashboard")

if not df_realtime.empty:
    # Layer untuk lokasi
    realtime_scatter = pdk.Layer(
        "ScatterplotLayer",
        df_realtime,
        get_position='[lon, lat]',
        get_color='[255, 0, 0, 255]',
        get_radius=15,
        pickable=True,
        auto_highlight=True,
    )

    # ViewState default berdasarkan data
    view_state = pdk.ViewState(
        latitude=df_realtime["lat"].mean(),
        longitude=df_realtime["lon"].mean(),
        zoom=15
    )
else:
    # Jika tidak ada data, set posisi default (misalnya: Yogyakarta)
    st.info("Tidak ada data lokasi ditemukan. Menampilkan peta kosong.")
    realtime_scatter = pdk.Layer("ScatterplotLayer", [])
    view_state = pdk.ViewState(latitude=-7.801194, longitude=110.364917, zoom=12)

# --- Peta Lokasi ---
st.subheader("Realtime Tracker")
st.pydeck_chart(pdk.Deck(
    layers=[realtime_scatter],
    initial_view_state=view_state,
    map_style='mapbox://styles/mapbox/streets-v12'
))

if not df_vulnerable.empty:
    # Layer untuk lokasi
    vulnerable_scatter = pdk.Layer(
        "ScatterplotLayer",
        df_vulnerable,
        get_position='[lon, lat]',
        get_color='[255, 0, 0, 255]',
        get_radius=80,
        pickable=True,
        auto_highlight=True,
    )

    # ViewState default berdasarkan data
    view_state = pdk.ViewState(
        latitude=df_vulnerable["lat"].mean(),
        longitude=df_vulnerable["lon"].mean(),
        zoom=14
    )
else:
    # Jika tidak ada data, set posisi default (misalnya: Yogyakarta)
    st.info("Tidak ada data lokasi ditemukan. Menampilkan peta kosong.")
    vulnerable_scatter = pdk.Layer("ScatterplotLayer", [])
    view_state = pdk.ViewState(latitude=-7.801194, longitude=110.364917, zoom=12)

# Tampilkan peta (selalu muncul meskipun kosong)
# --- Peta Lokasi ---
st.subheader("Daerah Rawan Penculikan")
st.pydeck_chart(pdk.Deck(
    layers=[vulnerable_scatter],
    initial_view_state=view_state,
    map_style='mapbox://styles/mapbox/streets-v12'
))

if audio_files:
    # --- Audio Files ---
    st.subheader("Daftar File Audio:")

    for audio in audio_files:
        audio_data = audio.read()
        st.markdown(f"**{audio.filename}**")
        st.audio(audio_data, format="audio/mp3")
else:
    st.info("Belum ada file audio yang tersimpan.")

