import streamlit as st
import pandas as pd

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Data Generus Desa 1", layout="wide")

# --- DATABASE TARGET LENGKAP ---
TARGET_MASTER = {
    "Kelas A": {
        "Tahun Pertama": {
            "Juli": {"quran": "Al Angkabut 45 - Arrum 24", "hadist": "Kitabussholah 1-18", "surat": "An-Nas s/d Al-Kafirun", "doa": "Doa kumpulan nabi muhammad", "dalil": "Mengaji (2 dalil)"},
            "Agustus": {"quran": "Arrum 25 - Luqman 11", "hadist": "Kitabussholah 19-36", "surat": "Al-Kausar s/d Al-Fil", "doa": "Doa berlindung amal jelek", "dalil": "Mengamal (2 dalil)"},
            # ... (data lainnya tetap sama)
        },
        # ... (Tahun Kedua, dll tetap sama)
    }
    # Tambahkan Kelas B dan C di sini seperti kode aslimu
}

# 2. SIDEBAR (INPUT IDENTITAS)
with st.sidebar:
    st.header("👤 Data Input")
    nama = st.text_input("Nama Lengkap")
    kelompok = st.selectbox("Pilih Kelompok", ["LA 1", "LA 2", "C 1", "C 2", "C 3", "RT 7", "D 1"])
    kls = st.selectbox("Pilih Kelas", ["Kelas A", "Kelas B", "Kelas C"])
    thn = st.radio("Pilih Tahun", ["Tahun Pertama", "Tahun Kedua"])
    bln = st.selectbox("Pilih Bulan", ["Juli", "Agustus", "September", "Oktober", "November", "Desember", "Januari", "Februari", "Maret", "April", "Mei", "Juni"])

st.title("📊 Sistem Evaluasi Kurikulum Generus")

# 3. TAMPILKAN TARGET
target = TARGET_MASTER.get(kls, {}).get(thn, {}).get(bln, {"quran": "-", "hadist": "-", "surat": "-", "doa": "-", "dalil": "-"})
st.info(f"🎯 **Target {bln} ({thn}) untuk {kls}:**")
t_col1, t_col2 = st.columns(2)
with t_col1:
    st.write(f"📖 **Quran:** {target.get('quran', '-')}")
    st.write(f"📜 **Hadist:** {target.get('hadist', '-')}")
    st.write(f"🕋 **Surat:** {target.get('surat', '-')}")
with t_col2:
    st.write(f"🙏 **Doa:** {target.get('doa', '-')}")
    st.write(f"💡 **Dalil:** {target.get('dalil', '-')}")

st.divider()

# 4. BAGIAN PENILAIAN
st.subheader("📉 Detail Penilaian Persentase (%)")

def input_materi_detail(label, key_p):
    with st.expander(f"Penilaian {label}", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1: m = st.number_input(f"Materi {label} (%)", 0, 100, 0, key=f"{key_p}m")
        with c2: n = st.number_input(f"Makna {label} (%)", 0, 100, 0, key=f"{key_p}n")
        with c3: k = st.number_input(f"Ket {label} (%)", 0, 100, 0, key=f"{key_p}k")
    return (m + n + k) / 3

col_q, col_h = st.columns(2)
with col_q: total_q = input_materi_detail("Al-Quran", "q")
with col_h: total_h = input_materi_detail("Al-Hadist", "h")

st.markdown("#### Penilaian Hafalan")
col_s, col_d, col_l = st.columns(3)
with col_s: total_s = st.number_input("Hafalan Surat (%)", 0, 100, 0)
with col_d: total_d = st.number_input("Hafalan Doa (%)", 0, 100, 0)
with col_l: total_l = st.number_input("Hafalan Dalil (%)", 0, 100, 0)

# 5. LOGIKA PENYIMPANAN (SESUDAH VARIABEL NILAI DIBUAT)
avg = (total_q + total_h + total_s + total_d + total_l) / 5

if st.button("💾 SIMPAN DATA EVALUASI", use_container_width=True):
    if nama:
        # Simpan ke Session State (Lokal)
        if "rekap" not in st.session_state: st.session_state.rekap = []
        data_baru = {
            "Nama": nama, "Kelompok": kelompok, "Kelas": kls, "Tahun": thn, "Bulan": bln,
            "Quran": f"{total_q:.1f}%", "Hadist": f"{total_h:.1f}%",
            "Surat": f"{total_s}%", "Doa": f"{total_d}%", "Dalil": f"{total_l}%",
            "Rata-rata": f"{avg:.1f}%"
        }
        st.session_state.rekap.append(data_baru)
        
    else:
        st.warning("Nama harus diisi!")

# 6. REKAP TABEL
if "rekap" in st.session_state:
    st.subheader("📋 Rekapitulasi Nilai (Sesi Ini)")
    st.dataframe(pd.DataFrame(st.session_state.rekap), use_container_width=True)
