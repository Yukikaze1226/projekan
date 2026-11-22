import os
from app.db import koneksi

def bersihkan_layar():
    os.system("cls")

def registrasi():
    bersihkan_layar()
    print("===== REGISTRASI PETANI =====")

    nama = input("Nama lengkap: ")
    username = input("Username: ")
    password = input("Password: ")
    no_hp = input("No. HP: ")
    alamat = input("Alamat: ")

    if nama == "" or username == "" or password == "" or no_hp == "" or alamat == "":
        print("Semua data wajib diisi!")
        input("Tekan Enter untuk melanjutkan...")
        return

    try:
        conn = koneksi()
        cur = conn.cursor()
        cur.execute("SELECT id_role FROM role WHERE nama_role = 'petani'")
        id_role = cur.fetchone()[0]

        cur.execute(
            """INSERT INTO users (nama, username, password, no_hp, alamat, status, id_role)
               VALUES (%s, %s, %s, %s, %s, TRUE, %s)""",
            (nama, username, password, no_hp, alamat, id_role),)
        conn.commit()
        conn.close()
        print("Registrasi berhasil! Silakan login.")
    except Exception:
        print("Registrasi gagal. Username atau No. HP sudah dipakai.")

    input("Tekan Enter untuk melanjutkan...")

def login():
    bersihkan_layar()
    print("===== LOGIN =====")
    username = input("Username: ")
    password = input("Password: ")
    conn = koneksi()
    cur = conn.cursor()
    cur.execute(
        """SELECT users.id_users, users.nama, role.nama_role, users.status
           FROM users
           JOIN role ON users.id_role = role.id_role
           WHERE users.username = %s AND users.password = %s""",
        (username, password),)
    data = cur.fetchone() 
    conn.close()
    if data is None:
        print("Username atau password salah!")
        input("Tekan Enter untuk melanjutkan...")
        return None

    if data[3] == False:
        print("Akun Anda nonaktif. Hubungi admin!")
        input("Tekan Enter untuk melanjutkan...")
        return None

    print("Selamat datang,", data[1])
    input("Tekan Enter untuk melanjutkan...")
    return [data[0], data[1], data[2]]
