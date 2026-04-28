import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import io

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(base_dir, "main_data.csv"))

    df['dteday'] = pd.to_datetime(df['dteday'])

    season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    df['season_label'] = df['season'].map(season_map)

    df['workingday_label'] = df['workingday'].map({0: 'Libur', 1: 'Hari Kerja'})

    return df

df = load_data()

st.title("🚲 Bike Sharing Dashboard")
st.caption("Analisis data peminjaman sepeda tahun 2011–2012")
st.markdown("---")

with st.sidebar:
    st.header("🔧 Filter Data")
    year_options = {0: "2011", 1: "2012", "Semua": "Semua"}
    selected_year = st.selectbox("Pilih Tahun", options=["Semua", 0, 1],
                                  format_func=lambda x: year_options[x])
    selected_season = st.selectbox("Pilih Musim",
                                    options=["Semua", "Spring", "Summer", "Fall", "Winter"])
    st.markdown("---")
    st.info("Filter ini berlaku untuk semua grafik di bawah.")

df_filtered = df.copy()

if selected_year != "Semua":
    df_filtered = df_filtered[df_filtered['yr'] == selected_year]

if selected_season != "Semua":
    df_filtered = df_filtered[df_filtered['season_label'] == selected_season]

# Buat df_day_filtered dari main_data (agregasi per hari)
df_day_filtered = df_filtered.groupby('dteday').agg(
    cnt=('cnt', 'sum'),
    season_label=('season_label', 'first'),
    yr=('yr', 'first')
).reset_index()

# Data Wrangling
st.subheader("🔍 Data Wrangling")
with st.expander("📋 Assessing Data — Klik untuk buka"):

    st.markdown("**Info Dataset (main_data.csv)**")
    buf = io.StringIO()
    df.info(buf=buf)
    st.text(buf.getvalue())

    st.markdown("**Statistik Deskriptif**")
    st.dataframe(df.describe())

    st.markdown("**Missing Values**")
    st.dataframe(df.isnull().sum().rename('Jumlah Missing').to_frame())

    st.markdown("**Data Duplikat**")
    st.write(f"Jumlah duplikat: **{df.duplicated().sum()}**")

    st.markdown("**Cek Outlier Kolom `cnt` dengan IQR**")
    Q1 = df['cnt'].quantile(0.25)
    Q3 = df['cnt'].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = df[(df['cnt'] < lower) | (df['cnt'] > upper)]
    ca, cb, cc = st.columns(3)
    ca.metric("Batas Bawah", f"{lower:,.0f}")
    cb.metric("Batas Atas", f"{upper:,.0f}")
    cc.metric("Jumlah Outlier", len(outliers))
    st.caption("Outlier dianggap wajar, tidak dihapus.")

st.markdown("---")

# Metric Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Peminjaman", f"{df_day_filtered['cnt'].sum():,.0f}")
with col2:
    st.metric("Rata-rata / Hari", f"{df_day_filtered['cnt'].mean():,.0f}")
with col3:
    st.metric("Peminjaman Tertinggi", f"{df_day_filtered['cnt'].max():,.0f}")
with col4:
    st.metric("Total Hari Data", f"{len(df_day_filtered):,}")

st.markdown("---")

# Grafik 1
st.subheader("📊 Pertanyaan 1: Rata-rata Peminjaman per Musim")

avg_per_season = (
    df_day_filtered.groupby('season_label')['cnt'].mean()
    .reindex(['Spring', 'Summer', 'Fall', 'Winter']).dropna().reset_index()
)
avg_per_season.columns = ['Musim', 'Rata-rata']

if avg_per_season.empty:
    st.warning("Tidak ada data untuk filter yang dipilih.")
