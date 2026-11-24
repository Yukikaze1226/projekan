from app.auth import registrasi, login, bersihkan_layar
from app.admin import menu_admin
from app.petugas import menu_petugas
from app.petani import menu_petani

def tampilkan_logo():
    # Garis atas
    print("=" * 71)

    print(r" ___   _   _  __     __  _____   _   _   _____      _      _   _   ___ ")
    print(r"|_ _| | \ | | \ \   / / | ____| | \ | | |_   _|    / \    | \ | | |_ _|")
    print(r" | |  |  \| |  \ \ / /  |  _|   |  \| |   | |     / _ \   |  \| |  | | ")
    print(r" | |  | |\  |   \ V /   | |___  | |\  |   | |    / ___ \  | |\  |  | | ")
    print(r"|___| |_| \_|    \_/    |_____| |_| \_|   |_|   /_/   \_\ |_| \_| |___|")
    print("=" * 71)
    print("Aplikasi Inventarisasi Pupuk dan Pestisida".center(71))
    print("=" * 71)

def main():
    while True:
        bersihkan_layar()
        tampilkan_logo()
        print("1. Login")
        print("2. Registrasi (Petani)")
        print("0. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            user = login()
            if user is not None:
                if user[2] == "admin":
                    menu_admin(user)
                elif user[2] == "petugas":
                    menu_petugas(user)
                else:
                    menu_petani(user)
        elif pilihan == "2":
            registrasi()
        elif pilihan == "0":
            print("Terima kasih!")
            break
        else:
            print("Pilihan tidak valid!")
            input("Tekan Enter untuk melanjutkan...")


main()
