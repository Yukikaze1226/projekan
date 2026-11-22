from app.auth import bersihkan_layar


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
        if pilihan == "0":
            break
        else:
            print("Fitur ini belum dibuat.")
            input("Tekan Enter untuk melanjutkan...")