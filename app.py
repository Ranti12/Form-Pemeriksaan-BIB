import streamlit as st
import pandas as pd
from datetime import date
from pathlib import Path
import uuid
import base64
from PIL import Image

# ---------- Konfigurasi dasar ----------
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / "uploads"
ASSETS_DIR = BASE_DIR / "assets"
DATA_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)
CSV_PATH = DATA_DIR / "pemeriksaan_bib.csv"
LOGO_PATH = ASSETS_DIR / "astra_isuzu_logo.png"

st.set_page_config(
    page_title="Formulir Pemeriksaan BIB",
    page_icon=Image.open(LOGO_PATH) if LOGO_PATH.exists() else "🔧",
    layout="centered",
)

COLUMNS = [
    "Timestamp", "Nama Mekanik", "Tanggal Pemeriksaan", "No. Polisi Kendaraan",
    "STNK", "Tanggal Berlaku STNK", "SIM Pengemudi",
    "Buku Kir", "Tanggal Berlaku Buku Kir",
    "Bukti Transfer Suku Cadang", "Surat Peminjaman Kendaraan (file)",
    "Barang Bawaan", "Sparepart", "Foto Sparepart (file)", "Toolkit",
]

# ---------- Warna brand Astra Isuzu ----------
BIRU = "#005BAF"
BIRU_GELAP = "#003D78"
BIRU_MUDA = "#CFE3F5"
MERAH = "#E30613"
PUTIH = "#FFFFFF"
ABU_BG = "#F2F4F7"
ABU_TEKS = "#4A4A4A"


def get_base64(path: Path) -> str:
    if not path.exists():
        return ""
    return base64.b64encode(path.read_bytes()).decode()


logo_b64 = get_base64(LOGO_PATH)

# ---------- CSS ----------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background-color: {PUTIH};
}}

#MainMenu, footer, header {{visibility: hidden;}}

.block-container {{
    padding-top: 1.5rem;
    max-width: 760px;
}}

/* ---- Header banner ---- */
.bib-header {{
    position: relative;
    background: linear-gradient(100deg, {BIRU} 0%, {BIRU} 55%, {MERAH} 55%, {MERAH} 100%);
    clip-path: polygon(0 0, 100% 0, 100% 78%, 0% 100%);
    border-radius: 18px;
    padding: 28px 32px 46px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
}}
.bib-header .bib-logo-box {{
    background: {PUTIH};
    border-radius: 10px;
    padding: 8px 14px;
    display: inline-flex;
    align-items: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.15);
}}
.bib-header img {{
    height: 40px;
    display: block;
}}
.bib-header .bib-title {{
    text-align: right;
}}
.bib-header .bib-title h1 {{
    font-family: 'Poppins', sans-serif;
    font-weight: 700;
    font-size: 22px;
    color: {PUTIH};
    margin: 0;
    letter-spacing: 0.3px;
}}
.bib-header .bib-title p {{
    font-family: 'Inter', sans-serif;
    font-size: 12.5px;
    color: {PUTIH} !important;
    margin: 2px 0 0 0;
}}
.bib-sub {{
    text-align: center;
    color: {ABU_TEKS};
    font-size: 13px;
    margin-bottom: 18px;
}}

/* ---- Section label ---- */
.bib-section {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    font-size: 15px;
    color: {PUTIH};
    padding: 6px 16px;
    border-radius: 8px;
    margin: 6px 0 14px 0;
}}
.bib-section.biru {{ background: {BIRU}; }}
.bib-section.merah {{ background: {MERAH}; }}

/* ---- Card container (st.container border) ---- */
div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: {ABU_BG};
    border-radius: 18px !important;
    border: 1.5px solid {BIRU} !important;
    padding: 6px 8px;
    margin-bottom: 16px;
}}

/* ---- Inputs ---- */
.stTextInput input, .stDateInput input, .stTextArea textarea {{
    border-radius: 8px !important;
    border: 1px solid #D6DCE5 !important;
    background: {PUTIH} !important;
    color: #1A1A1A !important;
}}
.stTextInput input::placeholder, .stTextArea textarea::placeholder {{
    color: #9AA3AF !important;
}}
label, .stMarkdown p, .stRadio label, .stDateInput label, .stTextInput label,
[data-testid="stWidgetLabel"] p {{
    color: #1A1A1A !important;
}}
.stTextInput input:focus, .stDateInput input:focus {{
    border-color: {BIRU} !important;
    box-shadow: 0 0 0 1px {BIRU} !important;
}}

