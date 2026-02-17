import streamlit as st
import pandas as pd
import os

# Konfigurasi Halaman
st.set_page_config(page_title="Katalog Anggrek", layout="wide")

# Tampilkan Banner
if os.path.exists("anggrekku.png"):
    st.image("anggrekku.png", use_container_width=True)

st.title("🌸 Koleksi Anggrek Kelompok 3")
st.divider()

try:
    if os.path.exists("anggrekkel3.csv"):
        df = pd.read_csv("anggrekkel3.csv")
        df = df.dropna(subset=['foto'])

        daftar_kategori = df['kategori'].unique()

        for kat in daftar_kategori:
            st.header(f"🌿 Anggrek Jenis {kat.capitalize()}")
            data_per_kat = df[df['kategori'] == kat]

            cols = st.columns(4)

            for index, row in data_per_kat.reset_index().iterrows():
                nama_foto = str(row['foto']).strip()

                with cols[index % 4]:
                    if os.path.exists(nama_foto):
                        st.image(nama_foto, use_container_width=True)
                        st.subheader(row['nama'])
                        st.markdown(f"### **Rp {row['harga']:,}**")
                        st.markdown(f"**Status:** {row['status']}")
                    else:
                        st.warning(f"Foto {nama_foto} tidak ditemukan")

            st.divider()
    else:
        st.error("File 'anggrekkel3.csv' tidak ditemukan!")

except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")

# Footer
st.divider()
st.subheader("📍 Hubungi Kami")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Alamat Galeri:**  
     Jl. C. Simanjuntak No.60, Terban, Kec. Gondokusuman, Kota Yogyakarta, Daerah Istimewa Yogyakarta 55223
    """)

with col2:
    no_hp = "6288215748030"
    pesan = "Halo, saya tertarik memesan anggrek di katalog Anda."
    link_wa = f"https://wa.me/{no_hp}?text={pesan.replace(' ', '%20')}"
    st.link_button("📱 Pesan via WhatsApp", link_wa)

st.caption("© 2026 Toko Anggrek Digital")
