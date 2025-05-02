import streamlit as st
import pymongo
import datetime
import time

# Koneksi ke MongoDB
client = pymongo.MongoClient("mongodb+srv://neta_sic:neta_sic@backenddb.rfmwzg6.mongodb.net/?retryWrites=true&w=majority&appName=BackendDB")
db = client["locations"]
users_collection = db["users"]

# Set halaman
st.set_page_config(page_title="Aiovoice Tracker", page_icon="🌍")

st.title("Aiovoice Profile")

# Inisialisasi session state jika belum ada
if 'show_form' not in st.session_state:
    st.session_state['show_form'] = 'login'  # Default ke halaman login

def button_login_register():
    # Tombol login dan register
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("🔐 Login", use_container_width=True):
            st.session_state['show_form'] = 'login'
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("📝 Register", use_container_width=True):
            st.session_state['show_form'] = 'register'
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("👩‍👦 Family", use_container_width=True):
            st.session_state['show_form'] = 'family'
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# Fungsi untuk menampilkan form login
def show_login_form():
    st.info("Silakan login:")
    with st.form("login_form"):
        login_email = st.text_input("Email")
        login_password = st.text_input("Password", type="password")
        login_submit = st.form_submit_button("Login")
        if login_submit:
            if not login_email or not login_password:
                st.warning("Email dan password harus diisi!")
            else:
                # Verifikasi login dengan database
                user = users_collection.find_one({'email': login_email, 'password': login_password})
                if user:
                    # Jika login berhasil, set session state dan ubah halaman
                    st.session_state['show_form'] = 'home'
                    st.session_state['device_id'] = user['device_id']
                    st.session_state['email'] = login_email
                    st.success(f"Selamat datang, {login_email}!")
                    st.rerun()
                else:
                    st.warning("Email atau password salah!")

# Fungsi untuk menampilkan form register
def show_register_form():
    st.info("Buat akun baru:")
    with st.form("register_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        device_id = st.text_input("ID Alat")
        device_key = st.text_input("Sandi Alat")
        register_submit = st.form_submit_button("Register")
        if register_submit:
            if not email:
                st.warning("Email harus diisi!")
            elif not password:
                st.warning("Password harus diisi!")
            elif not device_id:
                st.warning("ID Alat harus diisi!")
            elif not device_key:
                st.warning("Sandi Alat harus diisi!")
            else:
                # Cek apakah email sudah terdaftar
                existing_user = users_collection.find_one({'email': email})
                if existing_user:
                    st.warning("Email sudah terdaftar!")
                else:
                    # Registrasi berhasil
                    result = users_collection.insert_one({
                        'device_id': device_id,
                        'device_key': device_key,
                        'email': email,
                        'password': password,
                        "key_option": "tolong",
                        'timestamp': datetime.datetime.utcnow()
                    })
                    st.success("Registrasi berhasil! Silakan login.")
                    time.sleep(2)
                    st.session_state['show_form'] = 'login'
                    st.rerun()

def show_device_id_form():
    st.info("Silakan Masukkan device id:")
    with st.form("device_id_form"):
        device_id = st.text_input("Device ID")
        login_submit = st.form_submit_button("Submit")
        if login_submit:
            if not device_id:
                st.warning("Id Device diisi!")
            else:
                st.session_state['device_id'] = device_id
                st.session_state['show_form'] = "home_family"
                st.success(f"Selamat datang Family")
                st.rerun()

# Fungsi untuk menampilkan profil
def show_profile():
    device_id = st.session_state.get('device_id', 'Unknown Device')
    st.write(f"Selamat datang, {device_id}!")
    st.write(f"ID Alat: {device_id}")

def key_options():
    # Inisialisasi session state jika belum ada
    user = users_collection.find_one({'email': st.session_state['email']})
    if 'key_option' not in st.session_state:
        st.session_state['key_option'] = user['key_option']

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    # Menampilkan tombol-tombol dengan pilihan
    with col1:
        if st.button("Aduh", use_container_width=True):
            st.session_state['key_option'] = 'aduh' 
    with col2:
        if st.button("Tolong", use_container_width=True):
            st.session_state['key_option'] = 'tolong' 
    with col3:
        if st.button("Please", use_container_width=True):
            st.session_state['key_option'] = 'please' 
    with col4:
        if st.button("Ayolah", use_container_width=True):
            st.session_state['key_option'] = 'ayolah' 

    # Menampilkan pilihan yang dipilih
    st.markdown(
        f"""
        <div style="border: 2px solid red; padding: 10px; background-color: #f9f9f9; border-radius: 10px; width: fit-content; margin-bottom:20px">
            <h4 style="color:red;">Kata Kunci: {st.session_state['key_option']}</h4>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Tombol untuk menyimpan pilihan
    if st.button("Save"):
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
            else:
                st.error("Tidak ada perubahan yang disimpan.")
        else:
            st.error("Pengguna tidak ditemukan.")

def show_family():
    st.success("HALO KELUARGA ⛔")


# Cek halaman berdasarkan session state
if st.session_state['show_form'] == 'login':
    button_login_register()
    # Menampilkan form login
    show_login_form()
elif st.session_state.get('show_form') == 'register':
    button_login_register()
    # Menampilkan form register
    show_register_form()
elif st.session_state.get('show_form') == 'home':
    # Menampilkan halaman profil setelah login
    show_profile()
    key_options()
elif st.session_state.get('show_form') == 'family':
    button_login_register()
    show_device_id_form()
elif st.session_state.get('show_form') == 'home_family':
    show_family()