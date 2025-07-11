from student_manager import ManajemenMahasiswa
from utils import input_angka, input_pilihan

def tampilkan_menu():
    """Menampilkan menu utama"""
    print("\nSistem Manajemen Nilai dan Kehadiran Mahasiswa")
    print("1. Tambah Mahasiswa")
    print("2. Perbarui Nilai")
    print("3. Perbarui Kehadiran")
    print("4. Hapus Mahasiswa")
    print("5. Lihat Data Mahasiswa")
    print("6. Tampilkan Semua Mahasiswa")
    print("7. Buat Laporan")
    print("8. Batalkan Aksi Terakhir")
    print("0. Keluar")

def input_nim():
    return input("Masukkan NIM: ").strip()

def input_nama():
    return input("Masukkan Nama: ").strip()

def input_nilai():
    return input_angka("Masukkan Nilai (0-100): ", 0, 100)

def input_kehadiran():
    return int(input_angka("Masukkan Persentase Kehadiran (0-100): ", 0, 100))

def main():
    manajer = ManajemenMahasiswa()
    
    while True:
        tampilkan_menu()
        pilihan = input_pilihan("Masukkan pilihan Anda (0-8): ", list(map(str, range(9))))
        
        if pilihan == '0':
            print("Keluar dari sistem...")
            break
        elif pilihan == '1':
            nim = input_nim()
            nama = input_nama()
            nilai = input_nilai()
            kehadiran = input_kehadiran()
            manajer.tambah_mahasiswa(nim, nama, nilai, kehadiran)
        elif pilihan == '2':
            nim = input_nim()
            nilai = input_nilai()
            manajer.perbarui_nilai(nim, nilai)
        elif pilihan == '3':
            nim = input_nim()
            kehadiran = input_kehadiran()
            manajer.perbarui_kehadiran(nim, kehadiran)
        elif pilihan == '4':
            nim = input_nim()
            manajer.hapus_mahasiswa(nim)
        elif pilihan == '5':
            nim = input_nim()
            manajer.tampilkan_mahasiswa(nim)
        elif pilihan == '6':
            manajer.daftar_mahasiswa()
        elif pilihan == '7':
            manajer.buat_laporan()
        elif pilihan == '8':
            manajer.batalkan_aksi_terakhir()

if __name__ == "__main__":
    main()
