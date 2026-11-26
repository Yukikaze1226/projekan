from tabulate import tabulate
from app.db import koneksi
from app.auth import bersihkan_layar
from app.ui import tampilkan_logo


def menu_admin(user):
    while True:
        bersihkan_layar()
        tampilkan_logo()
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
        elif pilihan == "3":
            kelola_pemasok()
        elif pilihan == "4":
            periksa_permintaan()
        elif pilihan == "5":
            cetak_laporan()
        elif pilihan == "0":
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

def ambil_pemasok():
    conn = koneksi()
    cur = conn.cursor()
    cur.execute("SELECT id_pemasok, nama_pemasok, no_hp, alamat FROM pemasok ORDER BY id_pemasok")
    data = cur.fetchall()
    conn.close()
    return data

def kelola_pemasok():
    while True:
        bersihkan_layar()

        data = ambil_pemasok()
        print(tabulate(data, headers=["ID", "Nama Pemasok", "No. HP", "Alamat"], tablefmt="fancy_grid"))
        print("=== Kelola Data Pemasok ===")
        print("1. Tambah Pemasok")
        print("2. Ubah Pemasok")
        print("3. Kembali")
        pilihan = input("Pilih menu (1/2/3): ")
        if pilihan == "1":
            tambah_pemasok()
        elif pilihan == "2":
            ubah_pemasok()
        elif pilihan == "3":
            break
        else:
            print("Pilihan tidak valid!")
            input("Tekan Enter untuk melanjutkan...")

def tambah_pemasok():
    bersihkan_layar()
    print("=== Tambah Pemasok ===")
    nama = input("Nama pemasok: ")
    no_hp = input("No. HP: ")
    alamat = input("Alamat: ")
    if nama == "" or no_hp == "" or alamat == "":
        print("Semua data wajib diisi!")
        input("Tekan Enter untuk melanjutkan...")
        return
    conn = koneksi()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM pemasok WHERE nama_pemasok = %s OR no_hp = %s",
        (nama, no_hp),
    )
    sudah_ada = cur.fetchone()
    if sudah_ada is not None:
        print("Nama pemasok atau No. HP sudah dipakai!")
    else:
        cur.execute(
            "INSERT INTO pemasok (nama_pemasok, no_hp, alamat) VALUES (%s, %s, %s)",
            (nama, no_hp, alamat),
        )
        conn.commit()
        print("Pemasok berhasil ditambahkan!")
    conn.close()
    input("Tekan Enter untuk melanjutkan...")

def ubah_pemasok():
    bersihkan_layar()
    data = ambil_pemasok()
    print(tabulate(data, headers=["ID", "Nama Pemasok", "No. HP", "Alamat"], tablefmt="fancy_grid"))
    print("=== Ubah Pemasok ===")
    id_pemasok = input("Masukkan ID pemasok yang akan diubah: ")
    ditemukan = False
    for baris in data:
        if str(baris[0]) == id_pemasok:
            ditemukan = True
    if ditemukan == False:
        print("Pemasok tidak ditemukan!")
        input("Tekan Enter untuk melanjutkan...")
        return
    nama = input("Nama pemasok baru: ")
    no_hp = input("No. HP baru: ")
    alamat = input("Alamat baru: ")
    if nama == "" or no_hp == "" or alamat == "":
        print("Semua data wajib diisi!")
        input("Tekan Enter untuk melanjutkan...")
        return
        
    conn = koneksi()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM pemasok WHERE (nama_pemasok = %s OR no_hp = %s) AND id_pemasok != %s",
        (nama, no_hp, id_pemasok),
    )
    sudah_ada = cur.fetchone()
    if sudah_ada is not None:
        print("Nama pemasok atau No. HP sudah dipakai pemasok lain!")
    else:
        cur.execute(
            "UPDATE pemasok SET nama_pemasok = %s, no_hp = %s, alamat = %s WHERE id_pemasok = %s",
            (nama, no_hp, alamat, id_pemasok),
        )
        conn.commit()
        print("Pemasok berhasil diubah!")
    conn.close()
    input("Tekan Enter untuk melanjutkan...")

