# 🚲 Bike Sharing Dashboard

Dashboard interaktif untuk menganalisis data peminjaman sepeda tahun 2011–2012 menggunakan Streamlit.

---

## 📁 Struktur Proyek

```
submission/
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv
├── notebook.ipynb
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Environment

### 1. Clone atau Download Proyek

Download semua berkas dan pastikan strukturnya sesuai di atas.

### 2. Buat Virtual Environment (Opsional tapi Disarankan)

```bash
python -m venv venv
```

Aktifkan virtual environment:

- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Install Library yang Dibutuhkan

```bash
pip install -r requirements.txt
```

---

## 🚀 Menjalankan Dashboard

```bash
cd dashboard
streamlit run dashboard.py
```


## 📊 Fitur Dashboard

- **Filter** data berdasarkan tahun (2011 / 2012) dan musim
- **Metric cards** — total peminjaman, rata-rata per hari, peminjaman tertinggi
- **Grafik 1** — Rata-rata peminjaman harian per musim
- **Grafik 2** — Pola peminjaman per jam: Hari Kerja vs Hari Libur
- **Assessing Data** — ringkasan info dataset, statistik deskriptif, missing values, dan outlier



