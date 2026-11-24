from datetime import datetime
from app.auth import bersihkan_layar
from app.db import koneksi
from tabulate import tabulate

def menu_petugas(user):
    while True:
        bersihkan_layar()
        print("===== MENU PETUGAS GUDANG =====")
        print("Login sebagai:", user[1])
        print("1. Kelola Data Barang")
        print("2. Catat Barang Masuk")
        print("3. Catat Barang Keluar")
        print("0. Logout")
        pilihan = input("Pilih menu: ")
        if pilihan == "1":
            kelola_barang()
        elif pilihan == "2":
            barang_masuk(user)
        elif pilihan == "3":
            barang_keluar(user)
        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak ada.")
            input("Tekan Enter untuk melanjutkan...")

def isi_data(pertanyaan):
    """Tanya satu isian. Mengembalikan None kalau user mengetik 0."""
    jawaban = input(pertanyaan).strip()
    if jawaban == "0":
        return None
    return jawaban

def ke_angka(teks):
    """Ubah teks ke angka (boleh desimal). Mengembalikan None kalau tidak valid."""
    try:
        nilai = float(teks)
    except ValueError:
        return None
    if nilai < 0:
        return None
    return nilai

def ambil_satuan():
    """Ambil daftar satuan langsung dari enum jenis_satuan di database."""
    conn = koneksi()
    cur = conn.cursor()
    cur.execute("SELECT unnest(enum_range(NULL::jenis_satuan))::text")
    data = cur.fetchall()
    conn.close()
    return [baris[0] for baris in data]

def ambil_barang():
    conn = koneksi()
    cur = conn.cursor()
    cur.execute(
        """SELECT barang.id_barang, barang.nama_barang, kategori.nama_kategori,
                  barang.satuan, barang.harga, barang.stok, barang.batas_minimum,
                  pemasok.nama_pemasok
           FROM barang
           LEFT JOIN kategori ON barang.id_kategori = kategori.id_kategori
           LEFT JOIN pemasok ON barang.id_pemasok = pemasok.id_pemasok
           ORDER BY barang.id_barang""")
    data = cur.fetchall()
    conn.close()
    return data
    
def tampilkan_barang(data):
    print(tabulate(
        data,
        headers=["ID", "Nama Barang", "Kategori", "Satuan", "Harga", "Stok", "Batas Min", "Pemasok"],
        tablefmt="fancy_grid"))
def ambil_ringkas():
    conn = koneksi()
    cur = conn.cursor()
    cur.execute("SELECT id_barang, nama_barang, satuan, stok, harga FROM barang ORDER BY id_barang")
    data = cur.fetchall()
    conn.close()
    return data

def cari_baris(data, id_teks):
    """Cari baris yang kolom pertamanya sama dengan id yang diketik."""
    for baris in data:
        if str(baris[0]) == id_teks:
            return baris
    return None

def kelola_barang():
    while True:
        bersihkan_layar()
        print("===== KELOLA DATA BARANG =====")
        print("1. Lihat Semua Barang")
        print("2. Tambah Barang")
        print("3. Ubah Barang")
        print("4. Hapus Barang")
        print("5. Lihat Stok Menipis")
        print("0. Kembali")

        pilihan = input("Pilih menu: ")
        if pilihan == "1":
            lihat_barang()
        elif pilihan == "2":
            tambah_barang()
        elif pilihan == "3":
            ubah_barang()
        elif pilihan == "4":
            hapus_barang()
        elif pilihan == "5":
            stok_menipis()
        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak ada.")
            input("Tekan Enter untuk melanjutkan...")

def lihat_barang():
    bersihkan_layar()
    print("=== Daftar Barang ===")
    data = ambil_barang()
    if len(data) == 0:
        print("Belum ada data barang.")
    else:
        tampilkan_barang(data)
    input("Tekan Enter untuk kembali ke menu...")
def stok_menipis():
    bersihkan_layar()
    conn = koneksi()
    cur = conn.cursor()
    cur.execute(
        """SELECT nama_barang, satuan, stok, batas_minimum
           FROM barang
           WHERE stok < batas_minimum
           ORDER BY nama_barang""")
    data = cur.fetchall()
    conn.close()

    print("=== Barang dengan Stok di Bawah Batas Minimum ===")
    if len(data) == 0:
        print("Tidak ada barang yang stoknya menipis.")
    else:
        print(tabulate(data, headers=["Nama Barang", "Satuan", "Stok", "Batas Min"], tablefmt="fancy_grid"))
    input("Tekan Enter untuk kembali ke menu...")

