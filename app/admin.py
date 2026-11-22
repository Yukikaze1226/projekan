from tabulate import tabulate
from app.db import koneksi
from app.auth import bersihkan_layar


def menu_admin(user):
    while True:
        bersihkan_layar()
        print("===== MENU ADMIN =====")
        print("Login sebagai:", user[1])
        print("1. Kelola Akun Pengguna")
        print("2. Kelola Data Master")
        print("3. Kelola Data Pemasok")
        print("4. Periksa dan Setujui Permintaan")
        print("5. Cetak Laporan")
        print("0. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            kelola_akun(user)
        elif pilihan == "2":
            kelola_data_master()
        elif piliham == "0":
            break
        else:
            print("Fitur ini belum dibuat.")
            input("Tekan Enter untuk melanjutkan...")


def ambil_akun():
    conn = koneksi()
    cur = conn.cursor()
    cur.execute(
        """SELECT users.id_users, users.nama, users.username, role.nama_role, users.status
           FROM users
           JOIN role ON users.id_role = role.id_role
           ORDER BY users.id_users""")
    data = cur.fetchall()
    conn.close()
    return data

def kelola_akun(user):
    while True:
        bersihkan_layar()

        data = ambil_akun()
        print(tabulate(data, headers=["ID", "Nama", "Username", "Role", "Aktif"], tablefmt="fancy_grid"))

        print("=== Kelola Akun Pengguna ===")
        print("1. Tambah Akun")
        print("2. Ubah Akun")
        print("3. Nonaktifkan Akun")
        print("4. Kembali")

        pilihan = input("Pilih menu (1/2/3/4): ")

        if pilihan == "1":
            tambah_akun()
        elif pilihan == "2":
            ubah_akun()
        elif pilihan == "3":
            nonaktifkan_akun(user[0])
        elif pilihan == "4":
            break
        else:
            print("Pilihan tidak valid!")
            input("Tekan Enter untuk melanjutkan...")

def tambah_akun():
    bersihkan_layar()
    print("=== Tambah Akun ===")

    # 1. Ambil data dari pengguna
    nama = input("Nama lengkap: ")
    username = input("Username: ")
    password = input("Password: ")
    no_hp = input("No. HP: ")
    alamat = input("Alamat: ")
    print("Role: 1. Admin   2. Petugas   3. Petani")
    id_role = input("Pilih role (1/2/3): ")

    if nama == "" or username == "" or password == "" or no_hp == "" or alamat == "":
        print("Semua data wajib diisi!")
        input("Tekan Enter untuk melanjutkan...")
        return
    if id_role not in ["1", "2", "3"]:
        print("Pilihan role tidak valid!")
        input("Tekan Enter untuk melanjutkan...")
        return
    conn = koneksi()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username = %s OR no_hp = %s",
        (username, no_hp),)
    sudah_ada = cur.fetchone()

    if sudah_ada is not None:
        print("Username atau No. HP sudah dipakai!")
    else:
        cur.execute(
            """INSERT INTO users (nama, username, password, no_hp, alamat, status, id_role)
               VALUES (%s, %s, %s, %s, %s, TRUE, %s)""",
            (nama, username, password, no_hp, alamat, id_role),)
        conn.commit()
        print("Akun berhasil ditambahkan!")

    conn.close()
    input("Tekan Enter untuk melanjutkan...")


def ubah_akun():
    bersihkan_layar()

    data = ambil_akun()
    print(tabulate(data, headers=["ID", "Nama", "Username", "Role", "Aktif"], tablefmt="fancy_grid"))

    print("=== Ubah Akun ===")
    id_user = input("Masukkan ID akun yang akan diubah: ")

    ditemukan = False
    for baris in data:
        if str(baris[0]) == id_user:
            ditemukan = True

    if ditemukan == False:
        print("Akun tidak ditemukan!")
        input("Tekan Enter untuk melanjutkan...")
        return

    nama = input("Nama baru: ")
    no_hp = input("No. HP baru: ")
    alamat = input("Alamat baru: ")
    print("Role: 1. Admin   2. Petugas   3. Petani")
    id_role = input("Role baru (1/2/3): ")

    if nama == "" or no_hp == "" or alamat == "":
        print("Semua data wajib diisi!")
        input("Tekan Enter untuk melanjutkan...")
        return

    if id_role not in ["1", "2", "3"]:
        print("Pilihan role tidak valid!")
        input("Tekan Enter untuk melanjutkan...")
        return

    conn = koneksi()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE no_hp = %s AND id_users != %s",
        (no_hp, id_user),)
    sudah_ada = cur.fetchone()
    if sudah_ada is not None:
        print("No. HP sudah dipakai akun lain!")
    else:
        cur.execute(
            "UPDATE users SET nama = %s, no_hp = %s, alamat = %s, id_role = %s WHERE id_users = %s",
            (nama, no_hp, alamat, id_role, id_user),)
        conn.commit()
        print("Akun berhasil diubah!")
    conn.close()
    input("Tekan Enter untuk melanjutkan...")


