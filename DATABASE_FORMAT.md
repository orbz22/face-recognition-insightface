# Format Database - Parent-Child-Class

Sistem sekarang menggunakan format database yang menyimpan informasi lengkap:
**Nama Orang Tua_Nama Anak_Kelas Anak**

## 📋 Format Label

### Format
```
NamaOrtu_NamaAnak_Kelas
```

### Contoh
```
Budi Santoso_Andi Santoso_3A
Siti Aminah_Dewi Lestari_5B
Ahmad Wijaya_Reza Ahmad_1C
```

## 📝 Proses Enrollment

### 1. Jalankan Program
```bash
python main.py
```

### 2. Pilih Menu 1 (Enroll)

### 3. Input Data
Program akan meminta 3 informasi:

```
Nama Orang Tua: Budi Santoso
Nama Anak: Andi Santoso  
Kelas Anak (contoh: 3A, 5B): 3A
```

### 4. Konfirmasi Data
```
[*] Data yang akan didaftarkan:
   Nama Orang Tua: Budi Santoso
   Nama Anak: Andi Santoso
   Kelas: 3A
   Label Database: Budi Santoso_Andi Santoso_3A

Apakah data sudah benar? (y/n): y
```

### 5. Capture Wajah
- Arahkan wajah orang tua ke kamera
- Tekan 'c' untuk capture (10x samples)
- Selesai!

## 🎯 Tampilan Recognition

Saat wajah terdeteksi, akan ditampilkan:

```
┌─────────────────────┐
│ Ortu: Budi Santoso  │
│ Anak: Andi Santoso  │
│ Kelas: 3A           │
│ sim=0.85            │
└─────────────────────┘
```

## 🔍 Melihat Database

### Opsi 1: Menggunakan view_database.py

```bash
python view_database.py
```

Menu:
```
1. Lihat Semua Data
2. Cari Berdasarkan Nama Anak
3. Cari Berdasarkan Kelas
4. Export ke CSV
5. Keluar
```

### Opsi 2: Manual

```python
import json

with open('face_db/labels.json', 'r') as f:
    labels = json.load(f)

for label in labels:
    parts = label.split('_')
    print(f"Ortu: {parts[0]}, Anak: {parts[1]}, Kelas: {parts[2]}")
```

## 📊 Contoh Output Database Viewer

```
================================================================================
  DATABASE WAJAH ORANG TUA - FACE RECOGNITION SYSTEM
================================================================================
Total Terdaftar: 3 orang
Total Embeddings: 3
================================================================================

No   Nama Orang Tua            Nama Anak                 Kelas     
--------------------------------------------------------------------------------
1    Budi Santoso              Andi Santoso              3A        
2    Siti Aminah               Dewi Lestari              5B        
3    Ahmad Wijaya              Reza Ahmad                1C        
================================================================================
```

## 🔎 Pencarian

### Cari Berdasarkan Nama Anak

```bash
python view_database.py
# Pilih 2
# Input: Andi

Hasil:
No   Nama Orang Tua            Nama Anak                 Kelas     
--------------------------------------------------------------------------------
1    Budi Santoso              Andi Santoso              3A        
```

### Cari Berdasarkan Kelas

```bash
python view_database.py
# Pilih 3
# Input: 3A

Hasil:
Ditemukan 2 orang tua di kelas 3A:

No   Nama Orang Tua            Nama Anak                 Kelas     
--------------------------------------------------------------------------------
1    Budi Santoso              Andi Santoso              3A        
5    Rina Putri                Sari Rina                 3A        
```

## 📤 Export ke CSV

```bash
python view_database.py
# Pilih 4

Output: database_export.csv
```

Format CSV:
```csv
No,Nama Orang Tua,Nama Anak,Kelas,Label Lengkap
1,Budi Santoso,Andi Santoso,3A,Budi Santoso_Andi Santoso_3A
2,Siti Aminah,Dewi Lestari,5B,Siti Aminah_Dewi Lestari_5B
```

## 💾 Struktur Database

### labels.json
```json
[
  "Budi Santoso_Andi Santoso_3A",
  "Siti Aminah_Dewi Lestari_5B",
  "Ahmad Wijaya_Reza Ahmad_1C"
]
```

### embeddings.npy
```
Array shape: (3, 512)
- Row 0: Embedding wajah Budi Santoso
- Row 1: Embedding wajah Siti Aminah
- Row 2: Embedding wajah Ahmad Wijaya
```

## 🔄 Migrasi dari Format Lama

Jika Anda punya database dengan format lama (hanya nama):

### Manual Update

```python
import json

# Load
with open('face_db/labels.json', 'r') as f:
    labels = json.load(f)

# Update format
new_labels = []
for label in labels:
    # Tambahkan info anak dan kelas
    # Contoh: "Budi" → "Budi_AnakBudi_1A"
    child_name = input(f"Nama anak dari {label}: ")
    class_name = input(f"Kelas anak: ")
    new_label = f"{label}_{child_name}_{class_name}"
    new_labels.append(new_label)

# Save
with open('face_db/labels.json', 'w') as f:
    json.dump(new_labels, f, indent=2)
```

## ⚠️ Catatan Penting

1. **Separator adalah Underscore (_)**
   - Jangan gunakan underscore di nama
   - Jika nama punya underscore, ganti dengan spasi atau strip

2. **Format Kelas**
   - Konsisten: 3A, 5B, 1C (angka + huruf)
   - Atau: III-A, V-B, I-C

3. **Nama Lengkap**
   - Gunakan nama lengkap untuk identifikasi yang jelas
   - Hindari singkatan

4. **Backward Compatibility**
   - Sistem tetap support format lama (hanya nama)
   - Tapi tampilan akan kurang informatif

## 🎯 Use Cases

### 1. Penjemputan Anak Sekolah
```
Ortu datang → Scan wajah → Tampil:
- Nama ortu: Budi Santoso
- Anak: Andi Santoso
- Kelas: 3A
→ Guru tahu harus panggil anak dari kelas 3A
```

### 2. Laporan Kehadiran Ortu
```
Export CSV → Filter by kelas → Kirim ke wali kelas
```

### 3. Statistik per Kelas
```
Cari kelas 3A → Lihat berapa ortu yang sudah terdaftar
```

## 📚 Tools

| Tool | Fungsi |
|------|--------|
| `main.py` | Enrollment & Recognition |
| `view_database.py` | View, search, export database |
| `view_logs.py` | View activity logs |
| `reset_db.py` | Reset database |

## 🔒 Privacy

Label berisi informasi pribadi:
- ✅ Simpan di database lokal
- ❌ Jangan commit ke git public
- ✅ Backup secara terpisah
- ✅ Encrypt jika perlu

## 📖 References

- Main README: `README.md`
- Logging: `LOGGING.md`
- Installation: `INSTALL.md`
- Project Structure: `PROJECT_STRUCTURE.md`
