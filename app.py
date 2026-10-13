import datetime
import altair as alt
import pandas as pd
import requests
import streamlit as st

# Konfigurasi Halaman Utama
st.set_page_config(
    page_title="Malailak Financial Report",
    page_icon="🌟",
    layout="wide",
)

# --- PENGATURAN URL GOOGLE APPS SCRIPT ---
try:
  APPS_SCRIPT_URL = st.secrets["APPS_SCRIPT_URL"]
except:
  APPS_SCRIPT_URL = "URL_WEB_APP_ANDA_DISINI"

# --- FUNGSI AMBIL & KIRIM DATA KE GOOGLE SHEETS ---


def load_data_from_sheets():
  if not APPS_SCRIPT_URL or APPS_SCRIPT_URL == "URL_WEB_APP_ANDA_DISINI":
    return pd.DataFrame([
        {
            "Tanggal": "2026-10-01",
            "Member": "Petrus 👨",
            "Tipe": "Income",
            "Kategori": "Gaji 💰",
            "Nominal": 15000000,
            "Catatan": "Gaji Bulanan",
        }
    ])
  try:
    response = requests.get(APPS_SCRIPT_URL)
    data = response.json()
    if data:
      df = pd.DataFrame(data)
      df["Nominal"] = pd.to_numeric(df["Nominal"], errors="coerce").fillna(0)
      return df
    else:
      return pd.DataFrame(
          columns=["Tanggal", "Member", "Tipe", "Kategori", "Nominal", "Catatan"]
      )
  except Exception as e:
    st.error(f"Gagal memuat data dari Google Sheets: {e}")
    return pd.DataFrame(
        columns=["Tanggal", "Member", "Tipe", "Kategori", "Nominal", "Catatan"]
    )


def save_data_to_sheets(row_data):
  if not APPS_SCRIPT_URL or APPS_SCRIPT_URL == "URL_WEB_APP_ANDA_DISINI":
    return False
  try:
    response = requests.post(APPS_SCRIPT_URL, json=row_data)
    result = response.json()
    return result.get("status") == "success"
  except Exception as e:
    st.error(f"Gagal menyimpan data ke Google Sheets: {e}")
    return False