def nonaktifkan_akun(id_login):
    bersihkan_layar()

    data = ambil_akun()
    print(tabulate(data, headers=["ID", "Nama", "Username", "Role", "Aktif"], tablefmt="fancy_grid"))

    print("=== Nonaktifkan Akun ===")
    id_user = input("Masukkan ID akun yang akan dinonaktifkan: ")

    # 1. Admin tidak boleh menonaktifkan akunnya sendiri
    if id_user == str(id_login):
        print("Anda tidak dapat menonaktifkan akun yang sedang digunakan!")
        input("Tekan Enter untuk melanjutkan...")
        return
        
    ditemukan = False
    nama_akun = ""
    for baris in data:
        if str(baris[0]) == id_user:
            ditemukan = True
            nama_akun = baris[1]

    if ditemukan == False:
        print("Akun tidak ditemukan!")
        input("Tekan Enter untuk melanjutkan...")
        return

    yakin = input("Nonaktifkan akun " + nama_akun + "? (y/n): ")

    if yakin == "y":
        conn = koneksi()
        cur = conn.cursor()
        cur.execute("UPDATE users SET status = FALSE WHERE id_users = %s", (id_user,))
        conn.commit()
        conn.close()
        print("Akun berhasil dinonaktifkan.")
    else:
        print("Dibatalkan.")

    input("Tekan Enter untuk melanjutkan...")



def kelola_data_master():
    while True:
        bersihkan_layar()
        print("=== Kelola Data Master ===")
        print("1. Kategori Barang")
        print("2. Satuan Barang")
        print("3. Batas Minimum Stok")
        print("4. Kembali")

        pilihan = input("Pilih menu (1/2/3/4): ")

        if pilihan == "1":
            kelola_kategori()
        elif pilihan == "2":
            kelola_satuan()
        elif pilihan == "3":
            kelola_batas_minimum()
        elif pilihan == "4":
            break
        else:
            print("Pilihan tidak valid!")
            input("Tekan Enter untuk melanjutkan...")


def ambil_kategori():
    conn = koneksi()
    cur = conn.cursor()
    cur.execute("SELECT id_kategori, nama_kategori FROM kategori ORDER BY id_kategori")
    data = cur.fetchall()
    conn.close()
    return data


def kelola_kategori():
    while True:
        bersihkan_layar()

        data = ambil_kategori()
        print(tabulate(data, headers=["ID", "Nama Kategori"], tablefmt="fancy_grid"))

        print("=== Kelola Kategori Barang ===")
        print("1. Tambah Kategori")
        print("2. Ubah Kategori")
        print("3. Kembali")

        pilihan = input("Pilih menu (1/2/3): ")

        if pilihan == "1":
            tambah_kategori()
        elif pilihan == "2":
            ubah_kategori()
        elif pilihan == "3":
            break
        else:
            print("Pilihan tidak valid!")
            input("Tekan Enter untuk melanjutkan...")


def tambah_kategori():
    bersihkan_layar()
    print("=== Tambah Kategori ===")
    nama = input("Nama kategori: ")

    if nama == "":
        print("Nama kategori wajib diisi!")
        input("Tekan Enter untuk melanjutkan...")
        return

    conn = koneksi()
    cur = conn.cursor()
    cur.execute("SELECT * FROM kategori WHERE nama_kategori = %s", (nama,))
    sudah_ada = cur.fetchone()

    if sudah_ada is not None:
        print("Kategori sudah ada!")
    else:
        cur.execute("INSERT INTO kategori (nama_kategori) VALUES (%s)", (nama,))
        conn.commit()
        print("Kategori berhasil ditambahkan!")

    conn.close()
    input("Tekan Enter untuk melanjutkan...")


