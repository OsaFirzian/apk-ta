from flask import Flask, render_template, request, redirect, url_for, session
import pymysql

app = Flask(__name__)
app.secret_key = 'key_apk-ta'

# =======================================================
# 1. KONFIGURASI DATABASE
# =======================================================
def get_db_connection():
    """Fungsi ini menjembatani Flask dengan MySQL di Laragon"""
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='apk-ta',
        cursorclass=pymysql.cursors.DictCursor
    )

# =======================================================
# 2. ROUTING AUTENTIKASI (LOGIN)
# =======================================================
@app.route('/', methods=['GET', 'POST'])
def login():
    pesan_error = None
    if request.method == 'POST':
        input_username = request.form['username']
        input_password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM tabel_user WHERE BINARY username = %s AND BINARY password = %s"
        cursor.execute(query, (input_username, input_password))
        user_cocok = cursor.fetchone()
        cursor.close()
        conn.close()

        if user_cocok:
            # SIMPAN DATA KE SESSION SAAT BERHASIL LOGIN
            session['username'] = user_cocok['username']
            session['role'] = user_cocok['role']
            return redirect(url_for('home'))
        else:
            pesan_error = "Username atau Password salah!"

    return render_template('login.html', error=pesan_error)

# FUNGSI BARU: LOGOUT
@app.route('/logout')
def logout():
    session.clear() # Hapus KTP sementara
    return redirect(url_for('login'))

# FUNGSI BARU: KELOLA PENGGUNA
@app.route('/kelola_pengguna', methods=['GET', 'POST'])
def kelola_pengguna():
    # CEK KEAMANAN: Jika belum login atau BUKAN admin, tendang ke Dashboard!
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('home'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Logika untuk Tambah User Baru
    if request.method == 'POST':
        user_baru = request.form['username']
        pass_baru = request.form['password']
        role_baru = request.form['role']
        
        cursor.execute("INSERT INTO tabel_user (username, password, role) VALUES (%s, %s, %s)", 
                       (user_baru, pass_baru, role_baru))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('kelola_pengguna'))

    # Ambil semua data user untuk ditampilkan di tabel
    cursor.execute("SELECT * FROM tabel_user")
    semua_user = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('kelola_pengguna.html', data_user=semua_user)

# =======================================================
# 3. ROUTING MENU UTAMA & DIAGNOSA (CBR ENGINE)
# =======================================================
# =======================================================
# 1. RUTE DASHBOARD UTAMA
# =======================================================
@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Ambil Angka untuk Summary Cards
    cursor.execute("SELECT COUNT(*) AS total FROM tabel_kasus WHERE status_kasus = 'Terverifikasi'")
    total_kb = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) AS total FROM tabel_kasus WHERE status_kasus = 'Menunggu Review'")
    total_pending = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) AS total FROM tabel_parameter")
    total_param = cursor.fetchone()['total']

    # 2. Ambil Data untuk Pie Chart (Distribusi Perangkat)
    cursor.execute("SELECT jenis_perangkat, COUNT(*) AS jumlah FROM tabel_kasus GROUP BY jenis_perangkat")
    chart_perangkat = cursor.fetchall()

    # 3. Ambil Data untuk Pie Chart (Tren Problem Zabbix)
    cursor.execute("SELECT kategori_problem, COUNT(*) AS jumlah FROM tabel_kasus GROUP BY kategori_problem")
    chart_problem = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('home.html', 
                           total_kb=total_kb, 
                           total_pending=total_pending, 
                           total_param=total_param, 
                           chart_perangkat=chart_perangkat, 
                           chart_problem=chart_problem)

# =======================================================
# 2. RUTE FORM DIAGNOSA GANGGUAN
# =======================================================
@app.route('/diagnosa')
def diagnosa():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT kategori, nilai FROM tabel_parameter")
    data_param = cursor.fetchall()
    cursor.close()
    conn.close()

    opsi_tambahan = {
        'jenis_perangkat': [], 'kategori_problem': [], 'dampak_gangguan': [],
        'akses_remote': [], 'status_fisik': [], 'kondisi_kabel': []
    }
    for row in data_param:
        kategori = row['kategori']
        if kategori in opsi_tambahan:
            opsi_tambahan[kategori].append(row['nilai'])

    return render_template('diagnosa.html', opsi_tambahan=opsi_tambahan)

