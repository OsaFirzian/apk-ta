from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# Fungsi untuk menghubungkan Python ke MySQL (Laragon)
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='apk-ta', # Nama database sesuai instruksi
        cursorclass=pymysql.cursors.DictCursor
    )

# Route untuk halaman utama (Login)
@app.route('/', methods=['GET', 'POST'])
def login():
    pesan_error = None
    
    # Jika user menekan tombol submit (metode POST)
    if request.method == 'POST':
        input_username = request.form['username']
        input_password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        
        # PERHATIAN: Penggunaan 'BINARY' memaksa pencarian menjadi Case Sensitive
        # %s digunakan untuk mencegah celah keamanan SQL Injection
        query = "SELECT * FROM tabel_user WHERE BINARY username = %s AND BINARY password = %s"
        cursor.execute(query, (input_username, input_password))
        
        # Mengambil 1 baris hasil pencarian
        user_cocok = cursor.fetchone()
        
        cursor.close()
        conn.close()

        # Logika Verifikasi
        if user_cocok:
            # Jika data cocok, arahkan ke halaman home
            return redirect(url_for('home'))
        else:
            # Jika gagal, kembalikan pesan error
            pesan_error = "Username atau Password salah!"

    # Tampilkan halaman login (beserta pesan error jika ada)
    return render_template('login.html', error=pesan_error)

# Route untuk halaman tujuan setelah berhasil login
@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)