# --- CUSTOM CSS: DESAIN & PERBAIKAN WARNA TEKS MENU ---
st.markdown(
    """
    <style>
    .stApp { background-color: #f8fafc; }
    
    /* Memastikan teks menu navigasi horizontal terlihat jelas dan tidak transparan */
    .stRadio div[role="radiogroup"] label p {
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 15px !important;
    }
    
    .main-header {
        background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
        padding: 20px 30px;
        border-radius: 16px;
        color: white;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        margin-bottom: 25px;
    }
    .main-header h1 { margin: 0; font-size: 28px; font-weight: 800; letter-spacing: -0.5px; }
    .main-header p { margin: 5px 0 0 0; font-size: 14px; opacity: 0.9; }

    .custom-card {
        padding: 20px;
        border-radius: 14px;
        color: white;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 10px;
    }
    .card-income { background: linear-gradient(135deg, #10b981, #047857); }
    .card-expense { background: linear-gradient(135deg, #f43f5e, #be123c); }
    .card-saving { background: linear-gradient(135deg, #8b5cf6, #6d28d9); }
    .card-balance { background: linear-gradient(135deg, #0284c7, #0369a1); }
    
    .c-title { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; opacity: 0.9; }
    .c-value { font-size: 24px; font-weight: 800; margin-top: 5px; }
    
    .kid-box {
        background: #ffffff;
        border: 3px dashed #38bdf8;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.15);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- AMBIL DATA DARI GOOGLE SHEETS & INISIALISASI SESSION STATE ---
if "data_transaksi" not in st.session_state:
  st.session_state["data_transaksi"] = load_data_from_sheets()

if "list_member" not in st.session_state:
  st.session_state["list_member"] = [
      "Petrus 👨",
      "Mommy 👩",
      "Kia 👧",
      "Juna 👦 (6 Tahun)",
      "Extended Cost 🏡",
  ]

if "kategori_by_tipe" not in st.session_state:
  st.session_state["kategori_by_tipe"] = {
      "Income": ["Gaji 💰", "Tambahan Gaji 💵", "Hadiah 🎁", "Lainnya ✨"],
      "Expenses": [
          "Jajan / Makanan 🍔",
          "Belanja Bulanan 🛒",
          "Mainan / Hobi 🧸",
          "Listrik & Air ⚡",
          "Transport 🚗",
          "Lainnya ✨",
      ],
      "Top Up Saving": ["Tabungan Celengan 🏦", "Deposit Anak 📈"],
      "Withdraw Saving": ["Ambil Tabungan 💸"],
  }

df = st.session_state["data_transaksi"]
list_member = st.session_state["list_member"]
kategori_by_tipe = st.session_state["kategori_by_tipe"]
all_types = ["Income", "Expenses", "Top Up Saving", "Withdraw Saving"]

# --- HEADER UTAMA APLIKASI ---
st.markdown(
    """
    <div class="main-header">
        <h1>🌟 Malailak Financial Report</h1>
        <p>Sistem Manajemen Keuangan Keluarga Terintegrasi & Ramah Anak (Cloud Sheets)</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Navigasi Menu Atas Horizontal Asli
menu = st.radio(
    "Navigasi",
    [
        "📊 Dashboard Utama & Filter",
        "🎮 Input",
        "🗂️ Riwayat",
        "⚙️ Pengaturan (Admin)",
    ],
    horizontal=True,
    label_visibility="collapsed",
)

st.markdown("<br>", unsafe_allow_html=True)

# --- HALAMAN 1: DASHBOARD UTAMA & FILTER ---
if menu == "📊 Dashboard Utama & Filter":

  col_ref1, col_ref2 = st.columns([5, 1])
  with col_ref2:
    if st.button("🔄 Refresh Data", use_container_width=True):
      st.session_state["data_transaksi"] = load_data_from_sheets()
      st.rerun()

  st.subheader("📌 Grand Total Keuangan Keluarga (Global)")
  if not df.empty:
    g_income = df[df["Tipe"] == "Income"]["Nominal"].sum()
    g_expense = df[df["Tipe"] == "Expenses"]["Nominal"].sum()
    g_saving = df[df["Tipe"] == "Top Up Saving"]["Nominal"].sum()
    g_sisa = g_income - g_expense
  else:
    g_income, g_expense, g_saving, g_sisa = 0, 0, 0, 0

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.markdown(
        f'<div class="custom-card card-income"><div class="c-title">Total Pemasukan</div><div class="c-value">Rp {g_income:,.0f}</div></div>',
        unsafe_allow_html=True,
    )
  with col2:
    st.markdown(
        f'<div class="custom-card card-expense"><div class="c-title">Total Pengeluaran</div><div class="c-value">Rp {g_expense:,.0f}</div></div>',
        unsafe_allow_html=True,
    )
  with col3:
    st.markdown(
        f'<div class="custom-card card-saving"><div class="c-title">Total Tabungan</div><div class="c-value">Rp {g_saving:,.0f}</div></div>',
        unsafe_allow_html=True,
    )
  with col4:
    st.markdown(
        f'<div class="custom-card card-balance"><div class="c-title">Sisa Dana Net</div><div class="c-value">Rp {g_sisa:,.0f}</div></div>',
        unsafe_allow_html=True,
    )

  st.markdown("<br>", unsafe_allow_html=True)
  st.subheader("📊 Visualisasi Grafik Kondisi Grand Total")
  st.markdown(
      "💡 *Tip: Klik atau tap salah satu batang grafik di bawah untuk melihat"
      " hingga 20 history transaksi terakhir.*"
  )

  df_grand = pd.DataFrame({
      "Komponen": ["Pemasukan", "Pengeluaran", "Tabungan", "Sisa Dana Net"],
      "Nominal": [g_income, g_expense, g_saving, g_sisa],
      "Warna": ["#10b981", "#f43f5e", "#8b5cf6", "#0284c7"],
  })

  select_gt = alt.selection_point(fields=["Komponen"], name="select_gt")

  base_gt = alt.Chart(df_grand).encode(
      x=alt.X(
          "Komponen:N",
          sort=None,
          axis=alt.Axis(
              labelAngle=0,
              labelColor="black",
              labelFontWeight="bold",
              title=None,
          ),
      ),
      y=alt.Y(
          "Nominal:Q",
          axis=alt.Axis(
              labelColor="black", labelFontWeight="bold", title="Nominal (Rp)"
          ),
      ),
      color=alt.Color("Warna:N", scale=None),
  )

  bars_gt = (
      base_gt.mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
      .encode(
          opacity=alt.condition(select_gt, alt.value(1), alt.value(0.3)),
          tooltip=[
              alt.Tooltip("Komponen", title="Komponen"),
              alt.Tooltip("Nominal", title="Nominal (Rp)", format=",.0f"),
          ],
      )
      .add_params(select_gt)
  )

  text_gt = base_gt.mark_text(
      align="center", baseline="bottom", dy=-5, fontWeight="bold", color="black"
  ).encode(text=alt.Text("Nominal:Q", format=",.0f"))

  chart_gt = (bars_gt + text_gt).properties(height=300)

  event_gt = st.altair_chart(
      chart_gt, use_container_width=True, on_select="rerun"
  )

  selected_gt_points = (
      event_gt.get("selection", {}).get("select_gt", [])
      if isinstance(event_gt, dict)
      else []
  )

  if selected_gt_points:
    clicked_komponen = selected_gt_points[0].get("Komponen")
    st.markdown(
        f"### 🔍 20 History Transaksi Terakhir untuk: **{clicked_komponen}**"
    )

    if clicked_komponen == "Pemasukan":
      df_sub = df[df["Tipe"] == "Income"]
    elif clicked_komponen == "Pengeluaran":
      df_sub = df[df["Tipe"] == "Expenses"]
    elif clicked_komponen == "Tabungan":
      df_sub = df[df["Tipe"] == "Top Up Saving"]
    else:
      df_sub = df[df["Tipe"].isin(["Income", "Expenses"])]

    st.dataframe(df_sub.tail(20), use_container_width=True)

  st.markdown("---")

  col_title_f, col_btn_f = st.columns([4, 1])
  with col_title_f:
    st.subheader("🔍 Filter & Analisis Data Kustom")
  with col_btn_f:
    if st.button("🧹 Clear Filter", use_container_width=True):
      st.session_state["sel_members"] = []
      st.session_state["sel_types"] = []
      st.session_state["time_mode"] = "Semua Waktu"
      st.session_state["sel_cats"] = []
      st.rerun()

  f_col1, f_col2, f_col3 = st.columns(3)
  with f_col1:
    sel_members = st.multiselect(
        "Pilih Member",
        list_member,
        default=[],
        key="sel_members",
        placeholder="Pilih member...",
    )
  with f_col2:
    sel_types = st.multiselect(
        "Pilih Tipe Transaksi",
        all_types,
        default=[],
        key="sel_types",
        placeholder="Pilih tipe...",
    )
  with f_col3:
    time_mode = st.selectbox(
        "Pilih Periode Waktu",
        [
            "Semua Waktu",
            "This Year to Date (Tahun Ini)",
            "Pilih Tahun Tertentu",
            "Rentang Tanggal Kustom",
        ],
        key="time_mode",
    )

    today = datetime.date.today()
    if time_mode == "This Year to Date (Tahun Ini)":
      start_date = datetime.date(today.year, 1, 1)
      end_date = today
    elif time_mode == "Pilih Tahun Tertentu":
      chosen_year = st.selectbox("Pilih Tahun", [2026, 2025, 2024, 2023], index=0)
      start_date = datetime.date(chosen_year, 1, 1)
      end_date = datetime.date(chosen_year, 12, 31)
    elif time_mode == "Rentang Tanggal Kustom":
      custom_range = st.date_input(
          "Rentang Tanggal", value=[datetime.date(today.year, 1, 1), today]
      )
      if len(custom_range) == 2:
        start_date, end_date = custom_range
      else:
        start_date, end_date = datetime.date(2026, 1, 1), today
    else:
      start_date, end_date = None, None

  target_types = sel_types if sel_types else all_types
  available_cats = []
  for t in target_types:
    if t in kategori_by_tipe:
      for c in kategori_by_tipe[t]:
        if c not in available_cats:
          available_cats.append(c)

  sel_cats = st.multiselect(
      "Pilih Kategori",
      available_cats,
      default=[],
      key="sel_cats",
      placeholder="Pilih kategori...",
  )

  is_filter_active = bool(
      sel_members or sel_types or sel_cats or (time_mode != "Semua Waktu")
  )

  if not is_filter_active:
    df_filtered = pd.DataFrame(columns=df.columns)
  else:
    df_filtered = df.copy()
    if start_date and end_date and time_mode != "Semua Waktu":
      df_filtered["Tanggal_dt"] = pd.to_datetime(
          df_filtered["Tanggal"]
      ).dt.date
      df_filtered = df_filtered[
          (df_filtered["Tanggal_dt"] >= start_date)
          & (df_filtered["Tanggal_dt"] <= end_date)
      ]
    if sel_members:
      df_filtered = df_filtered[df_filtered["Member"].isin(sel_members)]
    if sel_types:
      df_filtered = df_filtered[df_filtered["Tipe"].isin(sel_types)]
    if sel_cats:
      df_filtered = df_filtered[df_filtered["Kategori"].isin(sel_cats)]

  st.markdown("---")
  st.subheader("📋 Hasil & Ringkasan Filter")

  if not is_filter_active:
    st.info(
        "👆 Silakan pilih filter di atas (Member, Tipe, Kategori, atau Waktu)"
        " untuk menampilkan data transaksi."
    )
  else:
    f_total = df_filtered["Nominal"].sum() if not df_filtered.empty else 0
    f_count = len(df_filtered)

    r_col1, r_col2 = st.columns(2)
    r_col1.metric("Total Nominal Dari Filter Ini", f"Rp {f_total:,.0f}")
    r_col2.metric("Jumlah Transaksi Ditemukan", f"{f_count} Data")

    st.dataframe(df_filtered, use_container_width=True)


# --- HALAMAN 2: INPUT ---
elif menu == "🎮 Input":
  if st.session_state.get("trigger_reset", False):
    st.session_state["in_member"] = list_member[0]
    st.session_state["in_tipe"] = "Expenses"
    st.session_state["in_kategori"] = kategori_by_tipe["Expenses"][0]
    st.session_state["in_quick"] = "Pilih Nominal Cepat"
    st.session_state["in_manual"] = ""
    st.session_state["in_catatan"] = ""
    st.session_state["trigger_reset"] = False

  st.markdown('<div class="kid-box">', unsafe_allow_html=True)
  st.title("🎈 Catat Keuangan Keluarga")
  st.markdown(
      "Gunakan halaman ini untuk mencatat pemasukan, pengeluaran, atau tabungan"
      " langsung ke Google Sheets! 🚀"
  )
  st.markdown("---")

  member = st.radio(
      "**1. Siapa nama member?**",
      list_member,
      horizontal=True,
      key="in_member",
  )

  tipe = st.radio(
      "**2. Apa jenis transaksinya?**",
      ["Expenses", "Income", "Top Up Saving", "Withdraw Saving"],
      horizontal=True,
      key="in_tipe",
  )

  kategori_pilihan = kategori_by_tipe.get(tipe, ["Lainnya ✨"])
  if (
      "in_kategori" in st.session_state
      and st.session_state["in_kategori"] not in kategori_pilihan
  ):
    st.session_state["in_kategori"] = kategori_pilihan[0]

  kategori = st.selectbox(
      "**3. Pilih Kategorinya:**", kategori_pilihan, key="in_kategori"
  )

  st.markdown("**4. Berapa Nominalnya?**")
  quick_choice = st.radio(
      "Nominal Cepat:",
      [
          "Pilih Nominal Cepat",
          "Rp 5.000",
          "Rp 10.000",
          "Rp 20.000",
          "Rp 50.000",
          "Ketik Sendiri",
      ],
      horizontal=True,
      label_visibility="collapsed",
      key="in_quick",
  )

  nominal = 0
  if quick_choice == "Rp 5.000":
    nominal = 5000
  elif quick_choice == "Rp 10.000":
    nominal = 10000
  elif quick_choice == "Rp 20.000":
    nominal = 20000
  elif quick_choice == "Rp 50.000":
    nominal = 50000
  elif quick_choice == "Ketik Sendiri":
    raw_nominal = st.text_input(
        "Atau Ketik Nominal Sendiri (Rp):",
        placeholder="Contoh: 3000000",
        key="in_manual",
    )
    clean_digits = "".join(filter(str.isdigit, raw_nominal))
    nominal = int(clean_digits) if clean_digits else 0
    if nominal > 0:
      formatted_preview = f"{nominal:,.0f}".replace(",", ".")
      st.markdown(f"✨ **Auto-Correct Nominal:** `Rp {formatted_preview}`")

  catatan = st.text_input(
      "**Catatan Singkat (Contoh: Beli Mainan / Jajan Es Krim):**",
      key="in_catatan",
  )

  st.markdown("---")

  if st.button("🌟 SIMPAN KE CLOUD!", use_container_width=True):
    if nominal <= 0:
      st.warning(
          "⚠️ Nominal belum diisi atau bernilai 0! Silakan pilih tombol cepat"
          " atau ketik nominalnya."
      )
    else:
      new_row = {
          "Tanggal": str(datetime.date.today()),
          "Member": member,
          "Tipe": tipe,
          "Kategori": kategori,
          "Nominal": nominal,
          "Catatan": catatan if catatan else "-",
      }

      success = save_data_to_sheets(new_row)

      if success:
        st.session_state["data_transaksi"] = load_data_from_sheets()
        st.session_state["trigger_reset"] = True
        st.success(
            "🎉 Hore! Berhasil tersimpan secara online ke Google Sheets!"
        )
        st.balloons()
        st.rerun()
      else:
        st.error(
            "❌ Gagal menyimpan ke Google Sheets. Pastikan URL Apps Script benar."
        )

  st.markdown("</div>", unsafe_allow_html=True)


# --- HALAMAN 3: RIWAYAT ---
elif menu == "🗂️ Riwayat":
  st.title("🗂️ Riwayat Seluruh Transaksi")
  st.markdown("Daftar lengkap seluruh transaksi dari Google Sheets.")
  st.markdown("---")

  if df.empty:
    st.info("Belum ada data transaksi.")
  else:
    st.metric("Total Seluruh Transaksi", f"{len(df)} Data")
    st.dataframe(df, use_container_width=True)


# --- HALAMAN 4: PENGATURAN (ADMIN) ---
elif menu == "⚙️ Pengaturan (Admin)":
  st.title("⚙️ Pengaturan Master Data (Admin)")
  admin_pass = st.text_input(
      "🔐 Masukkan Password Admin:", type="password", placeholder="Password..."
  )
  DEFAULT_PASSWORD = "malailak2026"

  if admin_pass == DEFAULT_PASSWORD:
    st.success("🔓 Akses Diterima!")
    st.markdown("---")
    st.subheader("👥 Kelola Anggota Keluarga (Member)")
    col_m1, col_m2, col_m3 = st.columns(3)

    with col_m1:
      new_member = st.text_input(
          "Tambah Member Baru (Contoh: Nenek 👵)", key="new_member_input"
      )
      if st.button("➕ Tambah Member"):
        if new_member and new_member not in st.session_state["list_member"]:
          st.session_state["list_member"].append(new_member)
          st.success(f"Berhasil menambahkan member: **{new_member}**")
          st.rerun()
        elif new_member in st.session_state["list_member"]:
          st.warning("Nama member tersebut sudah ada!")

    with col_m2:
      member_to_edit = st.selectbox(
          "Pilih Member yang Ingin Diubah/Rename",
          st.session_state["list_member"],
          key="m_edit_select",
      )
      rename_member = st.text_input(
          "Nama Baru:", placeholder="Contoh: Extended Cost / Rumah 🏡"
      )
      if st.button("✏️ Ubah Nama Member"):
        if rename_member and rename_member not in st.session_state["list_member"]:
          idx = st.session_state["list_member"].index(member_to_edit)
          st.session_state["list_member"][idx] = rename_member
          st.success(
              f"Berhasil mengubah **{member_to_edit}** menjadi"
              f" **{rename_member}**!"
          )
          st.rerun()
        elif rename_member in st.session_state["list_member"]:
          st.warning("Nama tersebut sudah ada!")

    with col_m3:
      member_to_del = st.selectbox(
          "Pilih Member yang Ingin Dihapus",
          st.session_state["list_member"],
          key="m_del_select",
      )
      if st.button("🗑️ Hapus Member"):
        if len(st.session_state["list_member"]) > 1:
          st.session_state["list_member"].remove(member_to_del)
          st.success(f"Berhasil menghapus member: **{member_to_del}**")
          st.rerun()
        else:
          st.warning("Minimal harus menyisakan 1 member di dalam sistem!")

    st.markdown("---")
    st.subheader("🏷️ Kelola Kategori Transaksi")
    selected_type = st.selectbox(
        "Pilih Tipe Transaksi", list(st.session_state["kategori_by_tipe"].keys())
    )

    col_c1, col_c2 = st.columns(2)
    with col_c1:
      new_cat = st.text_input(
          f"Tambah Kategori Baru untuk {selected_type}", key="new_cat_input"
      )
      if st.button("➕ Tambah Kategori"):
        if (
            new_cat
            and new_cat
            not in st.session_state["kategori_by_tipe"][selected_type]
        ):
          st.session_state["kategori_by_tipe"][selected_type].append(new_cat)
          st.success(
              f"Berhasil menambahkan kategori **{new_cat}** ke {selected_type}!"
          )
          st.rerun()
        elif new_cat in st.session_state["kategori_by_tipe"][selected_type]:
          st.warning("Kategori tersebut sudah ada di tipe ini!")

    with col_c2:
      cat_to_del = st.selectbox(
          f"Pilih Kategori yang Ingin Dihapus dari {selected_type}",
          st.session_state["kategori_by_tipe"][selected_type],
      )
      if st.button("🗑️ Hapus Kategori"):
        if len(st.session_state["kategori_by_tipe"][selected_type]) > 1:
          st.session_state["kategori_by_tipe"][selected_type].remove(cat_to_del)
          st.success(f"Berhasil menghapus kategori **{cat_to_del}**!")
          st.rerun()
        else:
          st.warning("Minimal harus menyisakan 1 kategori dalam tipe ini!")

  elif admin_pass:
    st.error("❌ Password salah!")
  else:
    st.info("🔑 Masukkan password admin (*Password: malailak2026*).")