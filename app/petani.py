from app.auth import bersihkan_layar
from app.db import koneksi
from tabulate import tabulate

def menu_petani(user):
    while True:
        bersihkan_layar()
        print("===== MENU PETANI =====")
        print("Login sebagai:", user[1])
        print("1. Lihat Stok Barang")
        print("2. Ajukan Permintaan")
        print("3. Lihat Status Permintaan")
        print("4. Melakukan Transaksi")
        print("5. Lihat Riwayat Pengambilan")
        print("0. Logout")

         pilihan = input("Pilih menu: ")
        if pilihan == "1":
            lihat_stok()
        elif pilihan == "2":
            ajukan_permintaan(user)
        elif pilihan == "3":
            lihat_status_permintaan(user)
        elif pilihan == "4":
            melakukan_transaksi(user)
        elif pilihan == "5":
            lihat_riwayat(user)
        elif pilihan == "0":
            break
        else:
            print("Fitur ini belum dibuat.")
            input("Tekan Enter untuk melanjutkan...")
def ambil_barang():
    conn = koneksi()
    cur = conn.cursor()
    cur.execute("SELECT id_barang, nama_barang, satuan, stok FROM barang ORDER BY id_barang")
    data = cur.fetchall()
    conn.close()
    return data


def lihat_stok():
    bersihkan_layar()

    conn = koneksi()
    cur = conn.cursor()
    cur.execute(
        """SELECT barang.nama_barang, kategori.nama_kategori, barang.satuan, barang.stok
           FROM barang
           JOIN kategori ON barang.id_kategori = kategori.id_kategori
           ORDER BY barang.nama_barang""")
    data = cur.fetchall()
    conn.close()

    print("=== Lihat Stok Barang ===")
    print(tabulate(data, headers=["Nama Barang", "Kategori", "Satuan", "Stok"], tablefmt="fancy_grid"))
    input("Tekan Enter untuk melanjutkan...")