def ubah_kategori():
    bersihkan_layar()
    data = ambil_kategori()
    print(tabulate(data, headers=["ID", "Nama Kategori"], tablefmt="fancy_grid"))

    print("=== Ubah Kategori ===")
    id_kategori = input("Masukkan ID kategori yang akan diubah: ")

    ditemukan = False
    for baris in data:
        if str(baris[0]) == id_kategori:
            ditemukan = True
    if ditemukan == False:
        print("Kategori tidak ditemukan!")
        input("Tekan Enter untuk melanjutkan...")
        return
        
    nama = input("Nama kategori baru: ")

    if nama == "":
        print("Nama kategori wajib diisi!")
        input("Tekan Enter untuk melanjutkan...")
        return

    conn = koneksi()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM kategori WHERE nama_kategori = %s AND id_kategori != %s",
        (nama, id_kategori),)
    sudah_ada = cur.fetchone()
    if sudah_ada is not None:
        print("Nama kategori sudah dipakai!")
    else:
        cur.execute(
            "UPDATE kategori SET nama_kategori = %s WHERE id_kategori = %s",
            (nama, id_kategori),)
        conn.commit()
        print("Kategori berhasil diubah!")

    conn.close()
    input("Tekan Enter untuk melanjutkan...")


def ambil_barang():
    conn = koneksi()
    cur = conn.cursor()
    cur.execute(
        """SELECT id_barang, nama_barang, satuan, stok, batas_minimum
           FROM barang
           ORDER BY id_barang"""
    )
    data = cur.fetchall()
    conn.close()
    return data


def ambil_satuan():
    conn = koneksi()
    cur = conn.cursor()
    cur.execute("SELECT unnest(enum_range(NULL::jenis_satuan))")
    data = cur.fetchall()
    conn.close()

    daftar = []
    for baris in data:
        daftar.append(baris[0])
    return daftar


def kelola_satuan():
    while True:
        bersihkan_layar()
        
        daftar_satuan = ambil_satuan()
        print("Satuan yang tersedia:", daftar_satuan)

        data = ambil_barang()
        print(tabulate(data, headers=["ID", "Nama Barang", "Satuan", "Stok", "Batas Minimum"], tablefmt="fancy_grid"))

        print("=== Kelola Satuan Barang ===")
        print("1. Ubah Satuan Barang")
        print("2. Kembali")

        pilihan = input("Pilih menu (1/2): ")

        if pilihan == "1":
            ubah_satuan(data, daftar_satuan)
        elif pilihan == "2":
            break
        else:
            print("Pilihan tidak valid!")
            input("Tekan Enter untuk melanjutkan...")


def ubah_satuan(data, daftar_satuan):
    id_barang = input("Masukkan ID barang yang akan diubah satuannya: ")

    ditemukan = False
    for baris in data:
        if str(baris[0]) == id_barang:
            ditemukan = True

    if ditemukan == False:
        print("Barang tidak ditemukan!")
        input("Tekan Enter untuk melanjutkan...")
        return
    satuan = input("Satuan baru: ")

    if satuan not in daftar_satuan:
        print("Satuan tidak tersedia!")
        input("Tekan Enter untuk melanjutkan...")
        return

    conn = koneksi()
    cur = conn.cursor()
    cur.execute("UPDATE barang SET satuan = %s WHERE id_barang = %s", (satuan, id_barang))
    conn.commit()
    conn.close()

    print("Satuan barang berhasil diubah!")
    input("Tekan Enter untuk melanjutkan...")


def kelola_batas_minimum():
    while True:
        bersihkan_layar()

        data = ambil_barang()
        print(tabulate(data, headers=["ID", "Nama Barang", "Satuan", "Stok", "Batas Minimum"], tablefmt="fancy_grid"))

        print("=== Kelola Batas Minimum Stok ===")
        print("1. Ubah Batas Minimum")
        print("2. Kembali")

        pilihan = input("Pilih menu (1/2): ")

        if pilihan == "1":
            ubah_batas_minimum(data)
        elif pilihan == "2":
            break
        else:
            print("Pilihan tidak valid!")
            input("Tekan Enter untuk melanjutkan...")

def ubah_batas_minimum(data):
    id_barang = input("Masukkan ID barang yang akan diubah batas minimumnya: ")
    ditemukan = False
    for baris in data:
        if str(baris[0]) == id_barang:
            ditemukan = True

    if ditemukan == False:
        print("Barang tidak ditemukan!")
        input("Tekan Enter untuk melanjutkan...")
        return
    batas = input("Batas minimum baru: ")

    if batas.isdigit() == False:
        print("Batas minimum harus berupa angka!")
        input("Tekan Enter untuk melanjutkan...")
        return
    conn = koneksi()
    cur = conn.cursor()
    cur.execute("UPDATE barang SET batas_minimum = %s WHERE id_barang = %s", (batas, id_barang))
    conn.commit()
    conn.close()

    print("Batas minimum berhasil diubah!")
    input("Tekan Enter untuk melanjutkan...")
