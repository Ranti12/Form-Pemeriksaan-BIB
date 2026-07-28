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
MERAH_MUDA = "#FCE0E2"
PUTIH = "#FFFFFF"
ABU_BG = "#F2F4F7"
ABU_TEKS = "#4A4A4A"


def get_base64(path: Path) -> str:
    if not path.exists():
        return ""
    return base64.b64encode(path.read_bytes()).decode()


logo_b64 = get_base64(LOGO_PATH)

# ---------- Session state ----------
if "errors" not in st.session_state:
    st.session_state.errors = {}
if "just_submitted" not in st.session_state:
    st.session_state.just_submitted = False

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
    margin-bottom: 14px;
}}

/* ---- Progress indicator ---- */
.bib-progress {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    margin: 4px 0 22px 0;
    flex-wrap: wrap;
}}
.bib-progress-step {{
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    font-weight: 600;
    color: {ABU_TEKS};
    white-space: nowrap;
}}
.bib-progress-step span {{
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: {BIRU};
    color: {PUTIH};
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-family: 'Poppins', sans-serif;
    flex-shrink: 0;
}}
.bib-progress-line {{
    width: 26px;
    height: 2px;
    background: #D6DCE5;
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
    box-shadow: 0 2px 0 rgba(0,0,0,0.08);
}}
.bib-section.biru {{ background: {BIRU}; }}
.bib-section.merah {{ background: {MERAH}; }}

/* ---- Card container (st.container border) ---- */
div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: {ABU_BG};
    border-radius: 18px !important;
    border: 1.5px solid #E3E7EE !important;
    padding: 6px 8px;
    margin-bottom: 16px;
}}

/* ---- Card top accent strip ---- */
.card-accent {{
    height: 4px;
    border-radius: 4px;
    margin: 2px 4px 12px 4px;
}}
.card-accent.biru {{ background: {BIRU}; }}
.card-accent.merah {{ background: {MERAH}; }}

/* ---- Custom field label + required star ---- */
.bib-label {{
    font-weight: 600;
    font-size: 14px;
    color: #1A1A1A;
    margin: 2px 0 4px 2px;
}}
.req-star {{
    color: {MERAH};
    font-weight: 700;
}}