@app.route('/proses_diagnosa', methods=['POST'])
def proses_diagnosa():
    # Mengambil input dari form
    input_kasus = {
        'jenis_perangkat': request.form.get('jenis_perangkat'),
        'kategori_problem': request.form.get('kategori_problem'),
        'dampak_gangguan': request.form.get('dampak_gangguan'),
        'akses_remote': request.form.get('akses_remote'),
        'status_fisik': request.form.get('status_fisik'),
        'kondisi_kabel': request.form.get('kondisi_kabel')
    }

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tabel_kasus WHERE status_kasus = 'Terverifikasi'")
    data_kb = cursor.fetchall()

    bobot = {
        'jenis_perangkat': 2,
        'kategori_problem': 4,
        'dampak_gangguan': 5,
        'akses_remote': 3,
        'status_fisik': 5,
        'kondisi_kabel': 4
    }
    total_bobot = sum(bobot.values())

    hasil_perhitungan = []
    for row in data_kb:
        skor_mirip = 0
        for fitur in bobot.keys():
            if str(input_kasus[fitur]).strip().lower() == str(row[fitur]).strip().lower():
                skor_mirip += bobot[fitur]

        persentase = (skor_mirip / total_bobot) * 100
        hasil_perhitungan.append({
            'persentase': round(persentase, 2),
            'diagnosis': row['diagnosis'],
            'solusi': row['solusi']
        })

    # Urutkan dari persentase tertinggi ke terendah
    hasil_perhitungan = sorted(hasil_perhitungan, key=lambda x: x['persentase'], reverse=True)
    
    # AMBIL 3 KASUS TERBAIK (TOP 3)
    top_3_kasus = hasil_perhitungan[:3]
    
    # Ambil kasus Peringkat 1 untuk disimpan sementara di database (Fase Retain)
    kasus_terbaik = top_3_kasus[0] 

    query_insert = """
    INSERT INTO tabel_kasus 
    (jenis_perangkat, kategori_problem, dampak_gangguan, akses_remote, status_fisik, kondisi_kabel, diagnosis, solusi, status_kasus)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Menunggu Review')
    """
    cursor.execute(query_insert, (
        input_kasus['jenis_perangkat'], input_kasus['kategori_problem'], 
        input_kasus['dampak_gangguan'], input_kasus['akses_remote'], 
        input_kasus['status_fisik'], input_kasus['kondisi_kabel'],
        kasus_terbaik['diagnosis'], kasus_terbaik['solusi'] 
    ))
    conn.commit()
    cursor.close()
    conn.close()

    # Memecah teks solusi menjadi poin-poin UNTUK SEMUA kasus di Top 3
    for kasus in top_3_kasus:
        daftar_solusi = str(kasus['solusi']).split('|')
        kasus['daftar_solusi'] = [s.strip() for s in daftar_solusi if s.strip()]

    # Kirim data top_3 ke halaman HTML
    return render_template('hasil_diagnosa.html', top_kasus=top_3_kasus)

# =======================================================
# 4. ROUTING MANAJEMEN KASUS (VALIDASI & KNOWLEDGE BASE)
# =======================================================

# 1. HALAMAN VALIDASI KASUS (MENUNGGU REVIEW)
@app.route('/validasi_kasus')
def validasi_kasus():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    # Hanya ambil data yang Menunggu Review
    cursor.execute("SELECT * FROM tabel_kasus WHERE status_kasus = 'Menunggu Review' ORDER BY id_kasus DESC")
    data_kasus = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('validasi_kasus.html', data_kasus=data_kasus)

# 2. HALAMAN KNOWLEDGE BASE (TERVERIFIKASI)
@app.route('/knowledge_base')
def knowledge_base():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Kembalikan ke default sorting berdasarkan ID
    query = "SELECT * FROM tabel_kasus WHERE status_kasus = 'Terverifikasi' ORDER BY id_kasus ASC"
    
    cursor.execute(query)
    data_kasus = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('knowledge_base.html', data_kasus=data_kasus)

# 3. MENGEDIT DIAGNOSIS DAN SOLUSI KASUS
@app.route('/edit_kasus/<int:id_kasus>', methods=['GET', 'POST'])
def edit_kasus(id_kasus):
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        diagnosis_baru = request.form['diagnosis']
        solusi_baru = request.form['solusi']
        status_baru = request.form['status_kasus']

        query_update = "UPDATE tabel_kasus SET diagnosis=%s, solusi=%s, status_kasus=%s WHERE id_kasus=%s"
        cursor.execute(query_update, (diagnosis_baru, solusi_baru, status_baru, id_kasus))
        conn.commit()
        cursor.close()
        conn.close()
        
        # Setelah diedit, kembalikan user ke halaman Validasi
        return redirect(url_for('validasi_kasus'))

    else:
        cursor.execute("SELECT * FROM tabel_kasus WHERE id_kasus = %s", (id_kasus,))
        kasus = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('edit_kasus.html', kasus=kasus)


