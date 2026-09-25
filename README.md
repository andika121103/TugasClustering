# Customer Segmentation App - CC_GENERAL

Aplikasi web sederhana untuk melakukan **segmentasi nasabah kartu kredit** menggunakan model **K-Means Clustering** yang telah dilatih pada dataset `CC_GENERAL.csv`. Aplikasi dibangun dengan **Streamlit** dan siap di-deploy ke **Streamlit Community Cloud**.

## Fungsi Aplikasi

Aplikasi ini menerima input data transaksi nasabah kartu kredit (saldo, pembelian, penarikan tunai, limit kredit, pembayaran, dan lama keanggotaan), lalu memprediksi **segmen/cluster** nasabah tersebut menggunakan model K-Means (K=2) yang sudah dilatih pada `notebook.ipynb`:

- **Cluster 0** — Nasabah dengan aktivitas transaksi ringan hingga menengah.
- **Cluster 1** — Nasabah dengan aktivitas transaksi tinggi (*heavy user*).

Karena K-Means tidak memiliki `predict_proba()`, aplikasi menampilkan **tingkat kedekatan (proximity)** input terhadap tiap centroid cluster sebagai gambaran seberapa dekat data tersebut ke masing-masing segmen.

Model **tidak dilatih ulang** oleh aplikasi ini — `model/model.joblib` dihasilkan dari proses training yang identik dengan langkah-langkah pada `notebook.ipynb` (fitur, preprocessing, algoritma, dan hyperparameter sama persis), sehingga hasil clustering konsisten dengan penelitian pada notebook.

## Struktur Folder

```
project/
│
├── notebook.ipynb           # Notebook penelitian asli
├── dataset.csv              # Dataset asli
│
├── model.joblib             # Pipeline (StandardScaler + KMeans) hasil training
│
├── app.py                   # Aplikasi Streamlit
├── requirements.txt         # Daftar dependency
└── README.md                # Dokumentasi ini
```

## Fitur yang Digunakan Model

Model menggunakan 6 fitur numerik berikut (harus tersedia di `model/model.joblib` dan diisi lewat form aplikasi):

| Fitur | Keterangan |
|---|---|
| `BALANCE` | Saldo kartu kredit nasabah |
| `PURCHASES` | Total nilai pembelian |
| `CASH_ADVANCE` | Total penarikan tunai |
| `CREDIT_LIMIT` | Limit kartu kredit |
| `PAYMENTS` | Total pembayaran |
| `TENURE` | Lama keanggotaan (bulan) |

Preprocessing (`StandardScaler`) sudah disatukan dalam satu `Pipeline` bersama model `KMeans`, sehingga input dari Streamlit otomatis diproses dengan cara yang sama seperti saat training — tanpa perlu langkah manual tambahan di `app.py`.

## Cara Menjalankan Secara Lokal

1. **Clone / unduh project ini**, pastikan struktur folder sesuai di atas.

2. **(Opsional tapi disarankan) Buat virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. **Install dependency:**

   ```bash
   pip install -r requirements.txt
   ```

## Cara Menjalankan dengan Streamlit

Dari folder root project (folder yang berisi `app.py`), jalankan:

```bash
streamlit run app.py
```

Aplikasi akan otomatis terbuka di browser pada alamat `http://localhost:8501`. Isi form data nasabah pada aplikasi, lalu klik tombol **Predict** untuk melihat hasil segmentasi.

## Cara Upload ke GitHub

1. Buat repository baru di GitHub (misalnya `customer-segmentation-cc-general`).
2. Di folder project, inisialisasi git (jika belum) dan push:

   ```bash
   git init
   git add .
   git commit -m "Add customer segmentation deployment app"
   git branch -M main
   git remote add origin https://github.com/<username>/<nama-repo>.git
   git push -u origin main
   ```

3. Pastikan seluruh isi folder `project/` (termasuk `model/model.joblib`, `app.py`, `requirements.txt`) ikut ter-upload.

## Cara Deploy ke Streamlit Community Cloud

1. Buka [share.streamlit.io](https://share.streamlit.io) dan login menggunakan akun GitHub.
2. Klik **"New app"**.
3. Pilih repository, branch (`main`), dan file utama: `app.py`.
4. Klik **"Deploy"**.
5. Tunggu proses build selesai — Streamlit Cloud akan otomatis menginstall dependency dari `requirements.txt`.
6. Setelah selesai, aplikasi dapat diakses melalui URL publik yang diberikan Streamlit Cloud.

**Catatan:** Pastikan file `model/model.joblib` ikut ter-commit ke GitHub (bukan file besar yang di-ignore), karena aplikasi memerlukan file ini saat runtime.

## Catatan Teknis

- Model, algoritma, hyperparameter, fitur, dan hasil evaluasi **sama persis** dengan yang ada di `notebook.ipynb` — tidak ada evaluasi ulang atau perubahan apa pun terhadap penelitian asli.
- `requirements.txt` di-pin ke versi package yang sama dengan yang digunakan saat menyimpan `model.joblib`, untuk menghindari error kompatibilitas saat load model.
