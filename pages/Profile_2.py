import streamlit as st
import pymongo

st.set_page_config(page_title="Profile", layout="wide")

client = pymongo.MongoClient("mongodb+srv://neta_sic:neta_sic@backenddb.rfmwzg6.mongodb.net/?retryWrites=true&w=majority&appName=BackendDB")
db = client["locations"]

users_collection = db["users"]

if 'email' not in st.session_state:
    st.session_state['email'] = None

if st.session_state['email'] is None:
    st.warning("Silahkan login dahulu untuk melanjutkan")
    st.stop()


if 'key_option' not in st.session_state:
    st.session_state['key_option'] = user['key_option']

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

@st.dialog("Change Password")
def edit_password():
    user = users_collection.find_one({'email': st.session_state['email']})
    st.subheader("Current Password")
    st.header(user['key_option'])

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("Ayolah", use_container_width=True):
            st.session_state['key_option'] = 'ayolah'
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("Tolong", use_container_width=True):
            st.session_state['key_option'] = 'tolong'
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("Please", use_container_width=True):
            st.session_state['key_option'] = 'please'
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Update kata kunci", use_container_width=True):
        # Mengupdate pilihan yang dipilih ke database MongoDB berdasarkan email atau device_id
        user = users_collection.find_one({'email': st.session_state['email']})  # Ganti dengan email atau identifier lainnya
        if user:
            # Update 'key_options' di dokumen pengguna
            result = users_collection.update_one(
                {'email': st.session_state['email']},  # Ganti dengan email atau identifier lainnya
                {'$set': {'key_option': st.session_state['key_option']}}
            )
            if result.modified_count > 0:
                st.success(f"Pilihan '{st.session_state['key_option']}' berhasil disimpan!")
                st.rerun()
            else:
                st.error("Tidak ada perubahan yang disimpan.")
        else:
            st.error("Pengguna tidak ditemukan.")

user = users_collection.find_one({'email': st.session_state['email']})

# Data
nama = "Praneta Dwi Indarti"
email = user['email']
telepon = "0898887878787"
status = "Device Owner/Family"

# Layout dengan 2 kolom
with st.container():
    st.markdown("### 💀 Profil Pengguna")
    
    col1, col2, col3 = st.columns([1.2, 2, 1])
    
    with col1:
        st.markdown("**👤 Nama**")
        st.markdown("**✉️ Email**")
        st.markdown("**📞 Telepon**")
        st.markdown("**💫 Status**")

    with col2:
        st.write(nama)
        st.write(email)
        st.write(telepon)
        st.write(status)

    with col3:
        st.button("✏️ Edit Profil", use_container_width=True)
        if st.button("🔒 Edit Password", use_container_width=True):
            edit_password()  # pastikan fungsi ini sudah didefinisikan

# Divider untuk pembatas
st.divider()


# Section berikutnya
st.subheader("👨‍👩 Keluarga Terdaftar")

col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    st.markdown("**👤 Nama**")
with col2:
    st.markdown("**📧 Email**")
with col3:
    st.markdown("**📱 Telepon**")

for i in range(4):  # ganti 4 dengan jumlah data
    with st.container():
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.write("Annisa Urohmah")
        with col2:
            st.write("annisa_urohmah@gmail.com")
        with col3:
            st.write("0986774635123")
        st.divider()


# st.button("Edit Password", key="password_button")
