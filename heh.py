import streamlit as st
import pandas as pd
import os


st.set_page_config(page_title="Katalog Anggrek", layout="wide")

st.markdown("""
<style>

/* Background utama */
.stApp {
    background: linear-gradient(to bottom, #fff0f6, #fce4ec);
}

/* Judul utama */
h1 {
    color: #ad1457 !important;
    font-weight: 800;
}

/* Header */
h2, h3 {
    color: #c2185b !important;
}

/* Card produk (container) */
div[data-testid="stVerticalBlock"] > div:has(div.stImage) {
    background-color: white;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}

/* Tombol */
div.stButton > button {
    background-color: #c2185b;
    color: white;
    border-radius: 12px;
    font-weight: bold;
}

div.stButton > button:hover {
    background-color: #880e4f;
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #f8bbd0;
}

/* Expander */
details {
    background-color: #fff;
    padding: 10px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

if "keranjang" not in st.session_state:
    st.session_state.keranjang = []

if os.path.exists("anggrekku.png"):
    st.image("anggrekku.png", use_container_width=True)

st.markdown(
    "<h1 style='text-align:center;'>🌸 Koleksi Anggrek Kelompok 3</h1>",
    unsafe_allow_html=True
)

 
st.divider()

def tips_perawatan(kategori):

    kategori = kategori.lower().strip()

    if kategori == "vanda":
        return """
Siram 2–3x seminggu  
Cahaya terang tidak langsung  
Suhu 18–30°C  
Pupuk 2 minggu sekali
"""

    elif kategori == "dendrobium":
        return """
Siram setiap 2 hari sekali  
Butuh cahaya lebih banyak  
Suhu 20–32°C  
Gunakan pupuk tinggi nitrogen saat fase daun
"""

    else:
        return """
Siram 2–3x seminggu  
Cahaya cukup  
Suhu 20–30°C  
Pupuk rutin setiap 2 minggu
"""

try:
    if os.path.exists("anggrekkel3.csv"):

        df = pd.read_csv("anggrekkel3.csv", encoding="utf-8")
        df["harga"] = pd.to_numeric(df["harga"], errors="coerce")
        df["status"] = df["status"].fillna("tersedia")

        st.sidebar.header("🔍 Filter Produk")

        kategori_list = ["Semua"] + sorted(df["kategori"].unique())
        kategori_pilih = st.sidebar.selectbox("Pilih Kategori", kategori_list)

        keyword = st.sidebar.text_input("Cari Nama Anggrek")

        if kategori_pilih != "Semua":
            df = df[df["kategori"] == kategori_pilih]

        if keyword:
            df = df[df["nama"].str.contains(keyword, case=False, na=False)]

        # =========================
        # TAMPILKAN PRODUK
        # =========================
        if df.empty:
            st.warning("Produk tidak ditemukan.")
        else:
            cols = st.columns(3)

            for index, row in df.reset_index().iterrows():
                with cols[index % 3]:

                    st.markdown("----")

                    if os.path.exists(row["foto"]):
                        st.image(row["foto"], use_container_width=True)

                    st.subheader(row["nama"])
                    st.markdown(f"💰 **Rp {int(row['harga']):,}**")

                    # STATUS
                    if row["status"].lower() == "belum tersedia":
                        st.error("❌ Belum Tersedia")
                    else:
                        st.success("✅ Tersedia")

                        if st.button("🛒 Tambah ke Keranjang", key=f"btn_{index}"):
                            st.session_state.keranjang.append({
                                "nama": row["nama"],
                                "harga": row["harga"]
                            })
                            st.success("Ditambahkan ke keranjang!")

                    # TIPS PERAWATAN
                    with st.expander("🌿 Tips Perawatan"):
                        st.markdown(tips_perawatan(row["kategori"]))

        
        st.sidebar.divider()
        st.sidebar.header("🛍 Keranjang Belanja")

        if len(st.session_state.keranjang) == 0:
            st.sidebar.info("Keranjang masih kosong")
        else:
            total = 0

            for i, item in enumerate(st.session_state.keranjang):
                st.sidebar.write(f"{item['nama']} - Rp {int(item['harga']):,}")
                total += item["harga"]

                if st.sidebar.button("❌ Hapus", key=f"hapus_{i}"):
                    st.session_state.keranjang.pop(i)
                    st.rerun()

            st.sidebar.divider()
            st.sidebar.subheader(f"Total: Rp {int(total):,}")

            # Checkout WhatsApp
            no_hp = "6288215748030"
            pesan = "Halo, saya ingin memesan:\n"

            for item in st.session_state.keranjang:
                pesan += f"- {item['nama']} (Rp {int(item['harga']):,})\n"

            pesan += f"\nTotal: Rp {int(total):,}"

            link_wa = f"https://wa.me/{no_hp}?text={pesan.replace(' ', '%20').replace(chr(10), '%0A')}"

            st.sidebar.link_button("📱 Checkout via WhatsApp", link_wa)

            if st.sidebar.button("🗑 Kosongkan Keranjang"):
                st.session_state.keranjang = []
                st.rerun()

    else:
        st.error("File 'anggrekkel3.csv' tidak ditemukan!")

except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")

st.divider()
st.header("🌱 Edukasi: Pupuk Organik untuk Anggrek")

with st.expander("🌿 Klik untuk melihat cara membuat pupuk dari kulit pisang"):
    
    st.subheader("🎥 Video Tutorial")
    st.video("https://youtu.be/8mZjb9VVrAQ")

    st.subheader("Bahan")
    st.write("""
    - 3–5 kulit pisang  
    - 1 liter air bersih  
    - Botol atau wadah tertutup  
    """)

    st.subheader("Cara Membuat")
    st.write("""
    1. Potong kecil-kecil kulit pisang  
    2. Masukkan ke dalam botol  
    3. Tambahkan 1 liter air  
    4. Tutup rapat  
    5. Diamkan 2–3 hari  
    6. Saring sebelum digunakan  
    """)

    st.subheader("Manfaat")
    st.success("""
    - Kaya kalium  
    - Merangsang pertumbuhan bunga  
    - Menguatkan akar  
    """)
with st.expander("🌸Tips Anggrek cepat berbunga"):

    st.success("""
    - Gunakan sprayer untuk mengaplikasikan pupuk pada daun dan akar.
    - Berikan pupuk secara teratur namun jangan terlalu lembap.
    - Pastikan anggrek mendapatkan cahaya matahari yang cukup namun tidak langsung.  
    """)

st.divider()
st.subheader("📍 Hubungi Kami")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
**Alamat Galeri:**  
Jl. C. Simanjuntak No.60, Yogyakarta
""")
    
    st.components.v1.html("""
<iframe
  src="https://www.google.com/maps?q=Jl.+C.+Simanjuntak+No.60+Yogyakarta&output=embed"
  width="100%"
  height="300"
  style="border:0;"
  allowfullscreen=""
  loading="lazy">
</iframe>
""", height=300)

with col2:
    no_hp = "6288215748030"
    pesan = "Halo, saya tertarik memesan anggrek di katalog Anda."
    link_wa = f"https://wa.me/{no_hp}?text={pesan.replace(' ', '%20')}"
    st.link_button("📱 Pesan via WhatsApp", link_wa)

st.caption("© 2026 Toko Anggrek Digital")



