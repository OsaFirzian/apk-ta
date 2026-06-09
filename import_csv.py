import pandas as pd
import pymysql

# 1. Baca file CSV
df = pd.read_csv('knowledge_base.csv', skiprows=1)

# 2. Buka jembatan ke MySQL
koneksi = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='apk-ta'
)
cursor = koneksi.cursor()

# 3. Masukkan data baris demi baris
for index, row in df.iterrows():
    query = """
    INSERT INTO tabel_kasus 
    (jenis_perangkat, kategori_problem, dampak_gangguan, akses_remote, status_fisik, kondisi_kabel, diagnosis, solusi, status_kasus)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Terverifikasi')
    """
    # Pastikan mengatasi nilai kosong (NaN) dari Excel
    nilai = (
        str(row['Jenis_Perangkat']) if pd.notna(row['Jenis_Perangkat']) else '',
        str(row['Kategori_Problem']) if pd.notna(row['Kategori_Problem']) else '',
        str(row['Dampak_Gangguan']) if pd.notna(row['Dampak_Gangguan']) else '',
        str(row['Akses_Remote']) if pd.notna(row['Akses_Remote']) else '',
        str(row['Status_Fisik']) if pd.notna(row['Status_Fisik']) else '',
        str(row['Kondisi_Kabel']) if pd.notna(row['Kondisi_Kabel']) else '',
        str(row['Diagnosis']) if pd.notna(row['Diagnosis']) else '',
        str(row['Solusi']) if pd.notna(row['Solusi']) else ''
    )
    cursor.execute(query, nilai)

# Simpan dan tutup
koneksi.commit()
cursor.close()
koneksi.close()

print("Data CSV berhasil dipindahkan ke MySQL!")