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

        if pilihan == "0":
            break
        else:
            print("Fitur ini belum dibuat.")
            input("Tekan Enter untuk melanjutkan...")