/* ---- Radio (accent warna biru) ---- */
.stRadio [role="radiogroup"] label {{
    background: {PUTIH};
    padding: 6px 14px;
    border-radius: 20px;
    margin-right: 6px;
    border: 1px solid #D6DCE5;
}}
.stRadio [role="radiogroup"] label p,
.stRadio [role="radiogroup"] label span,
.stRadio [role="radiogroup"] label div {{
    color: #1A1A1A !important;
}}
input[type="radio"] {{ accent-color: {BIRU}; }}
.stRadio [role="radiogroup"] label [data-baseweb="radio"] div:first-child {{
    border-color: {BIRU} !important;
}}
.stRadio [role="radiogroup"] label [data-baseweb="radio"] div:first-child > div {{
    background-color: {BIRU} !important;
}}
.stRadio [role="radiogroup"] label svg {{
    fill: {BIRU} !important;
}}

/* ---- File uploader ---- */
[data-testid="stFileUploaderDropzone"] {{
    border-radius: 10px !important;
    border: 1.5px dashed {BIRU} !important;
    background: #F7FAFF !important;
}}
[data-testid="stFileUploaderDropzone"] p,
[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] small {{
    color: #1A1A1A !important;
}}

/* ---- Tombol submit (merah, sesuai logo) ---- */
div[data-testid="stFormSubmitButton"] button {{
    background: {MERAH} !important;
    color: {PUTIH} !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 10px 0 !important;
    transition: 0.15s ease;
}}
div[data-testid="stFormSubmitButton"] button:hover {{
    background: #C10510 !important;
}}
div[data-testid="stFormSubmitButton"] button p {{
    color: {PUTIH} !important;
}}

/* ---- Tombol biasa (download dsb, biru) ---- */
.stDownloadButton button {{
    background: {BIRU} !important;
    color: {PUTIH} !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}}
.stDownloadButton button:hover {{
    background: {BIRU_GELAP} !important;
}}
.stDownloadButton button p {{
    color: {PUTIH} !important;
}}

/* ---- Tabs ---- */
.stTabs [data-baseweb="tab-list"] {{
    gap: 8px;
    background: {PUTIH};
    padding: 5px;
    border-radius: 14px !important;
    border: 1px solid #E3E7EE;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 10px !important;
    overflow: hidden;
    font-weight: 600;
    background: {BIRU_MUDA} !important;
}}
.stTabs [data-baseweb="tab"],
.stTabs [data-baseweb="tab"] div,
.stTabs [data-baseweb="tab"] p,
.stTabs [data-baseweb="tab"] span {{
    color: {BIRU_GELAP} !important;
}}
.stTabs [aria-selected="true"] {{
    background: {BIRU} !important;
}}
.stTabs [aria-selected="true"],
.stTabs [aria-selected="true"] div,
.stTabs [aria-selected="true"] p,
.stTabs [aria-selected="true"] span {{
    color: {PUTIH} !important;
}}

/* ---- Metric ---- */
div[data-testid="stMetric"] {{
    background: {ABU_BG};
    border: 1px solid #E3E7EE;
    border-radius: 12px;
    padding: 10px 14px;
}}

