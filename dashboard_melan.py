import numpy as np
import pandas as pd
import plotly.express as px
import pymysql
import streamlit as st
from sqlalchemy import create_engine


st.set_page_config(
    page_title="Dashboard SPK SAW UMKM",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

THEME = {
    "bg": "#0b1220",
    "surface": "#111827",
    "surface_soft": "#0f172a",
    "text": "#e5e7eb",
    "muted": "#94a3b8",
    "border": "#243244",
    "primary": "#22c55e",
    "primary_soft": "#14532d",
    "secondary": "#38bdf8",
    "success": "#22c55e",
    "warning": "#f59e0b",
    "danger": "#ef4444",
}

CHART_COLORS = ["#22c55e", "#38bdf8", "#14b8a6", "#94a3b8", "#4ade80", "#0ea5e9"]

st.markdown(
    f"""
    <style>
        :root {{
            --bg: {THEME['bg']};
            --surface: {THEME['surface']};
            --surface-soft: {THEME['surface_soft']};
            --text: {THEME['text']};
            --muted: {THEME['muted']};
            --border: {THEME['border']};
            --primary: {THEME['primary']};
            --primary-soft: {THEME['primary_soft']};
            --secondary: {THEME['secondary']};
            --success: {THEME['success']};
            --warning: {THEME['warning']};
            --danger: {THEME['danger']};
        }}

        .stApp {{
            background:
                radial-gradient(circle at top left, rgba(34, 197, 94, 0.10), transparent 26%),
                radial-gradient(circle at top right, rgba(56, 189, 248, 0.10), transparent 24%),
                linear-gradient(180deg, #0b1220 0%, #111827 100%);
        }}

        section.main h1,
        section.main h2,
        section.main h3,
        section.main h4,
        section.main h5,
        section.main h6 {{
            color: var(--text);
        }}

        section.main p,
        section.main li,
        section.main label,
        section.main span {{
            color: #cbd5e1;
        }}

        .block-container {{
            padding-top: 3.4rem;
            padding-bottom: 2rem;
            max-width: 1420px;
        }}

        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
        }}

        [data-testid="stSidebar"] .block-container {{
            padding-top: 0.8rem;
            padding-bottom: 1rem;
        }}

        [data-testid="stSidebar"] * {{
            color: #ffffff !important;
        }}

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] h4,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span {{
            line-height: 1.45;
        }}

        [data-testid="stSidebar"] .stRadio {{
            margin-top: 0.35rem;
        }}

        [data-testid="stSidebar"] .stRadio label {{
            font-size: 0.96rem;
        }}

        .sidebar-card {{
            background: linear-gradient(180deg, rgba(15, 23, 42, 0.96) 0%, rgba(17, 24, 39, 0.96) 100%);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 18px;
            padding: 14px 14px 12px;
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.22);
            margin-bottom: 12px;
        }}

        .sidebar-card-title {{
            color: #f8fafc;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.10em;
            text-transform: uppercase;
            margin-bottom: 8px;
        }}

        .sidebar-card-value {{
            color: #ffffff;
            font-size: 28px;
            font-weight: 900;
            line-height: 1;
            margin-bottom: 6px;
        }}

        .sidebar-card-copy {{
            color: #cbd5e1;
            font-size: 12px;
            line-height: 1.55;
            margin-bottom: 10px;
        }}

        .sidebar-chip-row {{
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
        }}

        .sidebar-chip {{
            padding: 5px 10px;
            border-radius: 999px;
            border: 1px solid rgba(255, 255, 255, 0.12);
            background: rgba(255, 255, 255, 0.06);
            color: #e2e8f0;
            font-size: 11px;
            font-weight: 700;
        }}

        .sidebar-weight-list {{
            display: grid;
            gap: 8px;
        }}

        .sidebar-weight-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            padding: 8px 10px;
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.07);
        }}

        .sidebar-weight-name {{
            color: #f8fafc;
            font-size: 12px;
            font-weight: 700;
            line-height: 1.35;
        }}

        .sidebar-weight-value {{
            color: #22c55e;
            font-size: 12px;
            font-weight: 800;
            white-space: nowrap;
        }}

        .hero {{
            background:
                radial-gradient(circle at top right, rgba(56, 189, 248, 0.16), transparent 28%),
                linear-gradient(135deg, rgba(15, 118, 110, 0.98) 0%, rgba(15, 23, 42, 0.98) 100%);
            color: white;
            padding: 18px 20px;
            border-radius: 20px;
            box-shadow: 0 18px 40px rgba(15, 23, 42, 0.18);
            border: 1px solid rgba(255, 255, 255, 0.08);
            margin-bottom: 12px;
            margin-top: 0.6rem;
        }}

        .hero-kicker {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.14);
            color: #ecfeff;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.10em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }}

        .hero-title {{
            font-size: 28px;
            font-weight: 900;
            line-height: 1.12;
            margin-bottom: 8px;
        }}

        .hero-desc {{
            color: rgba(255, 255, 255, 0.86);
            font-size: 13px;
            line-height: 1.65;
            max-width: 840px;
            margin-bottom: 12px;
        }}

        .hero-badges {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }}

        .hero-badge {{
            padding: 6px 11px;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.12);
            border: 1px solid rgba(255, 255, 255, 0.12);
            font-size: 11px;
            font-weight: 600;
        }}

        .section-card {{
            background: rgba(17, 24, 39, 0.92);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 12px 14px;
            box-shadow: 0 12px 28px rgba(0, 0, 0, 0.28);
            margin-bottom: 12px;
        }}

        .section-label {{
            color: var(--primary);
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 6px;
        }}

        .section-heading {{
            color: var(--text);
            font-size: 17px;
            font-weight: 800;
            margin-bottom: 6px;
        }}

        .section-copy {{
            color: var(--muted);
            font-size: 13px;
            line-height: 1.65;
        }}

        .metric-card {{
            background: linear-gradient(180deg, rgba(17,24,39,0.98) 0%, rgba(15,23,42,0.98) 100%);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 14px 14px 16px;
            box-shadow: 0 12px 28px rgba(0, 0, 0, 0.30);
            min-height: 96px;
            position: relative;
            overflow: hidden;
        }}

        .metric-card::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
        }}

        .metric-card.accent-primary::before {{ background: linear-gradient(90deg, #22c55e, #38bdf8); }}
        .metric-card.accent-secondary::before {{ background: linear-gradient(90deg, #38bdf8, #14b8a6); }}
        .metric-card.accent-success::before {{ background: linear-gradient(90deg, #22c55e, #4ade80); }}
        .metric-card.accent-warning::before {{ background: linear-gradient(90deg, #f59e0b, #f97316); }}
        .metric-card.accent-danger::before {{ background: linear-gradient(90deg, #ef4444, #fb7185); }}

        .metric-label {{
            color: var(--muted);
            font-size: 11px;
            font-weight: 700;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}

        .metric-value {{
            color: var(--text);
            font-size: 23px;
            font-weight: 900;
            line-height: 1.15;
            word-break: break-word;
        }}

        .metric-note {{
            color: var(--muted);
            font-size: 12px;
            margin-top: 6px;
        }}

        .info-box {{
            background: linear-gradient(135deg, #0f172a 0%, #111827 100%);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 14px 16px;
            color: #e5e7eb;
            font-size: 14px;
            line-height: 1.6;
            margin-bottom: 16px;
        }}

        .small-note {{
            color: var(--muted);
            font-size: 13px;
            margin: 6px 0 14px;
        }}

        table {{
            color: #e5e7eb !important;
        }}

        thead tr th {{
            background: #0f172a !important;
            color: #f8fafc !important;
        }}

        tbody tr td {{
            background: #111827 !important;
            color: #e5e7eb !important;
        }}

        div[data-testid="stDataFrame"] {{
            border-radius: 14px;
            overflow: hidden;
        }}

        @media (max-width: 768px) {{
            .block-container {{
                padding-left: 1rem;
                padding-right: 1rem;
            }}

            .hero {{
                padding: 20px 18px;
                border-radius: 18px;
            }}

            .hero-title {{
                font-size: 25px;
            }}

            .hero-desc {{
                font-size: 13px;
            }}

            .metric-card {{
                min-height: 96px;
                padding: 16px;
            }}

            .metric-value {{
                font-size: 20px;
            }}

            .section-heading {{
                font-size: 18px;
            }}
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def get_engine():
    return create_engine("mysql+pymysql://root:@localhost/db_melan?charset=utf8mb4")


@st.cache_data
def load_data():
    query = """
        SELECT
            id_import,
            nama_debitur,
            jumlah_realisasi,
            outstanding,
            kolektabilitas_bumn,
            accrued_interest
        FROM tb_import_melan
    """
    engine = get_engine()
    with engine.connect() as connection:
        df = pd.read_sql_query(query, connection)

    df["nama_mitra_tampil"] = df.apply(
        lambda row: f"Nama Mitra Tidak Diketahui (ID {int(row['id_import'])})"
        if pd.isna(row["nama_debitur"]) or str(row["nama_debitur"]).strip() == ""
        else str(row["nama_debitur"]).strip(),
        axis=1,
    )
    return df


def rupiah(value):
    if pd.isna(value):
        return "Rp 0"
    return f"Rp {value:,.0f}".replace(",", ".")


def smart_rupiah(value):
    if pd.isna(value):
        return "Rp 0"

    nilai = float(value)
    nilai_abs = abs(nilai)

    if nilai_abs >= 1_000_000_000:
        return f"Rp {nilai / 1_000_000_000:.2f} M"
    if nilai_abs >= 1_000_000:
        return f"Rp {nilai / 1_000_000:.2f} jt"
    if nilai_abs >= 1_000:
        return f"Rp {nilai / 1_000:.2f} rb"
    return rupiah(nilai)


def angka(value):
    if pd.isna(value):
        return "0"
    return f"{value:,.0f}".replace(",", ".")


def konversi_kolektabilitas(value):
    if pd.isna(value):
        return 0

    teks = str(value).strip().lower()
    mapping = {
        "lancar": 5,
        "dalam perhatian khusus": 4,
        "dpk": 4,
        "kurang lancar": 3,
        "diragukan": 2,
        "macet": 1,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
        "1": 1,
    }
    return mapping.get(teks, 0)


def hitung_saw(df):
    df = df.copy()

    for col in ["jumlah_realisasi", "outstanding", "accrued_interest"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["skor_kolektabilitas"] = df["kolektabilitas_bumn"].apply(konversi_kolektabilitas)

    max_c1 = df["jumlah_realisasi"].max()
    max_c3 = df["skor_kolektabilitas"].max()
    min_c2 = df.loc[df["outstanding"] > 0, "outstanding"].min()
    min_c4 = df.loc[df["accrued_interest"] > 0, "accrued_interest"].min()

    if pd.isna(min_c2):
        min_c2 = 0
    if pd.isna(min_c4):
        min_c4 = 0

    df["c1_normalisasi"] = df["jumlah_realisasi"] / max_c1 if max_c1 != 0 else 0
    df["c2_normalisasi"] = (
        min_c2 / df["outstanding"].replace(0, np.nan)
    ).replace([np.inf, -np.inf], np.nan).fillna(0)
    df["c3_normalisasi"] = df["skor_kolektabilitas"] / max_c3 if max_c3 != 0 else 0
    df["c4_normalisasi"] = (
        min_c4 / df["accrued_interest"].replace(0, np.nan)
    ).replace([np.inf, -np.inf], np.nan).fillna(0)

    bobot_c1, bobot_c2, bobot_c3, bobot_c4 = 0.40, 0.30, 0.20, 0.10

    df["nilai_saw"] = (
        (df["c1_normalisasi"] * bobot_c1)
        + (df["c2_normalisasi"] * bobot_c2)
        + (df["c3_normalisasi"] * bobot_c3)
        + (df["c4_normalisasi"] * bobot_c4)
    )

    return df.sort_values("nilai_saw", ascending=False).reset_index(drop=True)


def style_currency_table(df, currency_cols=None, decimal_cols=None, highlight_cols=None):
    currency_cols = currency_cols or []
    decimal_cols = decimal_cols or []
    highlight_cols = highlight_cols or []

    styler = df.style

    if currency_cols:
        styler = styler.format({col: rupiah for col in currency_cols if col in df.columns}, na_rep="-")
    if decimal_cols:
        styler = styler.format({col: "{:.4f}" for col in decimal_cols if col in df.columns}, na_rep="-")

    if highlight_cols:
        styler = styler.set_table_styles([
            {"selector": "th", "props": [("background-color", "#0f172a"), ("color", "#f8fafc"), ("border", "1px solid #243244")]},
            {"selector": "td", "props": [("background-color", "#111827"), ("color", "#e5e7eb"), ("border", "1px solid #243244")]},
            {"selector": "table", "props": [("border-collapse", "separate"), ("border-spacing", "0")]},
        ])

        def color_scale(series):
            if not pd.api.types.is_numeric_dtype(series):
                return ["" for _ in series]

            min_v = series.min()
            max_v = series.max()
            if pd.isna(min_v) or pd.isna(max_v) or max_v == min_v:
                return ["background-color: #1f2937; color: #f8fafc; font-weight: 700;" for _ in series]

            styles = []
            for value in series:
                if pd.isna(value):
                    styles.append("")
                    continue

                ratio = max(0.0, min(1.0, (float(value) - min_v) / (max_v - min_v)))
                start = (31, 41, 55)
                end = (34, 197, 94)
                rgb = tuple(int(start[i] + (end[i] - start[i]) * ratio) for i in range(3))
                styles.append(f"background-color: rgb{rgb}; color: #f8fafc; font-weight: 700;")
            return styles

        for col in highlight_cols:
            if col in df.columns:
                styler = styler.apply(color_scale, subset=[col], axis=0)

    return styler


def render_metric(label, value, note="", accent="accent-primary"):
    st.markdown(
        f"""
        <div class="metric-card {accent}">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {f'<div class="metric-note">{note}</div>' if note else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


try:
    df_raw = load_data()
except Exception as exc:
    st.error("Gagal mengambil data dari database MySQL.")
    st.exception(exc)
    st.stop()

if df_raw.empty:
    st.warning("Data pada tabel tb_import_melan masih kosong.")
    st.stop()


df_ranked = hitung_saw(df_raw)
top_10 = df_ranked.head(10).copy()
bottom_10 = df_ranked.sort_values("nilai_saw", ascending=True).head(10).copy()
df_filtered = pd.concat([top_10, bottom_10], ignore_index=True).drop_duplicates(subset=["id_import"])
df_display = df_filtered.sort_values("nilai_saw", ascending=False).reset_index(drop=True)


st.sidebar.title("SPK SAW UMKM")
st.sidebar.caption("Sistem Pendukung Keputusan berbasis SAW")
st.sidebar.markdown(
    """
    <div class="sidebar-card">
        <div class="sidebar-card-title">Status Data</div>
        <div class="sidebar-card-value">20</div>
        <div class="sidebar-card-copy">Data yang tampil hanya 20 mitra terpilih: 10 tertinggi dan 10 terendah.</div>
        <div class="sidebar-chip-row">
            <span class="sidebar-chip">SAW Ready</span>
            <span class="sidebar-chip">MySQL</span>
            <span class="sidebar-chip">Top & Bottom</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

menu = st.sidebar.radio("Menu", ["Dashboard", "Data Mitra", "Perhitungan SAW", "Detail Mitra"])

st.sidebar.divider()
st.sidebar.markdown(
    """
    <div class="sidebar-card">
        <div class="sidebar-card-title">Bobot SAW</div>
        <div class="sidebar-weight-list">
            <div class="sidebar-weight-item"><div class="sidebar-weight-name">C1 Jumlah Realisasi</div><div class="sidebar-weight-value">0.40</div></div>
            <div class="sidebar-weight-item"><div class="sidebar-weight-name">C2 Outstanding</div><div class="sidebar-weight-value">0.30</div></div>
            <div class="sidebar-weight-item"><div class="sidebar-weight-name">C3 Kolektabilitas</div><div class="sidebar-weight-value">0.20</div></div>
            <div class="sidebar-weight-item"><div class="sidebar-weight-name">C4 Accrued Interest</div><div class="sidebar-weight-value">0.10</div></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">Simple Additive Weighting</div>
        <div class="hero-title">Dashboard Sistem Pendukung Keputusan</div>
        <div class="hero-desc">
            Penentuan prioritas penerima bantuan modal UMKM menggunakan metode SAW untuk menampilkan hasil analisis secara
            ringkas, jelas, dan siap dipresentasikan.
        </div>
        <div class="hero-badges">
            <div class="hero-badge">Bobot C1 = 40%</div>
            <div class="hero-badge">Bobot C2 = 30%</div>
            <div class="hero-badge">Bobot C3 = 20%</div>
            <div class="hero-badge">Bobot C4 = 10%</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if menu == "Dashboard":
    st.markdown(
        """
        <div class="section-card">
            <div class="section-label">Ringkasan</div>
            <div class="section-heading">Ringkasan hasil SAW terpilih</div>
            <div class="section-copy">
                Dashboard ini hanya menampilkan 20 data hasil filter SAW agar pembacaan cepat, ringkas, dan fokus ke peringkat teratas serta terbawah.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        render_metric("Jumlah Data Ditampilkan", angka(len(df_filtered)), "Gabungan top 10 dan bottom 10", "accent-primary")
    with col2:
        render_metric("Total Jumlah Realisasi", smart_rupiah(df_filtered["jumlah_realisasi"].sum()), "Akumulasi data yang tampil", "accent-secondary")
    with col3:
        render_metric("Total Outstanding", smart_rupiah(df_filtered["outstanding"].sum()), "Akumulasi data yang tampil", "accent-success")
    with col4:
        render_metric("Rata-rata Nilai SAW", f"{df_filtered['nilai_saw'].mean():.4f}", "Rata-rata 20 data terpilih", "accent-warning")
    with col5:
        render_metric("Nilai SAW Tertinggi", f"{df_filtered['nilai_saw'].max():.4f}", "Nilai tertinggi pada data yang difilter", "accent-danger")

    visual_tab, table_tab = st.tabs(["Visualisasi", "Tabel"])

    with visual_tab:
        left, right = st.columns(2)
        with left:
            st.subheader("Top 10 Nilai SAW")
            fig_top = px.bar(
                top_10,
                x="nilai_saw",
                y="nama_mitra_tampil",
                orientation="h",
                text="nilai_saw",
                labels={"nilai_saw": "Nilai SAW", "nama_mitra_tampil": "Nama Mitra"},
                custom_data=["jumlah_realisasi", "outstanding", "accrued_interest"],
            )
            fig_top.update_traces(
                marker_color=THEME["primary"],
                texttemplate="%{text:.4f}",
                textposition="outside",
                cliponaxis=False,
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Nilai SAW: %{x:.4f}<br>"
                    "Jumlah Realisasi: %{customdata[0]:,.0f}<br>"
                    "Outstanding: %{customdata[1]:,.0f}<br>"
                    "Accrued Interest: %{customdata[2]:,.0f}<extra></extra>"
                ),
            )
            fig_top.update_layout(
                template="plotly_dark",
                yaxis=dict(categoryorder="total ascending"),
                xaxis_title="Nilai SAW",
                yaxis_title="Nama Mitra",
                height=420,
                margin=dict(l=10, r=10, t=20, b=10),
            )
            st.plotly_chart(fig_top, width="stretch")

        with right:
            st.subheader("Bottom 10 Nilai SAW")
            fig_bottom = px.bar(
                bottom_10,
                x="nilai_saw",
                y="nama_mitra_tampil",
                orientation="h",
                text="nilai_saw",
                labels={"nilai_saw": "Nilai SAW", "nama_mitra_tampil": "Nama Mitra"},
                custom_data=["jumlah_realisasi", "outstanding", "accrued_interest"],
            )
            fig_bottom.update_traces(
                marker_color=THEME["secondary"],
                texttemplate="%{text:.4f}",
                textposition="outside",
                cliponaxis=False,
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Nilai SAW: %{x:.4f}<br>"
                    "Jumlah Realisasi: %{customdata[0]:,.0f}<br>"
                    "Outstanding: %{customdata[1]:,.0f}<br>"
                    "Accrued Interest: %{customdata[2]:,.0f}<extra></extra>"
                ),
            )
            fig_bottom.update_layout(
                template="plotly_dark",
                yaxis=dict(categoryorder="total ascending"),
                xaxis_title="Nilai SAW",
                yaxis_title="Nama Mitra",
                height=420,
                margin=dict(l=10, r=10, t=20, b=10),
            )
            st.plotly_chart(fig_bottom, width="stretch")

        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("Komposisi Kolektabilitas")
            kol_data = df_filtered["kolektabilitas_bumn"].value_counts().reset_index()
            kol_data.columns = ["kolektabilitas_bumn", "jumlah"]
            fig_pie = px.pie(
                kol_data,
                names="kolektabilitas_bumn",
                values="jumlah",
                hole=0.45,
                color_discrete_sequence=CHART_COLORS,
            )
            fig_pie.update_traces(
                textinfo="percent+label",
                hovertemplate="<b>%{label}</b><br>Jumlah data: %{value}<br>Porsi: %{percent}<extra></extra>",
            )
            fig_pie.update_layout(
                template="plotly_dark",
                legend_title_text="Kolektabilitas",
                height=390,
                margin=dict(l=10, r=10, t=20, b=10),
            )
            st.plotly_chart(fig_pie, width="stretch")

        with col_b:
            st.subheader("Scatter Plot Realisasi vs Outstanding")
            fig_scatter = px.scatter(
                df_filtered,
                x="jumlah_realisasi",
                y="outstanding",
                color="kolektabilitas_bumn",
                size="nilai_saw",
                hover_name="nama_mitra_tampil",
                labels={
                    "jumlah_realisasi": "Jumlah Realisasi",
                    "outstanding": "Outstanding",
                    "kolektabilitas_bumn": "Kolektabilitas",
                    "nilai_saw": "Nilai SAW",
                },
                custom_data=["accrued_interest", "nilai_saw"],
                color_discrete_sequence=CHART_COLORS,
            )
            fig_scatter.update_traces(
                hovertemplate=(
                    "<b>%{hovertext}</b><br>"
                    "Jumlah Realisasi: %{x:,.0f}<br>"
                    "Outstanding: %{y:,.0f}<br>"
                    "Accrued Interest: %{customdata[0]:,.0f}<br>"
                    "Nilai SAW: %{customdata[1]:.4f}<extra></extra>"
                )
            )
            fig_scatter.update_layout(
                template="plotly_dark",
                legend_title_text="Kolektabilitas",
                xaxis_title="Jumlah Realisasi (Rp)",
                yaxis_title="Outstanding (Rp)",
                height=390,
                margin=dict(l=10, r=10, t=20, b=10),
            )
            st.plotly_chart(fig_scatter, width="stretch")

    with table_tab:
        st.subheader("10 Data Tertinggi dan 10 Data Terendah")
        st.caption("Tabel di bawah mempertahankan fokus hanya pada data terpilih supaya lebih mudah dibandingkan.")
        top_table_col, bottom_table_col = st.columns(2)

        top_table = top_10[["nama_mitra_tampil", "jumlah_realisasi", "outstanding", "kolektabilitas_bumn", "accrued_interest", "nilai_saw"]].copy()
        top_table = top_table.rename(columns={
            "nama_mitra_tampil": "Nama Mitra",
            "jumlah_realisasi": "Jumlah Realisasi",
            "outstanding": "Outstanding",
            "kolektabilitas_bumn": "Kolektabilitas",
            "accrued_interest": "Accrued Interest",
            "nilai_saw": "Nilai SAW",
        })

        bottom_table = bottom_10[["nama_mitra_tampil", "jumlah_realisasi", "outstanding", "kolektabilitas_bumn", "accrued_interest", "nilai_saw"]].copy()
        bottom_table = bottom_table.rename(columns={
            "nama_mitra_tampil": "Nama Mitra",
            "jumlah_realisasi": "Jumlah Realisasi",
            "outstanding": "Outstanding",
            "kolektabilitas_bumn": "Kolektabilitas",
            "accrued_interest": "Accrued Interest",
            "nilai_saw": "Nilai SAW",
        })

        with top_table_col:
            st.markdown("#### Top 10")
            st.dataframe(
                style_currency_table(
                    top_table,
                    currency_cols=["Jumlah Realisasi", "Outstanding", "Accrued Interest"],
                    decimal_cols=["Nilai SAW"],
                    highlight_cols=["Nilai SAW"],
                ),
                width="stretch",
                hide_index=True,
            )

        with bottom_table_col:
            st.markdown("#### Bottom 10")
            st.dataframe(
                style_currency_table(
                    bottom_table,
                    currency_cols=["Jumlah Realisasi", "Outstanding", "Accrued Interest"],
                    decimal_cols=["Nilai SAW"],
                    highlight_cols=["Nilai SAW"],
                ),
                width="stretch",
                hide_index=True,
            )

elif menu == "Data Mitra":
    st.markdown(
        """
        <div class="section-card">
            <div class="section-label">Data Mitra</div>
            <div class="section-heading">Daftar 20 data hasil filter SAW</div>
            <div class="section-copy">
                Tabel berikut menampilkan 20 data yang sudah difilter dari hasil SAW. Tidak ada ranking atau status prioritas di tampilan ini.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    display_data = df_display[[
        "nama_mitra_tampil",
        "jumlah_realisasi",
        "outstanding",
        "kolektabilitas_bumn",
        "accrued_interest",
        "nilai_saw",
    ]].copy()

    display_data = display_data.rename(columns={
        "nama_mitra_tampil": "Nama Mitra",
        "jumlah_realisasi": "Jumlah Realisasi",
        "outstanding": "Outstanding",
        "kolektabilitas_bumn": "Kolektabilitas",
        "accrued_interest": "Accrued Interest",
        "nilai_saw": "Nilai SAW",
    })

    st.markdown(
        f'<div class="small-note">Data yang ditampilkan: <b>{len(display_data)}</b> baris dari hasil filter SAW.</div>',
        unsafe_allow_html=True,
    )

    st.dataframe(
        style_currency_table(
            display_data,
            currency_cols=["Jumlah Realisasi", "Outstanding", "Accrued Interest"],
            decimal_cols=["Nilai SAW"],
            highlight_cols=["Nilai SAW"],
        ),
        width="stretch",
        hide_index=True,
    )

    csv = display_data.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "data_mitra_saw.csv", "text/csv", width="content")

elif menu == "Perhitungan SAW":
    st.markdown(
        """
        <div class="section-card">
            <div class="section-label">Perhitungan SAW</div>
            <div class="section-heading">Detail proses normalisasi dan bobot</div>
            <div class="section-copy">
                Pilih satu mitra untuk melihat nilai awal, hasil normalisasi, bobot, dan nilai terbobot setiap kriteria.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    selected_mitra = st.selectbox("Pilih Nama Mitra", options=df_display["nama_mitra_tampil"].dropna().unique())
    detail = df_display[df_display["nama_mitra_tampil"] == selected_mitra].iloc[0]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric("Jumlah Realisasi", smart_rupiah(detail["jumlah_realisasi"]), "Nilai awal C1", "accent-primary")
    with col2:
        render_metric("Outstanding", smart_rupiah(detail["outstanding"]), "Nilai awal C2", "accent-secondary")
    with col3:
        render_metric("Kolektabilitas", str(detail["kolektabilitas_bumn"]), "Kategori C3", "accent-warning")
    with col4:
        render_metric("Accrued Interest", smart_rupiah(detail["accrued_interest"]), "Nilai awal C4", "accent-danger")

    st.subheader(f"Proses SAW: {detail['nama_mitra_tampil']}")
    saw_detail = pd.DataFrame(
        {
            "Kriteria": ["C1 Jumlah Realisasi", "C2 Outstanding", "C3 Kolektabilitas", "C4 Accrued Interest"],
            "Nilai Awal": [detail["jumlah_realisasi"], detail["outstanding"], detail["skor_kolektabilitas"], detail["accrued_interest"]],
            "Normalisasi": [detail["c1_normalisasi"], detail["c2_normalisasi"], detail["c3_normalisasi"], detail["c4_normalisasi"]],
            "Bobot": [0.40, 0.30, 0.20, 0.10],
        }
    )
    saw_detail["Nilai Terbobot"] = saw_detail["Normalisasi"] * saw_detail["Bobot"]

    st.dataframe(
        style_currency_table(
            saw_detail,
            currency_cols=["Nilai Awal"],
            decimal_cols=["Normalisasi", "Bobot", "Nilai Terbobot"],
            highlight_cols=["Nilai Terbobot"],
        ),
        width="stretch",
        hide_index=True,
    )

    st.success(f"Nilai SAW = {detail['nilai_saw']:.4f}")
    csv = saw_detail.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, f"perhitungan_saw_{selected_mitra}.csv", "text/csv", width="content")

elif menu == "Detail Mitra":
    st.markdown(
        """
        <div class="section-card">
            <div class="section-label">Detail Mitra</div>
            <div class="section-heading">Ringkasan lengkap satu mitra</div>
            <div class="section-copy">
                Halaman ini menampilkan detail nilai awal, normalisasi, dan hasil akhir SAW untuk satu mitra yang dipilih.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    selected_mitra = st.selectbox("Pilih Nama Mitra", options=df_display["nama_mitra_tampil"].dropna().unique())
    detail = df_display[df_display["nama_mitra_tampil"] == selected_mitra].iloc[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        render_metric("Nilai SAW", f"{detail['nilai_saw']:.4f}", "Hasil akhir perhitungan", "accent-success")
    with col2:
        render_metric("Kolektabilitas", str(detail["kolektabilitas_bumn"]), "Kategori input data", "accent-warning")
    with col3:
        render_metric("Skor Kolektabilitas", str(int(detail["skor_kolektabilitas"])), "Skor yang dipakai pada C3", "accent-secondary")

    st.divider()

    raw_col1, raw_col2, raw_col3 = st.columns(3)
    with raw_col1:
        st.info(f"Jumlah Realisasi\n\n{smart_rupiah(detail['jumlah_realisasi'])}")
    with raw_col2:
        st.info(f"Outstanding\n\n{smart_rupiah(detail['outstanding'])}")
    with raw_col3:
        st.info(f"Accrued Interest\n\n{smart_rupiah(detail['accrued_interest'])}")

    detail_table = pd.DataFrame(
        {
            "Kriteria": ["C1 Jumlah Realisasi", "C2 Outstanding", "C3 Kolektabilitas", "C4 Accrued Interest"],
            "Nilai Awal": [detail["jumlah_realisasi"], detail["outstanding"], detail["skor_kolektabilitas"], detail["accrued_interest"]],
            "Normalisasi": [detail["c1_normalisasi"], detail["c2_normalisasi"], detail["c3_normalisasi"], detail["c4_normalisasi"]],
            "Bobot": [0.40, 0.30, 0.20, 0.10],
        }
    )
    detail_table["Nilai Terbobot"] = detail_table["Normalisasi"] * detail_table["Bobot"]

    st.subheader("Tabel Normalisasi SAW")
    st.dataframe(
        style_currency_table(
            detail_table,
            currency_cols=["Nilai Awal"],
            decimal_cols=["Normalisasi", "Bobot", "Nilai Terbobot"],
            highlight_cols=["Nilai Terbobot"],
        ),
        width="stretch",
        hide_index=True,
    )

    st.success(f"Nilai akhir SAW untuk {detail['nama_mitra_tampil']} adalah {detail['nilai_saw']:.4f}.")
    csv = detail_table.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, f"detail_mitra_{selected_mitra}.csv", "text/csv", width="content")