def ambil_permintaan_menunggu():
    conn = koneksi()
    cur = conn.cursor()
    cur.execute(
        """SELECT permintaan.id_permintaan, users.nama, barang.nama_barang,
                  permintaan.jumlah, permintaan.keperluan, barang.stok, permintaan.tanggal
           FROM permintaan
           JOIN users ON permintaan.id_users = users.id_users
           JOIN barang ON permintaan.id_barang = barang.id_barang
           WHERE permintaan.status = 'menunggu'
           ORDER BY permintaan.id_permintaan""")
    data = cur.fetchall()
    conn.close()
    return data

def periksa_permintaan():
    bersihkan_layar()

    data = ambil_permintaan_menunggu()
    if len(data) == 0:
        print("Tidak ada permintaan yang menunggu.")
        input("Tekan Enter untuk melanjutkan...")
        return
    print(tabulate(data, headers=["ID", "Nama Petani", "Nama Barang", "Jumlah", "Keperluan", "Stok Tersedia", "Tanggal"], tablefmt="fancy_grid"))
    print("=== Periksa dan Setujui Permintaan ===")
    id_permintaan = input("Masukkan ID permintaan: ")
    ditemukan = False
    jumlah = 0
    stok = 0
    for baris in data:
        if str(baris[0]) == id_permintaan:
            ditemukan = True
            jumlah = baris[3]
            stok = baris[5]
    if ditemukan == False:
        print("Permintaan tidak ditemukan!")
        input("Tekan Enter untuk melanjutkan...")
        return
    print("1. Setujui")
    print("2. Tolak")
    pilihan = input("Pilih aksi (1/2): ")
    if pilihan == "1":
        if stok < jumlah:
            print("Stok tidak mencukupi! Permintaan tidak dapat disetujui.")
            input("Tekan Enter untuk melanjutkan...")
            return
        status_baru = "disetujui"
    elif pilihan == "2":
        status_baru = "ditolak"
    else:
        print("Pilihan tidak valid!")
        input("Tekan Enter untuk melanjutkan...")
        return
    conn = koneksi()
    cur = conn.cursor()
    cur.execute(
        "UPDATE permintaan SET status = %s WHERE id_permintaan = %s",
        (status_baru, id_permintaan))
    conn.commit()
    conn.close()
    if status_baru == "disetujui":
        print("Permintaan disetujui.")
    else:
        print("Permintaan ditolak.")
    input("Tekan Enter untuk melanjutkan...")

def cetak_laporan():
    while True:
        bersihkan_layar()
        print("=== Cetak Laporan ===")
        print("1. Laporan Stok")
        print("2. Laporan Transaksi")
        print("3. Laporan Pemakaian")
        print("4. Kembali")
        pilihan = input("Pilih menu (1/2/3/4): ")
        if pilihan == "1":
            laporan_stok()
        elif pilihan == "2":
            laporan_transaksi()
        elif pilihan == "3":
            laporan_pemakaian()
        elif pilihan == "4":
            break
        else:
            print("Pilihan tidak valid!")
            input("Tekan Enter untuk melanjutkan...")
            
def simpan_ke_file(nama_file, judul, tabel):
    yakin = input("Cetak laporan ke file? (y/n): ")
    if yakin == "y":
        file = open(nama_file, "w", encoding="utf-8")
        file.write(judul + "\n")
        file.write(tabel)
        file.close()
        print("Laporan disimpan ke " + nama_file)

def laporan_stok():
    bersihkan_layar()

    conn = koneksi()
    cur = conn.cursor()
    cur.execute(
        """SELECT barang.nama_barang, kategori.nama_kategori, barang.stok, barang.batas_minimum
           FROM barang
           JOIN kategori ON barang.id_kategori = kategori.id_kategori
           ORDER BY barang.nama_barang""")
    data = cur.fetchall()
    conn.close()

    tabel = tabulate(data, headers=["Nama Barang", "Kategori", "Stok", "Batas Minimum"], tablefmt="fancy_grid")

    print("=== Laporan Stok ===")
    print(tabel)

    simpan_ke_file("laporan_stok.txt", "LAPORAN STOK", tabel)
    input("Tekan Enter untuk melanjutkan...")

