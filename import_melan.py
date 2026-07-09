import pandas as pd
import pymysql
import numpy as np
import math
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent


def find_excel_file():
    preferred_names = [
        "data melan ini yang bener.xlsx",
        "data melan ini yang bener .xlsx",
    ]

    for name in preferred_names:
        candidate = PROJECT_DIR / name
        if candidate.exists():
            return candidate

    excel_files = sorted(PROJECT_DIR.glob("*.xlsx"))
    if excel_files:
        return excel_files[0]

    raise FileNotFoundError("Tidak ada file Excel .xlsx yang ditemukan di folder project.")


FILE_EXCEL = find_excel_file()

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="db_melan",
    charset="utf8mb4"
)

cursor = conn.cursor()

df = pd.read_excel(FILE_EXCEL)

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)

print("Kolom terbaca:")
print(df.columns.tolist())
print(f"File Excel yang dipakai: {FILE_EXCEL.name}")

def clean_value(value):
    if value is None:
        return None

    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None

    if pd.isna(value):
        return None

    return value

sql = """
INSERT INTO tb_import_melan (
    nama_debitur,
    cabang,
    jumlah_realisasi,
    outstanding,
    kolektabilitas_bumn,
    accrued_interest,
    c1,
    c2,
    c3,
    c4,
    nilai_akhir,
    ranking
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

data = []

for _, row in df.iterrows():
    data.append((
        clean_value(row.get("nama_mitra_binaan")),
        None,
        clean_value(row.get("c1_jumlah_realisasi_(rp)")),
        clean_value(row.get("c2_outstanding_(rp)")),
        clean_value(row.get("c3_kolektabilitas_bumn")),
        clean_value(row.get("c4_accrued_interest")),
        clean_value(row.get("c1")),
        clean_value(row.get("c2")),
        clean_value(row.get("c3")),
        clean_value(row.get("c4")),
        clean_value(row.get("nilai_saw")),
        None
    ))

cursor.execute("TRUNCATE TABLE tb_import_melan")
cursor.executemany(sql, data)
conn.commit()

print(f"Berhasil import {len(data)} data ke tb_import_melan")

cursor.close()
conn.close()