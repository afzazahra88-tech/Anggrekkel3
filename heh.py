import streamlit as st
import pandas as pd
import os

# =========================
# FORMAT RUPIAH (PENTING)
# =========================
def format_rupiah(angka):
    try:
        return f"Rp {int(angka):,}".replace(",", ".")
    except:
        return "Rp 0"

# =========================
# CONFIG
# =========================
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

/* Card produk */
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
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #f8bbd0;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SESSION
# =========================
if "keranjang" not in st.session_state:
    st.session_state.keranjang = []

# =========================
# HEADER
# =========================
if os.path.exists("anggrekku.png"):
    st.image("anggrekku.png", use_container_width=True)

st.markdown("<h1 style='text-align:center;'>🌸 Koleksi Anggrek Unggulan</h1>", unsafe_allow_html=True)
st.divider()

# =========================
# TIPS PERAWATAN
# =========================
def tips_perawatan(kategori):
    kategori = kategori.lower().strip()

    if kategori == "vanda":
        return """Siram 2–3x seminggu  
Cahaya terang tidak langsung  
Suhu 18–30°C  
Pupuk 2 minggu sekali"""

    elif kategori == "dendrobium":
        return """Siram setiap 2 hari sekali  
Butuh cahaya lebih banyak  
Suhu 20–32°C  
Gunakan pupuk tinggi nitrogen"""

    else:
        return """Siram 2–3x seminggu  
Cahaya cukup  
Suhu 20–30°C  
Pupuk rutin"""

# =========================
# LOAD DATA
# =========================
try:
    if os.path.exists("anggrekkel3.csv"):

        df = pd.read_csv("anggrekkel3.csv")
        df["harga"] = pd.to_numeric(df["harga"], errors="coerce")
        df["status"] = df["status"].fillna("tersedia")

        # =========================
        # FILTER
        # =========================
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

                    st.markdown("---")

                    if os.path.exists(row["foto"]):
                        st.image(row["foto"], use_container_width=True)

                    st.subheader(row["nama"])

                    # ✅ FORMAT RUPIAH DI SINI
                    st.markdown(f"**{format_rupiah(row['harga'])}**")

                    if row["status"].lower() == "belum tersedia":
                        st.error("Belum Tersedia")
                    else:
                        st.success("Tersedia")

                        if st.button("Tambah ke Keranjang", key=f"btn_{index}"):
                            st.session_state.keranjang.append({
                                "nama": row["nama"],
                                "harga": row["harga"]
                            })
                            st.success("Ditambahkan ke keranjang!")

                    with st.expander("🌿 Tips Perawatan"):
                        st.markdown(tips_perawatan(row["kategori"]))

        # =========================
        # SIDEBAR KERANJANG
        # =========================
        st.sidebar.divider()
        st.sidebar.header("🛍 Keranjang Belanja")

        if len(st.session_state.keranjang) == 0:
            st.sidebar.info("Keranjang masih kosong")
        else:
            total = 0

            for i, item in enumerate(st.session_state.keranjang):
                # ✅ FORMAT DI SINI
                st.sidebar.write(f"{item['nama']} - {format_rupiah(item['harga'])}")
                total += item["harga"]

                if st.sidebar.button("❌ Hapus", key=f"hapus_{i}"):
                    st.session_state.keranjang.pop(i)
                    st.rerun()

            st.sidebar.divider()

            # ✅ TOTAL
            st.sidebar.subheader(f"Total: {format_rupiah(total)}")

            # =========================
            # WHATSAPP
            # =========================
            no_hp = "6288215748030"
            pesan = "Halo, saya ingin memesan:\n"

            for item in st.session_state.keranjang:
                pesan += f"- {item['nama']} ({format_rupiah(item['harga'])})\n"

            pesan += f"\nTotal: {format_rupiah(total)}"

            link_wa = f"https://wa.me/{no_hp}?text={pesan.replace(' ', '%20').replace(chr(10), '%0A')}"

            st.sidebar.link_button("📱 Checkout via WhatsApp", link_wa)

            if st.sidebar.button("🗑 Kosongkan Keranjang"):
                st.session_state.keranjang = []
                st.rerun()

    else:
        st.error("File CSV tidak ditemukan!")

except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")

# =========================
# EDUKASI
# =========================
st.divider()
st.header("🌱 Edukasi: Pupuk Organik untuk Anggrek")

with st.expander("🌿 Cara membuat pupuk kulit pisang"):
    st.video("https://youtu.be/8mZjb9VVrAQ")

# =========================
# FOOTER
# =========================
st.divider()
st.caption("© 2026 Toko Anggrek Digital")
