from app.auth import bersihkan_layar


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
        if pilihan == "0":
            break
        else:
            print("Fitur ini belum dibuat.")
            input("Tekan Enter untuk melanjutkan...")