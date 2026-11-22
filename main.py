from app.auth import registrasi, login, bersihkan_layar
from app.admin import menu_admin
from app.petugas import menu_petugas
from app.petani import menu_petani


def main():
    while True:
        bersihkan_layar()
        print("===== APLIKASI INVENTARISASI PUPUK DAN PESTISIDA =====")
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