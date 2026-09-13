import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(page_title="Pembukuan Pemuda Kotobaru", page_icon="💰", layout="wide")

# --- Konfigurasi Password Admin ---
def get_admin_password():
    try:
        return st.secrets.get("ADMIN_PASSWORD", "admin123")
    except Exception:
        return "admin123"

ADMIN_PASSWORD = get_admin_password()

# --- Setup Database SQLite ---
def init_db():
    conn = sqlite3.connect('kas_kotobaru.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS kas
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, tanggal TEXT, jenis TEXT, kategori TEXT, jumlah REAL, keterangan TEXT)''')
    conn.commit()
    return conn

conn = init_db()

def format_rp(val):
    if pd.isna(val) or val == 0:
        return "-"
    return f"Rp {val:,.0f}"

def get_ledger_df():
    """Mengambil semua data dan menghitung kas masuk, keluar, serta saldo berjalan."""
    df = pd.read_sql_query("SELECT * FROM kas ORDER BY tanggal ASC, id ASC", conn)
    if df.empty:
        return df
    
    df['Uang Masuk (Rp)'] = df.apply(lambda r: r['jumlah'] if r['jenis'] == 'Pemasukan' else 0.0, axis=1)
    df['Uang Keluar (Rp)'] = df.apply(lambda r: r['jumlah'] if r['jenis'] == 'Pengeluaran' else 0.0, axis=1)
    df['Saldo (Rp)'] = (df['Uang Masuk (Rp)'] - df['Uang Keluar (Rp)']).cumsum()
    return df

# --- Session State Login ---
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

st.title("💰 Pembukuan Kas Organisasi Pemuda Kotobaru")
st.caption("Transparansi & Pengelolaan Keuangan yang Rapi dan Terpercaya")

# --- Sidebar: Akses ---
st.sidebar.header("🔐 Hak Akses")
if st.session_state.is_admin:
    st.sidebar.success("Status: **Admin** 👑")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.is_admin = False
        st.rerun()
else:
    st.sidebar.info("Status: **Anggota** 👀")
    with st.sidebar.expander("🔑 Login Admin"):
        pwd = st.text_input("Password", type="password")
        if st.button("Masuk"):
            if pwd == ADMIN_PASSWORD:
                st.session_state.is_admin = True
                st.rerun()
            else:
                st.error("Salah!")

is_admin = st.session_state.is_admin

# --- Menu ---
if is_admin:
    menu = ["📊 Dashboard & Buku Kas", "📝 Input Kas Baru", "🛠️ Edit / Hapus Data"]
else:
    menu = ["📊 Dashboard & Buku Kas", "📋 Rincian Transparansi"]

pilihan = st.sidebar.radio("Navigasi", menu)

# ================= 1. DASHBOARD & TABEL TERPISAH =================
if "Dashboard" in pilihan or "Rincian" in pilihan:
    df_raw = get_ledger_df()
    
    if not df_raw.empty:
        total_masuk = df_raw['Uang Masuk (Rp)'].sum()
        total_keluar = df_raw['Uang Keluar (Rp)'].sum()
        saldo_akhir = total_masuk - total_keluar
        
        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Saldo Akhir", format_rp(saldo_akhir))
        col2.metric("📈 Total Pemasukan", format_rp(total_masuk))
        col3.metric("📉 Total Pengeluaran", format_rp(total_keluar))
        
        st.markdown("---")
        
        tab1, tab2, tab3 = st.tabs(["📑 Buku Kas Umum", "💵 Pemasukan", "💸 Pengeluaran"])
        
        with tab1:
            st.subheader("Semua Riwayat Transaksi")
            df_all = df_raw.copy()
            df_all['Debit'] = df_all['Uang Masuk (Rp)'].apply(format_rp)
            df_all['Kredit'] = df_all['Uang Keluar (Rp)'].apply(format_rp)
            df_all['Saldo'] = df_all['Saldo (Rp)'].apply(format_rp)
            st.dataframe(df_all[['tanggal', 'kategori', 'keterangan', 'Debit', 'Kredit', 'Saldo']], use_container_width=True, hide_index=True)

        with tab2:
            st.subheader("Rincian Uang Masuk")
            df_in = df_raw[df_raw['jenis'] == 'Pemasukan'].copy()
            df_in['Jumlah'] = df_in['jumlah'].apply(format_rp)
            st.dataframe(df_in[['tanggal', 'kategori', 'keterangan', 'Jumlah']], use_container_width=True, hide_index=True)
            st.info(f"Total Masuk: **{format_rp(total_masuk)}**")

        with tab3:
            st.subheader("Rincian Uang Keluar")
            df_out = df_raw[df_raw['jenis'] == 'Pengeluaran'].copy()
            df_out['Jumlah'] = df_out['jumlah'].apply(format_rp)
            st.dataframe(df_out[['tanggal', 'kategori', 'keterangan', 'Jumlah']], use_container_width=True, hide_index=True)
            st.info(f"Total Keluar: **{format_rp(total_keluar)}**")
            
        csv = df_raw.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Laporan (CSV)", csv, f"Laporan_Kas_{datetime.today().strftime('%Y%m%d')}.csv", "text/csv")
    else:
        st.info("Belum ada data.")

# ================= 2. INPUT DATA (ADMIN) =================
elif pilihan == "📝 Input Kas Baru":
    st.header("📝 Tambah Catatan Kas")
    with st.form("input"):
        c1, c2 = st.columns(2)
        tgl = c1.date_input("Tanggal", value=datetime.today())
        jns = c1.selectbox("Jenis", ["Pemasukan", "Pengeluaran"])
        kat = c2.selectbox("Kategori", ["Iuran", "Donasi", "Kegiatan", "Konsumsi", "Lainnya"])
        jml = c2.number_input("Nominal (Rp)", min_value=0.0, step=1000.0)
        ket = st.text_area("Keterangan")
        if st.form_submit_button("Simpan"):
            c = conn.cursor()
            c.execute("INSERT INTO kas (tanggal, jenis, kategori, jumlah, keterangan) VALUES (?,?,?,?,?)",
                      (str(tgl), jns, kat, jml, ket))
            conn.commit()
            st.success("Tersimpan!")
            st.rerun()

# ================= 3. EDIT/HAPUS (ADMIN) =================
elif pilihan == "🛠️ Edit / Hapus Data":
    st.header("🛠️ Kelola Data")
    df = pd.read_sql_query("SELECT * FROM kas ORDER BY id DESC", conn)
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        id_sel = st.selectbox("Pilih ID", df['id'].tolist())
        row = df[df['id'] == id_sel].iloc[0]
        with st.form("edit"):
            e_tgl = st.text_input("Tanggal", value=row['tanggal'])
            e_jns = st.selectbox("Jenis", ["Pemasukan", "Pengeluaran"], index=0 if row['jenis']=='Pemasukan' else 1)
            e_kat = st.text_input("Kategori", value=row['kategori'])
            e_jml = st.number_input("Nominal", value=float(row['jumlah']))
            e_ket = st.text_area("Keterangan", value=row['keterangan'])
            if st.form_submit_button("Update"):
                conn.execute("UPDATE kas SET tanggal=?, jenis=?, kategori=?, jumlah=?, keterangan=? WHERE id=?", (e_tgl, e_jns, e_kat, e_jml, e_ket, id_sel))
                conn.commit()
                st.rerun()
            if st.form_submit_button("Hapus"):
                conn.execute("DELETE FROM kas WHERE id=?", (id_sel,))
                conn.commit()
                st.rerun()