/* ---- Footer ---- */
.bib-footer {{
    text-align: center;
    font-size: 12px;
    color: #9AA3AF;
    margin-top: 28px;
}}
.bib-footer b {{ color: {BIRU}; }}
.bib-footer span {{ color: {MERAH}; }}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown(f"""
<div class="bib-header">
    <div class="bib-logo-box">
        <img src="data:image/png;base64,{logo_b64}" />
    </div>
    <div class="bib-title">
        <h1>Formulir Pemeriksaan BIB</h1>
        <p>Bengkel Isuzu Berjalan &mdash; Astra Isuzu Cabang Waru</p>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('<div class="bib-sub">Isi checklist pemeriksaan kendaraan dan kelengkapan sebelum unit berangkat.</div>', unsafe_allow_html=True)


def load_data() -> pd.DataFrame:
    if CSV_PATH.exists():
        return pd.read_csv(CSV_PATH)
    return pd.DataFrame(columns=COLUMNS)


def save_row(row: dict):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(CSV_PATH, index=False)


def save_uploaded_file(uploaded_file, no_polisi: str, label: str) -> str:
    if uploaded_file is None:
        return ""
    safe_no_polisi = "".join(c for c in no_polisi if c.isalnum()) or "unknown"
    ext = Path(uploaded_file.name).suffix
    filename = f"{safe_no_polisi}_{label}_{uuid.uuid4().hex[:6]}{ext}"
    filepath = UPLOAD_DIR / filename
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return filename


tab_form, tab_data = st.tabs(["📝  Isi Formulir", "📊  Data Tersimpan"])

# ================= TAB 1: FORM =================
with tab_form:
    with st.form("form_pemeriksaan_bib", clear_on_submit=False, border=False):

        st.markdown('<div class="bib-section biru">🔵 Data Umum</div>', unsafe_allow_html=True)
        with st.container(border=True):
            nama_mekanik = st.text_input("Nama Mekanik *")
            tanggal_pemeriksaan = st.date_input("Tanggal Pemeriksaan *", value=date.today())
            no_polisi = st.text_input("No. Polisi Kendaraan *")

        st.markdown('<div class="bib-section merah">🔴 Dokumen Kendaraan</div>', unsafe_allow_html=True)
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                stnk = st.radio("STNK *", ["Berlaku", "Mati"], horizontal=True, key="stnk")
            with col2:
                tgl_stnk = st.date_input("Tanggal Berlaku STNK *", value=date.today(), key="tgl_stnk")

            sim_pengemudi = st.radio("SIM Pengemudi *", ["Berlaku", "Mati"], horizontal=True, key="sim")

            col3, col4 = st.columns(2)
            with col3:
                buku_kir = st.radio("Buku Kir *", ["Berlaku", "Mati"], horizontal=True, key="kir")
            with col4:
                tgl_kir = st.date_input("Tanggal Berlaku Buku Kir *", value=date.today(), key="tgl_kir")

            bukti_transfer = st.radio(
                "Bukti Transfer Suku Cadang *", ["Ada", "Tidak ada"], horizontal=True, key="bukti_transfer"
            )

            surat_peminjaman = st.file_uploader(
                "Surat Peminjaman Kendaraan * (upload file)",
                type=["pdf", "jpg", "jpeg", "png"],
                key="surat_peminjaman",
            )

        st.markdown('<div class="bib-section biru">🔵 Barang Bawaan</div>', unsafe_allow_html=True)
        with st.container(border=True):
            sparepart = st.radio("Sparepart *", ["Ada", "Tidak ada"], horizontal=True, key="sparepart")

            foto_sparepart = st.file_uploader(
                "Foto Sparepart (opsional)",
                type=["jpg", "jpeg", "png"],
                key="foto_sparepart",
            )

            toolkit = st.radio("Toolkit *", ["Ada", "Tidak ada"], horizontal=True, key="toolkit")

        submitted = st.form_submit_button("Kirim Formulir", use_container_width=True)

        if submitted:
            errors = []
            if not nama_mekanik.strip():
                errors.append("Nama Mekanik wajib diisi.")
            if not no_polisi.strip():
                errors.append("No. Polisi Kendaraan wajib diisi.")
            if surat_peminjaman is None:
                errors.append("Surat Peminjaman Kendaraan wajib diupload.")

            if errors:
                for e in errors:
                    st.error(e)
            else:
                surat_filename = save_uploaded_file(surat_peminjaman, no_polisi, "surat_peminjaman")
                foto_filename = save_uploaded_file(foto_sparepart, no_polisi, "foto_sparepart")

                row = {
                    "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Nama Mekanik": nama_mekanik.strip(),
                    "Tanggal Pemeriksaan": tanggal_pemeriksaan.strftime("%Y-%m-%d"),
                    "No. Polisi Kendaraan": no_polisi.strip().upper(),
                    "STNK": stnk,
                    "Tanggal Berlaku STNK": tgl_stnk.strftime("%Y-%m-%d"),
                    "SIM Pengemudi": sim_pengemudi,
                    "Buku Kir": buku_kir,
                    "Tanggal Berlaku Buku Kir": tgl_kir.strftime("%Y-%m-%d"),
                    "Bukti Transfer Suku Cadang": bukti_transfer,
                    "Surat Peminjaman Kendaraan (file)": surat_filename,
                    "Barang Bawaan": "",
                    "Sparepart": sparepart,
                    "Foto Sparepart (file)": foto_filename,
                    "Toolkit": toolkit,
                }
                save_row(row)
                st.success("Data pemeriksaan berhasil disimpan! ✅")

# ================= TAB 2: DATA =================
with tab_data:
    st.markdown('<div class="bib-section biru">📊 Rekap Data Pemeriksaan</div>', unsafe_allow_html=True)
    df = load_data()

    if df.empty:
        st.info("Belum ada data yang masuk.")
    else:
        with st.container(border=True):
            st.dataframe(df, use_container_width=True, hide_index=True)

        colA, colB = st.columns(2)
        with colA:
            st.metric("Total Data Masuk", len(df))
        with colB:
            st.metric("STNK Mati", int((df["STNK"] == "Mati").sum()) if "STNK" in df.columns else 0)

        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️  Download CSV",
            data=csv_bytes,
            file_name="pemeriksaan_bib.csv",
            mime="text/csv",
            use_container_width=True,
        )

st.markdown(
    '<div class="bib-footer">Formulir Pemeriksaan BIB &middot; <b>ASTRA</b> <span>ISUZU</span> Cabang Waru</div>',
    unsafe_allow_html=True,
)