else:
    max_val = avg_per_season['Rata-rata'].max()
    min_val = avg_per_season['Rata-rata'].min()
    colors = ['#e74c3c' if v == max_val else '#3498db' if v == min_val else '#bdc3c7'
              for v in avg_per_season['Rata-rata']]

    fig1, ax1 = plt.subplots(figsize=(8, 4.5))
    bars = ax1.bar(avg_per_season['Musim'], avg_per_season['Rata-rata'],
                   color=colors, edgecolor='white')
    for bar in bars:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h + 40,
                 f'{h:,.0f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    ax1.set_title('Rata-rata Peminjaman Sepeda Harian per Musim', fontsize=13, fontweight='bold')
    ax1.set_xlabel('Musim', fontsize=11)
    ax1.set_ylabel('Rata-rata Peminjaman', fontsize=11)
    ax1.set_ylim(0, avg_per_season['Rata-rata'].max() * 1.2)
    ax1.spines[['top', 'right']].set_visible(False)
    ax1.yaxis.grid(True, linestyle='--', alpha=0.4)
    ax1.set_axisbelow(True)
    legend_els = [mpatches.Patch(facecolor='#e74c3c', label='Tertinggi'),
                  mpatches.Patch(facecolor='#3498db', label='Terendah'),
                  mpatches.Patch(facecolor='#bdc3c7', label='Lainnya')]
    ax1.legend(handles=legend_els, loc='upper left', fontsize=10)
    fig1.tight_layout()
    st.pyplot(fig1)

    top_season = avg_per_season.loc[avg_per_season['Rata-rata'].idxmax(), 'Musim']
    low_season = avg_per_season.loc[avg_per_season['Rata-rata'].idxmin(), 'Musim']
    st.info(f"💡 **Insight:** Peminjaman tertinggi di musim **{top_season}** dan terendah di musim **{low_season}**.")

st.markdown("---")

# Grafik 2
st.subheader("📈 Pertanyaan 2: Pola Peminjaman per Jam (Hari Kerja vs Libur)")

avg_per_hour = (
    df_filtered.groupby(['hr', 'workingday_label'])['cnt'].mean().reset_index()
)

if avg_per_hour.empty:
    st.warning("Tidak ada data untuk filter yang dipilih.")
else:
    workday = avg_per_hour[avg_per_hour['workingday_label'] == 'Hari Kerja']
    holiday = avg_per_hour[avg_per_hour['workingday_label'] == 'Libur']

    fig2, ax2 = plt.subplots(figsize=(10, 4.5))
    if not workday.empty:
        ax2.plot(workday['hr'], workday['cnt'], color='#e74c3c',
                 linewidth=2.5, marker='o', markersize=4, label='Hari Kerja')
        peak = workday.loc[workday['cnt'].idxmax()]
        ax2.annotate(f"Puncak\nJam {int(peak['hr'])}.00\n({peak['cnt']:.0f})",
                     xy=(peak['hr'], peak['cnt']),
                     xytext=(peak['hr'] - 3.5, peak['cnt'] - 90),
                     arrowprops=dict(arrowstyle='->', color='#333'),
                     fontsize=9, color='#333')
    if not holiday.empty:
        ax2.plot(holiday['hr'], holiday['cnt'], color='#3498db',
                 linewidth=2.5, marker='o', markersize=4, label='Libur')
    ax2.set_title('Rata-rata Peminjaman Sepeda per Jam\nHari Kerja vs Hari Libur',
                  fontsize=13, fontweight='bold')
    ax2.set_xlabel('Jam (0–23)', fontsize=11)
    ax2.set_ylabel('Rata-rata Peminjaman', fontsize=11)
    ax2.set_xticks(range(0, 24))
    ax2.spines[['top', 'right']].set_visible(False)
    ax2.yaxis.grid(True, linestyle='--', alpha=0.4)
    ax2.set_axisbelow(True)
    ax2.legend(fontsize=11)
    fig2.tight_layout()
    st.pyplot(fig2)

    st.info("💡 **Insight:** Hari kerja punya dua puncak tajam (berangkat & pulang kerja), "
            "sedangkan hari libur lebih merata di siang hari.")

st.markdown("---")
st.caption("📦 Data: Bike Sharing Dataset  | Periode: 2011–2012")