def laporan_transaksi():
    bersihkan_layar()

    conn = koneksi()
    cur = conn.cursor()
    cur.execute(
        """SELECT transaksi.tanggal, transaksi.jenis_transaksi, barang.nama_barang,
                  detail_transaksi.jumlah, detail_transaksi.harga_satuan
           FROM transaksi
           JOIN detail_transaksi ON transaksi.id_transaksi = detail_transaksi.id_transaksi
           JOIN barang ON detail_transaksi.id_barang = barang.id_barang
           ORDER BY transaksi.tanggal""")
    data = cur.fetchall()
    conn.close()

    tabel = tabulate(data, headers=["Tanggal", "Jenis Transaksi", "Nama Barang", "Jumlah", "Harga Satuan"], tablefmt="fancy_grid")

    print("=== Laporan Transaksi ===")
    print(tabel)

    simpan_ke_file("laporan_transaksi.txt", "LAPORAN TRANSAKSI", tabel)
    input("Tekan Enter untuk melanjutkan...")

def laporan_pemakaian():
    bersihkan_layar()
    print("=== Laporan Pemakaian ===")
    print("1. Per Petani")
    print("2. Per Bulan")
    print("3. Per Musim Tanam")
    pilihan = input("Pilih filter (1/2/3): ")

    dasar = """SELECT users.nama, barang.nama_barang, detail_transaksi.jumlah, transaksi.tanggal
               FROM transaksi
               JOIN detail_transaksi ON transaksi.id_transaksi = detail_transaksi.id_transaksi
               JOIN barang ON detail_transaksi.id_barang = barang.id_barang
               JOIN permintaan ON transaksi.id_permintaan = permintaan.id_permintaan
               JOIN users ON permintaan.id_users = users.id_users
               WHERE transaksi.jenis_transaksi = 'keluar' """

    conn = koneksi()
    cur = conn.cursor()

    if pilihan == "1":
        nama = input("Nama petani: ")
        cur.execute(dasar + "AND users.nama = %s ORDER BY transaksi.tanggal", (nama,))
    elif pilihan == "2":
        bulan = input("Bulan (1-12): ")
        tahun = input("Tahun: ")
        if bulan.isdigit() == False or tahun.isdigit() == False:
            print("Bulan dan tahun harus berupa angka!")
            conn.close()
            input("Tekan Enter untuk melanjutkan...")
            return
        cur.execute(
            dasar + """AND EXTRACT(MONTH FROM transaksi.tanggal) = %s
                       AND EXTRACT(YEAR FROM transaksi.tanggal) = %s
                       ORDER BY transaksi.tanggal""",
            (int(bulan), int(tahun)))
    elif pilihan == "3":
        print("1. Musim Hujan (Oktober - Maret)")
        print("2. Musim Kemarau (April - September)")
        musim = input("Pilih musim (1/2): ")
        if musim == "1":
            cur.execute(dasar + "AND EXTRACT(MONTH FROM transaksi.tanggal) IN (10, 11, 12, 1, 2, 3) ORDER BY transaksi.tanggal")
        elif musim == "2":
            cur.execute(dasar + "AND EXTRACT(MONTH FROM transaksi.tanggal) IN (4, 5, 6, 7, 8, 9) ORDER BY transaksi.tanggal")
        else:
            print("Pilihan musim tidak valid!")
            conn.close()
            input("Tekan Enter untuk melanjutkan...")
            return
    else:
        print("Pilihan tidak valid!")
        conn.close()
        input("Tekan Enter untuk melanjutkan...")
        return

    data = cur.fetchall()
    conn.close()

    if len(data) == 0:
        print("Tidak ada data pemakaian.")
        input("Tekan Enter untuk melanjutkan...")
        return

    tabel = tabulate(data, headers=["Nama Petani", "Nama Barang", "Jumlah", "Tanggal"], tablefmt="fancy_grid")

    print(tabel)

    simpan_ke_file("laporan_pemakaian.txt", "LAPORAN PEMAKAIAN", tabel)
    input("Tekan Enter untuk melanjutkan...")