def tambah_barang():
    bersihkan_layar()

    conn = koneksi()
    cur = conn.cursor()
    cur.execute("SELECT id_kategori, nama_kategori FROM kategori ORDER BY id_kategori")
    kategori = cur.fetchall()
    cur.execute("SELECT id_pemasok, nama_pemasok FROM pemasok ORDER BY id_pemasok")
    pemasok = cur.fetchall()
    conn.close()
    daftar_satuan = ambil_satuan()

    print("=== Tambah Barang ===")
    print("(Ketik 0 pada isian mana pun untuk kembali ke menu)")

    nama = isi_data("Nama barang: ")
    if nama is None:
        return

    print(tabulate(kategori, headers=["ID", "Kategori"], tablefmt="fancy_grid"))
    id_kategori = isi_data("ID kategori: ")
    if id_kategori is None:
        return

    print("Satuan yang tersedia:", ", ".join(daftar_satuan))
    satuan = isi_data("Satuan: ")
    if satuan is None:
        return
    satuan = satuan.lower()
    harga = isi_data("Harga per satuan: ")
    if harga is None:
        return
    stok = isi_data("Stok awal: ")
    if stok is None:
        return
    batas = isi_data("Batas minimum stok: ")
    if batas is None:
        return
    print(tabulate(pemasok, headers=["ID", "Pemasok"], tablefmt="fancy_grid"))
    id_pemasok = isi_data("ID pemasok (Enter jika tidak ada): ")
    if id_pemasok is None:
        return

    if nama == "" or id_kategori == "" or satuan == "" or harga == "" or stok == "" or batas == "":
        print("Semua data wajib diisi (kecuali pemasok)!")
        input("Tekan Enter untuk kembali ke menu...")
        return

    if cari_baris(kategori, id_kategori) is None:
        print("Kategori tidak ditemukan!")
        input("Tekan Enter untuk kembali ke menu...")
        return

    if satuan not in daftar_satuan:
        print("Satuan tidak valid!")
        input("Tekan Enter untuk kembali ke menu...")
        return

    harga_angka = ke_angka(harga)
    if harga_angka is None or harga_angka <= 0:
        print("Harga harus berupa angka lebih dari 0!")
        input("Tekan Enter untuk kembali ke menu...")
        return

    if stok.isdigit() == False or batas.isdigit() == False:
        print("Stok dan batas minimum harus berupa angka bulat!")
        input("Tekan Enter untuk kembali ke menu...")
        return

    if id_pemasok == "":
        id_pemasok = None
    elif cari_baris(pemasok, id_pemasok) is None:
        print("Pemasok tidak ditemukan!")
        input("Tekan Enter untuk kembali ke menu...")
        return

    conn = koneksi()
    cur = conn.cursor()
    try:
        cur.execute(
            """INSERT INTO barang (nama_barang, harga, satuan, stok, batas_minimum, id_kategori, id_pemasok)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (nama, harga_angka, satuan, int(stok), int(batas), id_kategori, id_pemasok))
        conn.commit()
        print("Barang berhasil ditambahkan.")
    except Exception as e:
        conn.rollback()
        print("Gagal menambah barang:", e)
    finally:
        conn.close()

    input("Tekan Enter untuk kembali ke menu...")


def ubah_barang():
    bersihkan_layar()

    data = ambil_barang()
    tampilkan_barang(data)

    print("=== Ubah Barang ===")
    print("(Ketik 0 untuk kembali ke menu, tekan Enter untuk tidak mengubah isian)")

    id_barang = isi_data("Masukkan ID barang: ")
    if id_barang is None:
        return

    barang = cari_baris(data, id_barang)
    if barang is None:
        print("Barang tidak ditemukan!")
        input("Tekan Enter untuk kembali ke menu...")
        return

    daftar_satuan = ambil_satuan()
    print("Satuan yang tersedia:", ", ".join(daftar_satuan))

    nama = isi_data("Nama barang [" + str(barang[1]) + "]: ")
    if nama is None:
        return
    satuan = isi_data("Satuan [" + str(barang[3]) + "]: ")
    if satuan is None:
        return
    harga = isi_data("Harga [" + str(barang[4]) + "]: ")
    if harga is None:
        return
    batas = isi_data("Batas minimum [" + str(barang[6]) + "]: ")
    if batas is None:
        return

    if nama == "":
        nama = barang[1]

    if satuan == "":
        satuan = str(barang[3])
    satuan = satuan.lower()
    if satuan not in daftar_satuan:
        print("Satuan tidak valid!")
        input("Tekan Enter untuk kembali ke menu...")
        return

    if harga == "":
        harga_angka = barang[4]
    else:
        harga_angka = ke_angka(harga)
        if harga_angka is None or harga_angka <= 0:
            print("Harga harus berupa angka lebih dari 0!")
            input("Tekan Enter untuk kembali ke menu...")
            return

    if batas == "":
        batas_angka = barang[6]
    else:
        if batas.isdigit() == False:
            print("Batas minimum harus berupa angka bulat!")
            input("Tekan Enter untuk kembali ke menu...")
            return
        batas_angka = int(batas)

    conn = koneksi()
    cur = conn.cursor()
    try:
        cur.execute(
            """UPDATE barang
               SET nama_barang = %s, satuan = %s, harga = %s, batas_minimum = %s
               WHERE id_barang = %s""",
            (nama, satuan, harga_angka, batas_angka, id_barang))
        conn.commit()
        print("Data barang berhasil diubah.")
    except Exception as e:
        conn.rollback()
        print("Gagal mengubah barang:", e)
    finally:
        conn.close()

    input("Tekan Enter untuk kembali ke menu...")


def hapus_barang():
    bersihkan_layar()

    data = ambil_barang()
    tampilkan_barang(data)
    print("=== Hapus Barang ===")
    print("(Ketik 0 untuk kembali ke menu)")
    id_barang = isi_data("Masukkan ID barang: ")
    if id_barang is None:
        return
    barang = cari_baris(data, id_barang)
    if barang is None:
        print("Barang tidak ditemukan!")
        input("Tekan Enter untuk kembali ke menu...")
        return
    yakin = input("Yakin menghapus " + str(barang[1]) + "? (y/n): ")
    if yakin != "y":
        print("Dibatalkan.")
        input("Tekan Enter untuk kembali ke menu...")
        return

    conn = koneksi()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM barang WHERE id_barang = %s", (id_barang,))
        conn.commit()
        print("Barang berhasil dihapus.")
    except Exception as e:
        conn.rollback()
        # kode 23503 = barang masih dipakai di tabel lain (permintaan / detail_transaksi)
        if getattr(e, "pgcode", None) == "23503":
            print("Barang tidak bisa dihapus karena sudah dipakai di permintaan atau transaksi.")
        else:
            print("Gagal menghapus barang:", e)
    finally:
        conn.close()

    input("Tekan Enter untuk kembali ke menu...")

def barang_masuk(user):
    bersihkan_layar()

    data = ambil_ringkas()
    print(tabulate([[b[0], b[1], b[2], b[3]] for b in data],
                   headers=["ID", "Nama Barang", "Satuan", "Stok"], tablefmt="fancy_grid"))

    print("=== Catat Barang Masuk ===")
    print("(Ketik 0 pada isian mana pun untuk kembali ke menu)")

    id_barang = isi_data("Masukkan ID barang: ")
    if id_barang is None:
        return

    barang = cari_baris(data, id_barang)
    if barang is None:
        print("Barang tidak ditemukan!")
        input("Tekan Enter untuk kembali ke menu...")
        return

    jumlah = isi_data("Jumlah masuk: ")
    if jumlah is None:
        return
    if jumlah.isdigit() == False or int(jumlah) <= 0:
        print("Jumlah harus berupa angka lebih dari 0!")
        input("Tekan Enter untuk kembali ke menu...")
        return
    harga = isi_data("Harga satuan [" + str(barang[4]) + "] (Enter = pakai harga barang): ")
    if harga is None:
        return
    if harga == "":
        harga_angka = barang[4]
    else:
        harga_angka = ke_angka(harga)
        if harga_angka is None or harga_angka <= 0:
            print("Harga harus berupa angka lebih dari 0!")
            input("Tekan Enter untuk kembali ke menu...")
            return
    kadaluwarsa = isi_data("Tanggal kadaluwarsa (YYYY-MM-DD, Enter jika tidak ada): ")
    if kadaluwarsa is None:
        return
    if kadaluwarsa == "":
        kadaluwarsa = None
    else:
        try:
            datetime.strptime(kadaluwarsa, "%Y-%m-%d")
        except ValueError:
            print("Format tanggal salah! Contoh: 2027-12-31")
            input("Tekan Enter untuk kembali ke menu...")
            return

    yakin = input("Simpan barang masuk? (y/n, 0 untuk kembali): ")
    if yakin == "0":
        return

    if yakin == "y":
        conn = koneksi()
        cur = conn.cursor()
        try:
            cur.execute(
                """INSERT INTO transaksi (jenis_transaksi, tanggal, id_users)
                   VALUES ('masuk', CURRENT_DATE, %s)
                   RETURNING id_transaksi""",
                (user[0],))
            id_transaksi = cur.fetchone()[0]

            cur.execute(
                """INSERT INTO detail_transaksi (id_transaksi, id_barang, jumlah, harga_satuan, tgl_kadaluwarsa)
                   VALUES (%s, %s, %s, %s, %s)""",
                (id_transaksi, id_barang, int(jumlah), harga_angka, kadaluwarsa))

            cur.execute(
                "UPDATE barang SET stok = stok + %s WHERE id_barang = %s",
                (int(jumlah), id_barang))
            conn.commit()
            print("Barang masuk berhasil dicatat. Stok bertambah", jumlah)
        except Exception as e:
            conn.rollback()
            print("Gagal mencatat barang masuk:", e)
        finally:
            conn.close()
    else:
        print("Dibatalkan.")

    input("Tekan Enter untuk kembali ke menu...")

def ambil_permintaan_siap():
    """Permintaan yang sudah disetujui dan belum dicatat transaksinya."""
    conn = koneksi()
    cur = conn.cursor()
    cur.execute(
        """SELECT permintaan.id_permintaan, users.nama, barang.nama_barang,
                  permintaan.jumlah, permintaan.keperluan, barang.stok,
                  permintaan.id_barang, barang.harga
           FROM permintaan
           JOIN users ON permintaan.id_users = users.id_users
           JOIN barang ON permintaan.id_barang = barang.id_barang
           WHERE permintaan.status = 'disetujui'
           AND permintaan.id_permintaan NOT IN
               (SELECT id_permintaan FROM transaksi WHERE id_permintaan IS NOT NULL)
           ORDER BY permintaan.id_permintaan""")
    data = cur.fetchall()
    conn.close()
    return data


def barang_keluar(user):
    bersihkan_layar()

    data = ambil_permintaan_siap()

    if len(data) == 0:
        print("Tidak ada permintaan disetujui yang menunggu diserahkan.")
        input("Tekan Enter untuk kembali ke menu...")
        return

    tampil = []
    for baris in data:
        tampil.append([baris[0], baris[1], baris[2], baris[3], baris[4], baris[5]])
    print(tabulate(tampil, headers=["ID", "Petani", "Barang", "Jumlah", "Keperluan", "Stok"], tablefmt="fancy_grid"))
    print("=== Catat Barang Keluar ===")
    print("(Ketik 0 untuk kembali ke menu)")
    id_permintaan = isi_data("Masukkan ID permintaan: ")
    if id_permintaan is None:
        return
    permintaan = cari_baris(data, id_permintaan)
    if permintaan is None:
        print("Permintaan tidak ditemukan!")
        input("Tekan Enter untuk kembali ke menu...")
        return
    jumlah = permintaan[3]
    stok = permintaan[5]
    id_barang = permintaan[6]
    harga = permintaan[7]
    if stok < jumlah:
        print("Stok barang sedang tidak mencukupi!")
        input("Tekan Enter untuk kembali ke menu...")
        return
    yakin = input("Konfirmasi penyerahan barang kepada " + str(permintaan[1]) + "? (y/n, 0 untuk kembali): ")
    if yakin == "0":
        return
    if yakin == "y":
        conn = koneksi()
        cur = conn.cursor()
        try:
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
                "UPDATE barang SET stok = stok - %s WHERE id_barang = %s AND stok >= %s",
                (jumlah, id_barang, jumlah))
            if cur.rowcount == 0:
                raise Exception("Stok tidak mencukupi")
            conn.commit()
            print("Barang keluar berhasil dicatat.")
        except Exception as e:
            conn.rollback()
            print("Gagal mencatat barang keluar:", e)
        finally:
            conn.close()
    else:
        print("Dibatalkan.")
    input("Tekan Enter untuk kembali ke menu...")
