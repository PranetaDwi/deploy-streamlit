import streamlit as st

st.set_page_config(page_title="Dashboard", layout="wide")

# Styling
st.markdown("""
    <style>
        .stMainBlockContainer {
            max-width: 95rem;
            padding-top: 5rem;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Profile")
st.markdown("---")

st.subheader("Info Akun")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    body {
        font-family: 'Inter', sans-serif;
        font-size: 18px;  /* Ukuran font untuk seluruh body */
    }

    .css-ffhzg2 {
        font-family: 'Inter', sans-serif;
        font-size: 18px;  /* Ukuran font untuk elemen tertentu */
    }

    /* Kamu bisa menambahkan lebih banyak styling seperti ini */
    .stMarkdown p {
        font-size: 20px;  /* Ukuran font untuk teks markdown */
    }
    </style>
    """, unsafe_allow_html=True
)

# Data
nama = "Annisa Urohmah"
email = "annisaurohman@mail.ugm.ac.id"
telepon = "0898887878787"
status = "Device Owner/Family"

# Layout dengan 2 kolom
col1, col2 = st.columns([1, 2])  # Bisa diatur proporsinya

with col1:
    st.markdown("**Nama**")
    st.markdown("**Email**")
    st.markdown("**Nomor Telepon**")
    st.markdown("**Status**")

with col2:
    st.markdown(nama)
    st.markdown(email)
    st.markdown(telepon)
    st.markdown(status)

st.subheader("Registed Family")

col1, col2, col3 = st.columns([2, 2,1])  # Bisa diatur proporsinya

with col1:
    st.markdown("**Annisa Urohmat**")
    st.markdown("**Annisa Urohmat**")
    st.markdown("**Annisa Urohmat**")
    st.markdown("**Annisa Urohmat**")

with col2:
    st.markdown("**annisa_urohmah@gmail.com**")
    st.markdown("**annisa_urohmah@gmail.com**")
    st.markdown("**annisa_urohmah@gmail.com**")
    st.markdown("**annisa_urohmah@gmail.com**")

with col3:
    st.markdown("**0986774635123**")
    st.markdown("**0986774635123**")
    st.markdown("**0986774635123**")
    st.markdown("**0986774635123**")