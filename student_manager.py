import csv
import os
from utils import get_timestamp

class ManajemenMahasiswa:
    def __init__(self, nama_file="data_mahasiswa.csv"):
        self.mahasiswa = {}  
        self.action_stack = [] 
        self.nama_file = nama_file
        self.muat_data()

    def muat_data(self):
        if os.path.exists(self.nama_file):
            with open(self.nama_file, mode='r', encoding='utf-8') as file:
                pembaca = csv.DictReader(file)
                for baris in pembaca:
                    nim = baris['nim']
                    self.mahasiswa[nim] = {
                        'nama': baris['nama'],
                        'nilai': float(baris['nilai']),
                        'kehadiran': int(baris['kehadiran']),
                        'terakhir_diperbarui': baris['terakhir_diperbarui']
                    }

    def simpan_data(self):
        with open(self.nama_file, mode='w', encoding='utf-8', newline='') as file:
            fieldnames = ['nim', 'nama', 'nilai', 'kehadiran', 'terakhir_diperbarui']
            penulis = csv.DictWriter(file, fieldnames=fieldnames)
            penulis.writeheader()
            
            for nim, data in self.mahasiswa.items():
                penulis.writerow({
                    'nim': nim,
                    'nama': data['nama'],
                    'nilai': data['nilai'],
                    'kehadiran': data['kehadiran'],
                    'terakhir_diperbarui': data['terakhir_diperbarui']
                })

    def tambah_mahasiswa(self, nim, nama, nilai=0.0, kehadiran=0):
        if nim in self.mahasiswa:
            print(f"Mahasiswa dengan NIM {nim} sudah ada!")
            return False
        
        self.mahasiswa[nim] = {
            'nama': nama,
            'nilai': nilai,
            'kehadiran': kehadiran,
            'terakhir_diperbarui': get_timestamp()
        }
        self.action_stack.append(('tambah', nim))  
        self.simpan_data()
        return True

    def perbarui_nilai(self, nim, nilai):
        if nim not in self.mahasiswa:
            print(f"Mahasiswa dengan NIM {nim} tidak ditemukan!")
            return False
        
        self.action_stack.append(('perbarui_nilai', nim, self.mahasiswa[nim]['nilai']))
        self.mahasiswa[nim]['nilai'] = nilai
        self.mahasiswa[nim]['terakhir_diperbarui'] = get_timestamp()
        self.simpan_data()
        return True

    def perbarui_kehadiran(self, nim, kehadiran):
        if nim not in self.mahasiswa:
            print(f"Mahasiswa dengan NIM {nim} tidak ditemukan!")
            return False
        
        self.action_stack.append(('perbarui_kehadiran', nim, self.mahasiswa[nim]['kehadiran']))
        self.mahasiswa[nim]['kehadiran'] = kehadiran
        self.mahasiswa[nim]['terakhir_diperbarui'] = get_timestamp()
        self.simpan_data()
        return True

    def hapus_mahasiswa(self, nim):
        if nim not in self.mahasiswa:
            print(f"Mahasiswa dengan NIM {nim} tidak ditemukan!")
            return False
        
        self.action_stack.append(('hapus', nim, self.mahasiswa[nim]))
        del self.mahasiswa[nim]
        self.simpan_data()
        print ("data mahasiswa berhasil dihapus")
        return True

    def batalkan_aksi_terakhir(self):
        if not self.action_stack:
            print("Tidak ada aksi yang bisa dibatalkan!")
            return False
        
        aksi = self.action_stack.pop()
        
        if aksi[0] == 'tambah':
            del self.mahasiswa[aksi[1]]
            print ("tambah mahasiswa telah dihapus")
        elif aksi[0] == 'hapus':
            nim, data_mhs = aksi[1], aksi[2]
            self.mahasiswa[nim] = data_mhs
            print ("hapus data telah dibatalkan")
        elif aksi[0] == 'perbarui_nilai':
            nim, nilai_sebelumnya = aksi[1], aksi[2]
            self.mahasiswa[nim]['nilai'] = nilai_sebelumnya
            self.mahasiswa[nim]['terakhir_diperbarui'] = get_timestamp()
        elif aksi[0] == 'perbarui_kehadiran':
            nim, kehadiran_sebelumnya = aksi[1], aksi[2]
            self.mahasiswa[nim]['kehadiran'] = kehadiran_sebelumnya
            self.mahasiswa[nim]['terakhir_diperbarui'] = get_timestamp()
        
        self.simpan_data()
        return True
    
    
    def tampilkan_mahasiswa(self, nim):
        if nim not in self.mahasiswa:
            print(f"Mahasiswa dengan NIM {nim} tidak ditemukan!")
            return False
        
        mhs = self.mahasiswa[nim]
        print("\nInformasi Mahasiswa:")
        print(f"NIM: {nim}")
        print(f"Nama: {mhs['nama']}")
        print(f"Nilai: {mhs['nilai']}")
        print(f"Kehadiran: {mhs['kehadiran']}%")
        print(f"Terakhir Diperbarui: {mhs['terakhir_diperbarui']}")
        return True

    def daftar_mahasiswa(self):
        if not self.mahasiswa:
            print("Tidak ada data mahasiswa!")
            return False
        
        print("\nDaftar Mahasiswa:")
        print("{:<12} {:<20} {:<10} {:<15} {:<20}".format(
            "NIM", "Nama", "Nilai", "Kehadiran %", "Terakhir Diperbarui"
        ))
        print("-" * 77)
        
        for nim, data in self.mahasiswa.items():
            print("{:<12} {:<20} {:<10.2f} {:<15} {:<20}".format(
                nim,
                data['nama'],
                data['nilai'],
                str(data['kehadiran']) + '%',
                data['terakhir_diperbarui']
            ))
        return True

    def buat_laporan(self):
        """Membuat laporan ringkasan"""
        if not self.mahasiswa:
            print("Tidak ada data mahasiswa!")
            return False
        
        total_mhs = len(self.mahasiswa)
        rata_nilai = sum(mhs['nilai'] for mhs in self.mahasiswa.values()) / total_mhs
        rata_kehadiran = sum(mhs['kehadiran'] for mhs in self.mahasiswa.values()) / total_mhs
        
        print("\nLaporan Sistem Manajemen Mahasiswa:")
        print(f"Total Mahasiswa: {total_mhs}")
        print(f"Rata-rata Nilai: {rata_nilai:.2f}")
        print(f"Rata-rata Kehadiran: {rata_kehadiran:.2f}%")
        
        # Kategorisasi nilai
        kategori_nilai = {
            'A (90-100)': 0, 
            'B (80-89)': 0, 
            'C (70-79)': 0, 
            'D (60-69)': 0, 
            'E (0-59)': 0
        }
        
        for mhs in self.mahasiswa.values():
            nilai = mhs['nilai']
            if nilai >= 90: kategori_nilai['A (90-100)'] += 1
            elif nilai >= 80: kategori_nilai['B (80-89)'] += 1
            elif nilai >= 70: kategori_nilai['C (70-79)'] += 1
            elif nilai >= 60: kategori_nilai['D (60-69)'] += 1
            else: kategori_nilai['E (0-59)'] += 1
        
        print("\nDistribusi Nilai:")
        for kategori, jumlah in kategori_nilai.items():
            print(f"{kategori}: {jumlah} mahasiswa")
        
        print("\nRingkasan Kehadiran:")
        print(f"{sum(1 for m in self.mahasiswa.values() if m['kehadiran'] >= 80)} mahasiswa dengan kehadiran 80%+")
        print(f"{sum(1 for m in self.mahasiswa.values() if m['kehadiran'] < 80)} mahasiswa dengan kehadiran di bawah 80%")
        
        return True
