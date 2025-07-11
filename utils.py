from datetime import datetime

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def input_angka(pesan, min_val=None, max_val=None):
    """Meminta input angka dengan validasi"""
    while True:
        try:
            angka = float(input(pesan))
            if (min_val is not None and angka < min_val) or (max_val is not None and angka > max_val):
                print(f"Masukkan angka antara {min_val} dan {max_val}!")
                continue
            return angka
        except ValueError:
            print("Harap masukkan angka yang valid!")

def input_pilihan(pertanyaan, pilihan_valid):
    """Meminta input pilihan dengan validasi"""
    while True:
        pilihan = input(pertanyaan).strip()
        if pilihan in pilihan_valid:
            return pilihan
        print(f"Pilihan tidak valid. Pilihan yang tersedia: {', '.join(pilihan_valid)}")



