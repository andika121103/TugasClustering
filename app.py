import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

st.set_page_config(
    page_title="Customer Segmentation - CC_GENERAL",
    page_icon="💳",
    layout="centered",
)

@st.cache_resource
def load_model():
    model_path = Path(__file__).resolve().parent / "model.joblib"
    artifact = joblib.load(model_path)
    return artifact["pipeline"], artifact["features"]

pipeline, FEATURES = load_model()

FEATURE_INFO = {
    "BALANCE": "Saldo kartu kredit nasabah saat ini",
    "PURCHASES": "Total nilai pembelian yang dilakukan nasabah",
    "CASH_ADVANCE": "Total penarikan tunai (cash advance) nasabah",
    "CREDIT_LIMIT": "Limit kartu kredit yang dimiliki nasabah",
    "PAYMENTS": "Total pembayaran yang telah dilakukan nasabah",
    "TENURE": "Lama keanggotaan nasabah (dalam bulan)",
}

CLUSTER_LABELS = {
    0: "Cluster 0 - Nasabah dengan aktivitas transaksi ringan hingga menengah",
    1: "Cluster 1 - Nasabah dengan aktivitas transaksi tinggi (heavy user)",
}

st.title("💳 Customer Segmentation - CC_GENERAL")

st.caption(
    "Aplikasi ini mengelompokkan nasabah kartu kredit ke dalam segmen "
    "menggunakan model K-Means yang telah dilatih pada notebook."
)

st.divider()
st.subheader("Masukkan Data Nasabah")

input_values = {}

col1, col2 = st.columns(2)
columns = [col1, col2]

for i, feature in enumerate(FEATURES):
    col = columns[i % 2]

    with col:
        if feature == "TENURE":
            input_values[feature] = st.number_input(
                label=feature,
                min_value=0,
                max_value=12,
                value=12,
                step=1,
                help=FEATURE_INFO.get(feature, ""),
            )
        else:
            input_values[feature] = st.number_input(
                label=feature,
                min_value=0.0,
                value=0.0,
                step=100.0,
                format="%.2f",
                help=FEATURE_INFO.get(feature, ""),
            )

st.divider()

if st.button("Predict", type="primary", use_container_width=True):
    input_df = pd.DataFrame([input_values])[FEATURES]

    cluster = pipeline.predict(input_df)[0]

    st.success(
        f"Hasil Prediksi: **{CLUSTER_LABELS.get(cluster, f'Cluster {cluster}')}**"
    )

    distances = pipeline.transform(input_df)[0]
    proximity = 1 / (1 + distances)
    proximity_pct = (proximity / proximity.sum() * 100).round(2)

    st.write("**Tingkat kedekatan terhadap tiap cluster:**")

    proximity_df = pd.DataFrame(
        {
            "Cluster": [
                CLUSTER_LABELS.get(i, f"Cluster {i}")
                for i in range(len(proximity_pct))
            ],
            "Kedekatan (%)": proximity_pct,
        }
    ).set_index("Cluster")

    st.bar_chart(proximity_df)

    with st.expander("Lihat data input"):
        st.dataframe(input_df)

st.divider()