def ajukan_permintaan(user):
    bersihkan_layar()

    data = ambil_barang()
    print(tabulate(data, headers=["ID", "Nama Barang", "Satuan", "Stok"], tablefmt="fancy_grid"))

    print("=== Ajukan Permintaan ===")
    id_barang = input("Masukkan ID barang: ")
    jumlah = input("Jumlah: ")
    keperluan = input("Keperluan: ")

    if id_barang == "" or jumlah == "" or keperluan == "":
        print("Semua data wajib diisi!")
        input("Tekan Enter untuk melanjutkan...")
        return

    if jumlah.isdigit() == False or int(jumlah) <= 0:
        print("Jumlah harus berupa angka lebih dari 0!")
        input("Tekan Enter untuk melanjutkan...")
        return

    ditemukan = False
    for baris in data:
        if str(baris[0]) == id_barang:
            ditemukan = True

    if ditemukan == False:
        print("Barang tidak ditemukan!")
        input("Tekan Enter untuk melanjutkan...")
        return

    conn = koneksi()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO permintaan (id_users, id_barang, jumlah, keperluan, tanggal, status)
           VALUES (%s, %s, %s, %s, CURRENT_DATE, 'menunggu')""",
        (user[0], id_barang, int(jumlah), keperluan))
    conn.commit()
    conn.close()

    print("Permintaan berhasil diajukan dengan status menunggu.")
    input("Tekan Enter untuk melanjutkan...")


def lihat_status_permintaan(user):
    bersihkan_layar()

    conn = koneksi()
    cur = conn.cursor()
    cur.execute(
        """SELECT permintaan.tanggal, barang.nama_barang, permintaan.jumlah,
                  permintaan.keperluan, permintaan.status
           FROM permintaan
           JOIN barang ON permintaan.id_barang = barang.id_barang
           WHERE permintaan.id_users = %s
           ORDER BY permintaan.tanggal DESC""",
        (user[0],))
    data = cur.fetchall()
    conn.close()

    print("=== Status Permintaan Saya ===")
    if len(data) == 0:
        print("Anda belum pernah mengajukan permintaan.")
    else:
        print(tabulate(data, headers=["Tanggal", "Nama Barang", "Jumlah", "Keperluan", "Status"], tablefmt="fancy_grid"))
    input("Tekan Enter untuk melanjutkan...")


def ambil_permintaan_disetujui(id_users):
    conn = koneksi()
    cur = conn.cursor()
    cur.execute(
        """SELECT permintaan.id_permintaan, barang.nama_barang, permintaan.jumlah,
                  permintaan.id_barang, barang.harga, barang.stok
           FROM permintaan
           JOIN barang ON permintaan.id_barang = barang.id_barang
           WHERE permintaan.id_users = %s
           AND permintaan.status = 'disetujui'
           AND permintaan.id_permintaan NOT IN
               (SELECT id_permintaan FROM transaksi WHERE id_permintaan IS NOT NULL)
           ORDER BY permintaan.id_permintaan""",
        (id_users,))
    data = cur.fetchall()
    conn.close()
    return data


def melakukan_transaksi(user):
    bersihkan_layar()

    data = ambil_permintaan_disetujui(user[0])

    if len(data) == 0:
        print("Tidak ada permintaan disetujui yang bisa diambil.")
        input("Tekan Enter untuk melanjutkan...")
        return

    tampil = []
    for baris in data:
        tampil.append([baris[0], baris[1], baris[2]])
    print(tabulate(tampil, headers=["ID", "Nama Barang", "Jumlah"], tablefmt="fancy_grid"))

    print("=== Melakukan Transaksi ===")
    id_permintaan = input("Masukkan ID permintaan: ")

    ditemukan = False
    id_barang = 0
    jumlah = 0
    harga = 0
    stok = 0
    for baris in data:
        if str(baris[0]) == id_permintaan:
            ditemukan = True
            jumlah = baris[2]
            id_barang = baris[3]
            harga = baris[4]
            stok = baris[5]

    if ditemukan == False:
        print("Permintaan tidak ditemukan!")
        input("Tekan Enter untuk melanjutkan...")
        return

    if stok < jumlah:
        print("Stok barang sedang tidak mencukupi!")
        input("Tekan Enter untuk melanjutkan...")
        return

    yakin = input("Konfirmasi pengambilan barang? (y/n): ")

    if yakin == "y":
        conn = koneksi()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO transaksi (jenis_transaksi, tanggal, id_users, id_permintaan)
               VALUES ('keluar', CURRENT_DATE, %s, %s)
               RETURNING id_transaksi""",
            (user[0], id_permintaan))
        id_transaksi = cur.fetchone()[0]

        cur.execute(
            """INSERT INTO detail_transaksi (id_transaksi, id_barang, jumlah, harga_satuan)
               VALUES (%s, %s, %s, %s)""",
            (id_transaksi, id_barang, jumlah, harga))

        cur.execute(
            "UPDATE barang SET stok = stok - %s WHERE id_barang = %s",
            (jumlah, id_barang))
        conn.commit()
        conn.close()
        print("Transaksi berhasil dicatat.")
    else:
        print("Dibatalkan.")

    input("Tekan Enter untuk melanjutkan...")

def lihat_riwayat(user):
    bersihkan_layar()

    conn = koneksi()
    cur = conn.cursor()
    cur.execute(
        """SELECT transaksi.tanggal, barang.nama_barang, detail_transaksi.jumlah,
                  detail_transaksi.jumlah * detail_transaksi.harga_satuan
           FROM transaksi
           JOIN detail_transaksi ON transaksi.id_transaksi = detail_transaksi.id_transaksi
           JOIN barang ON detail_transaksi.id_barang = barang.id_barang
           JOIN permintaan ON transaksi.id_permintaan = permintaan.id_permintaan
           WHERE permintaan.id_users = %s AND transaksi.jenis_transaksi = 'keluar'
           ORDER BY transaksi.tanggal DESC""",
        (user[0],))
    data = cur.fetchall()
    conn.close()

    print("=== Riwayat Pengambilan ===")
    if len(data) == 0:
        print("Belum ada riwayat pengambilan.")
    else:
        print(tabulate(data, headers=["Tanggal", "Nama Barang", "Jumlah", "Harga Total"], tablefmt="fancy_grid"))
    input("Tekan Enter untuk melanjutkan...")