/* ---- Inline field error ---- */
.field-error {{
    color: {MERAH};
    background: {MERAH_MUDA};
    font-size: 12px;
    font-weight: 500;
    padding: 4px 10px;
    border-radius: 6px;
    margin: -6px 2px 12px 2px;
    display: inline-block;
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

/* ---- Radio (accent warna biru + highlight saat dipilih) ---- */
.stRadio [role="radiogroup"] label {{
    background: {PUTIH};
    padding: 6px 14px;
    border-radius: 20px;
    margin-right: 6px;
    border: 1px solid #D6DCE5;
    transition: 0.15s ease;
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
.stRadio [role="radiogroup"] label:has(input:checked) {{
    background: {BIRU_MUDA} !important;
    border-color: {BIRU} !important;
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

/* ---- Success card ---- */
.bib-success {{
    display: flex;
    align-items: center;
    gap: 12px;
    background: #E9F7EF;
    border: 1.5px solid #34A853;
    border-radius: 14px;
    padding: 14px 18px;
    margin: 8px 0 16px 0;
}}
.bib-success .icon {{
    font-size: 26px;
}}
.bib-success .text b {{
    display: block;
    color: #1E7E34;
    font-size: 15px;
    font-family: 'Poppins', sans-serif;
}}
.bib-success .text span {{
    color: #3C763D;
    font-size: 12.5px;
}}

/* ---- File preview caption ---- */
.bib-file-preview {{
    font-size: 12.5px;
    color: {ABU_TEKS};
    margin: -4px 0 10px 2px;
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

/* ---- Mobile responsiveness ---- */
@media (max-width: 480px) {{
    .block-container {{
        padding-left: 12px;
        padding-right: 12px;
    }}
    .bib-header {{
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
        padding: 20px 18px 34px 18px;
    }}
    .bib-header .bib-title {{
        text-align: left;
    }}
    .bib-header .bib-title h1 {{
        font-size: 18px;
    }}
    .bib-progress-step {{
        font-size: 11px;
    }}
    .bib-progress-line {{
        width: 16px;
    }}
    .stRadio [role="radiogroup"] {{
        flex-wrap: wrap;
    }}
    div[data-testid="stFileUploaderDropzone"] {{
        min-height: 84px;
    }}
}}
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

# ---------- Progress indicator ----------
st.markdown("""
<div class="bib-progress">
    <div class="bib-progress-step"><span>1</span>Data Umum</div>
    <div class="bib-progress-line"></div>
    <div class="bib-progress-step"><span>2</span>Dokumen</div>
    <div class="bib-progress-line"></div>
    <div class="bib-progress-step"><span>3</span>Barang Bawaan</div>
</div>
""", unsafe_allow_html=True)


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


def field_label(text: str, required: bool = True):
    star = ' <span class="req-star">*</span>' if required else ""
    st.markdown(f'<div class="bib-label">{text}{star}</div>', unsafe_allow_html=True)


def show_error(field_key: str):
    msg = st.session_state.errors.get(field_key)
    if msg:
        st.markdown(f'<div class="field-error">⚠️ {msg}</div>', unsafe_allow_html=True)


def show_file_preview(uploaded_file, empty_hint: str = ""):
    if uploaded_file is None:
        if empty_hint:
            st.markdown(f'<div class="bib-file-preview">{empty_hint}</div>', unsafe_allow_html=True)
        return
    if uploaded_file.type is not None and uploaded_file.type.startswith("image"):
        st.image(uploaded_file, width=160)
    else:
        st.markdown(f'<div class="bib-file-preview">📄 File terpilih: <b>{uploaded_file.name}</b></div>', unsafe_allow_html=True)


tab_form, tab_data = st.tabs(["📝  Isi Formulir", "📊  Data Tersimpan"])

# ================= TAB 1: FORM =================
with tab_form:

    if st.session_state.just_submitted:
        st.markdown("""
        <div class="bib-success">
            <div class="icon">✅</div>
            <div class="text">
                <b>Data pemeriksaan berhasil disimpan!</b>
                <span>Silakan isi formulir baru untuk kendaraan berikutnya.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
        st.session_state.just_submitted = False

    with st.form("form_pemeriksaan_bib", clear_on_submit=False, border=False):

        st.markdown('<div class="bib-section biru">🔵 Data Umum</div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown('<div class="card-accent biru"></div>', unsafe_allow_html=True)

            field_label("Nama Mekanik")
            nama_mekanik = st.text_input("Nama Mekanik", label_visibility="collapsed")
            show_error("nama_mekanik")

            field_label("Tanggal Pemeriksaan")
            tanggal_pemeriksaan = st.date_input("Tanggal Pemeriksaan", value=date.today(), label_visibility="collapsed")

            field_label("No. Polisi Kendaraan")
            no_polisi = st.text_input("No. Polisi Kendaraan", label_visibility="collapsed")
            show_error("no_polisi")

        st.markdown('<div class="bib-section merah">🔴 Dokumen Kendaraan</div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown('<div class="card-accent merah"></div>', unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                field_label("STNK")
                stnk = st.radio("STNK", ["Berlaku", "Mati"], horizontal=True, key="stnk", label_visibility="collapsed")
            with col2:
                field_label("Tanggal Berlaku STNK")
                tgl_stnk = st.date_input("Tanggal Berlaku STNK", value=date.today(), key="tgl_stnk", label_visibility="collapsed")

            field_label("SIM Pengemudi")
            sim_pengemudi = st.radio("SIM Pengemudi", ["Berlaku", "Mati"], horizontal=True, key="sim", label_visibility="collapsed")

            col3, col4 = st.columns(2)
            with col3:
                field_label("Buku Kir")
                buku_kir = st.radio("Buku Kir", ["Berlaku", "Mati"], horizontal=True, key="kir", label_visibility="collapsed")
            with col4:
                field_label("Tanggal Berlaku Buku Kir")
                tgl_kir = st.date_input("Tanggal Berlaku Buku Kir", value=date.today(), key="tgl_kir", label_visibility="collapsed")

            field_label("Bukti Transfer Suku Cadang")
            bukti_transfer = st.radio(
                "Bukti Transfer Suku Cadang", ["Ada", "Tidak ada"], horizontal=True, key="bukti_transfer", label_visibility="collapsed"
            )

            field_label("Surat Peminjaman Kendaraan (upload file)")
            surat_peminjaman = st.file_uploader(
                "Surat Peminjaman Kendaraan",
                type=["pdf", "jpg", "jpeg", "png"],
                key="surat_peminjaman",
                label_visibility="collapsed",
            )
            show_file_preview(surat_peminjaman)
            show_error("surat_peminjaman")

        st.markdown('<div class="bib-section biru">🔵 Barang Bawaan</div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown('<div class="card-accent biru"></div>', unsafe_allow_html=True)

            field_label("Sparepart")
            sparepart = st.radio("Sparepart", ["Ada", "Tidak ada"], horizontal=True, key="sparepart", label_visibility="collapsed")

            field_label("Foto Sparepart", required=False)
            foto_sparepart = st.file_uploader(
                "Foto Sparepart",
                type=["jpg", "jpeg", "png"],
                key="foto_sparepart",
                label_visibility="collapsed",
            )
            show_file_preview(foto_sparepart)

            field_label("Toolkit")
            toolkit = st.radio("Toolkit", ["Ada", "Tidak ada"], horizontal=True, key="toolkit", label_visibility="collapsed")

        submitted = st.form_submit_button("✓  Kirim Formulir", use_container_width=True)

        if submitted:
            errors = {}
            if not nama_mekanik.strip():
                errors["nama_mekanik"] = "Nama Mekanik wajib diisi."
            if not no_polisi.strip():
                errors["no_polisi"] = "No. Polisi Kendaraan wajib diisi."
            if surat_peminjaman is None:
                errors["surat_peminjaman"] = "Surat Peminjaman Kendaraan wajib diupload."

            if errors:
                st.session_state.errors = errors
                st.rerun()
            else:
                st.session_state.errors = {}
                with st.spinner("Menyimpan data..."):
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
                st.session_state.just_submitted = True
                st.rerun()

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