# FUNGSI BARU: RESET PASSWORD
@app.route('/reset_password/<username>')
def reset_password(username):
    # Keamanan ekstra: Pastikan hanya admin yang bisa melakukan ini
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('home'))

    conn = get_db_connection()
    cursor = conn.cursor()
    # Ubah password menjadi 123456 untuk user yang dipilih
    query = "UPDATE tabel_user SET password = '123456' WHERE username = %s"
    cursor.execute(query, (username,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('kelola_pengguna'))

# FUNGSI BARU: HAPUS USER
@app.route('/hapus_user/<username>')
def hapus_user(username):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('home'))
        
    # Mencegah admin menghapus dirinya sendiri secara tidak sengaja
    if username == session.get('username'):
        return redirect(url_for('kelola_pengguna'))

    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM tabel_user WHERE username = %s"
    cursor.execute(query, (username,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('kelola_pengguna'))

# FUNGSI BARU: UBAH PASSWORD MANDIRI (UNTUK ALL ROLE)
@app.route('/ubah_password', methods=['GET', 'POST'])
def ubah_password():
    # Keamanan: Pastikan user sudah login, jika belum arahkan ke login
    if 'username' not in session:
        return redirect(url_for('login'))

    pesan = None
    status_alert = None

    if request.method == 'POST':
        pass_lama = request.form['password_lama']
        pass_baru = request.form['password_baru']
        konfirmasi_pass = request.form['konfirmasi_password']

        # 1. Validasi apakah password baru dan konfirmasi cocok
        if pass_baru != konfirmasi_pass:
            pesan = "Konfirmasi password baru tidak cocok!"
            status_alert = "error"
        else:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # 2. Validasi apakah password lama yang diinput sudah benar
            query_cek = "SELECT * FROM tabel_user WHERE username = %s AND password = %s"
            cursor.execute(query_cek, (session['username'], pass_lama))
            user_valid = cursor.fetchone()

            if user_valid:
                # 3. Jika benar, lakukan update password baru
                query_update = "UPDATE tabel_user SET password = %s WHERE username = %s"
                cursor.execute(query_update, (pass_baru, session['username']))
                conn.commit()
                pesan = "Password berhasil diperbarui!"
                status_alert = "sukses"
            else:
                pesan = "Password lama yang Anda masukkan salah!"
                status_alert = "error"
            
            cursor.close()
            conn.close()

    return render_template('ubah_password.html', pesan=pesan, status=status_alert)

# FUNGSI BARU: MANAJEMEN PARAMETER (KHUSUS ADMIN)
@app.route('/manajemen_parameter', methods=['GET', 'POST'])
def manajemen_parameter():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('home'))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        kategori = request.form['kategori']
        nilai = request.form['nilai']
        
        cursor.execute("INSERT INTO tabel_parameter (kategori, nilai) VALUES (%s, %s)", (kategori, nilai))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('manajemen_parameter'))

    # Ambil semua data parameter dan urutkan berdasarkan kategorinya
    cursor.execute("SELECT * FROM tabel_parameter ORDER BY kategori ASC, nilai ASC")
    data_param = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('manajemen_parameter.html', data_param=data_param)

# FUNGSI BARU: HAPUS PARAMETER
@app.route('/hapus_parameter/<int:id_param>')
def hapus_parameter(id_param):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('home'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tabel_parameter WHERE id_param = %s", (id_param,))
    conn.commit()
    cursor.close()
    conn.close()

# =======================================================
# PUSAT LAPORAN
# =======================================================
@app.route('/laporan')
def laporan():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Ambil semua kasus untuk dipisah di Python
    cursor.execute("SELECT * FROM tabel_kasus ORDER BY id_kasus DESC")
    semua_kasus = cursor.fetchall()

    # 2. Ambil data statistik perangkat
    cursor.execute("SELECT jenis_perangkat, COUNT(*) AS jumlah FROM tabel_kasus GROUP BY jenis_perangkat")
    stat_perangkat = cursor.fetchall()
    
    # 3. Ambil data statistik problem
    cursor.execute("SELECT kategori_problem, COUNT(*) AS jumlah FROM tabel_kasus GROUP BY kategori_problem")
    stat_problem = cursor.fetchall()

    # 4. Ambil daftar perangkat unik untuk filter Dropdown
    cursor.execute("SELECT DISTINCT jenis_perangkat FROM tabel_kasus WHERE status_kasus = 'Terverifikasi'")
    list_perangkat = cursor.fetchall()

    cursor.close()
    conn.close()

    # Pisahkan kasus berdasarkan status
    kasus_terverifikasi = [k for k in semua_kasus if k['status_kasus'] == 'Terverifikasi']
    kasus_pending = [k for k in semua_kasus if k['status_kasus'] == 'Menunggu Review']

    return render_template('laporan.html', 
                           kasus_terverifikasi=kasus_terverifikasi,
                           kasus_pending=kasus_pending,
                           stat_perangkat=stat_perangkat,
                           stat_problem=stat_problem,
                           list_perangkat=list_perangkat)
    
    return redirect(url_for('manajemen_parameter'))

# =======================================================
# 5. MENJALANKAN SERVER FLASK
# =======================================================
if __name__ == '__main__':
    app.run(debug=True)