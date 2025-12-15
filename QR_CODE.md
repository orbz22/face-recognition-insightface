# QR Code System - Face Recognition Fallback

Sistem QR Code terintegrasi sebagai backup/fallback untuk face recognition.

## 🎯 Use Case

QR Code berguna saat:
- Face recognition gagal (lighting buruk, kamera rusak, dll)
- Orang tua lupa/tidak bisa scan wajah
- Verifikasi ganda (face + QR code)
- Backup system

## 🔐 Keamanan

### Enkripsi
- Setiap QR code **dienkripsi** menggunakan Fernet (symmetric encryption)
- Encryption key disimpan di `face_db/.qr_key`
- Data dalam QR code: ID unik + Label + Index
- **TIDAK bisa diduplikasi** tanpa encryption key

### Format Data
```json
{
  "id": "a1b2c3d4e5f6g7h8",
  "label": "majid_Fahmi Majid_TK-A",
  "index": 0
}
```

Data ini di-encrypt → Base64 → QR Code

## 📋 Cara Menggunakan

### 1. Generate QR Codes

```bash
python main.py
# Pilih menu 4 (QR Code Menu)
# Pilih 1 (Generate QR Codes untuk Semua)
```

Output:
```
[*] Generating QR codes untuk 2 orang...
  [OK] majid_Fahmi Majid_TK-A → majid_Fahmi Majid_TK-A.png
  [OK] sulthon_Aisha Sulthon_TK-B → sulthon_Aisha Sulthon_TK-B.png

[OK] 2 QR codes berhasil di-generate!
     Lokasi: qr_codes/
```

### 2. Cetak QR Codes

QR codes tersimpan di folder `qr_codes/`:
```
qr_codes/
├── majid_Fahmi Majid_TK-A.png
└── sulthon_Aisha Sulthon_TK-B.png
```

**Cetak dan berikan ke orang tua:**
- Print di kertas
- Laminating (recommended)
- Bisa juga simpan di HP (screenshot)

### 3. Scan QR Code

```bash
python main.py
# Pilih menu 4 (QR Code Menu)
# Pilih 2 (Scan QR Code)
# Arahkan QR code ke kamera
```

Output jika berhasil:
```
[OK] QR Code berhasil di-scan!
     Label: majid_Fahmi Majid_TK-A
     Nama Ortu: majid
     Nama Anak: Fahmi Majid
     Kelas: TK-A
     Status: VALID ✓
```

## 🔄 Workflow

### Skenario 1: Face Recognition Berhasil
```
1. Ortu datang
2. Scan wajah → Terdeteksi ✓
3. Akses granted
```

### Skenario 2: Face Recognition Gagal → QR Fallback
```
1. Ortu datang
2. Scan wajah → Gagal ✗
3. Ortu tunjukkan QR code
4. Scan QR → Valid ✓
5. Akses granted
```

### Skenario 3: Verifikasi Ganda
```
1. Ortu datang
2. Scan wajah → Terdeteksi ✓
3. Minta QR code untuk konfirmasi
4. Scan QR → Valid ✓
5. Akses granted (double verified)
```

## 📊 Keuntungan QR Code

| Aspek | Face Recognition | QR Code |
|-------|------------------|---------|
| **Kecepatan** | Cepat (real-time) | Sangat cepat |
| **Akurasi** | 85-95% | 100% (jika valid) |
| **Kondisi** | Butuh lighting bagus | Tidak terpengaruh lighting |
| **Hardware** | Kamera bagus | Kamera biasa OK |
| **Backup** | Tidak ada | QR code fisik |
| **Keamanan** | Biometric (tinggi) | Encrypted (tinggi) |

## 🛠️ Technical Details

### QR Code Generation

```python
from qr_manager import QRCodeManager

qr_manager = QRCodeManager()

# Generate untuk semua
qr_manager.generate_qr_for_all()

# Generate untuk satu orang
qr_manager.generate_qr_code("majid_Fahmi Majid_TK-A", index=0)
```

### QR Code Scanning

```python
from qr_manager import QRCodeManager

qr_manager = QRCodeManager()

# Scan dari kamera
result = qr_manager.scan_qr_from_camera(cam_index=1)

if result:
    print(f"Label: {result['label']}")
    print(f"Index: {result['index']}")
    
    # Verify
    if qr_manager.verify_qr_data(result):
        print("VALID")
    else:
        print("INVALID")
```

### Encryption/Decryption

```python
# Encrypt
encrypted = qr_manager.encrypt_data("sensitive data")

# Decrypt
decrypted = qr_manager.decrypt_data(encrypted)
```

## 🔒 Security Best Practices

### 1. Protect Encryption Key
```bash
# Backup encryption key
cp face_db/.qr_key face_db/.qr_key.backup

# JANGAN commit ke git (sudah di .gitignore)
# JANGAN share ke orang lain
```

### 2. QR Code Distribution
- ✅ Cetak dan laminating
- ✅ Simpan di HP (password protected)
- ❌ Jangan post di social media
- ❌ Jangan share foto QR code

### 3. Regenerate QR Codes
Jika encryption key hilang/bocor:
```bash
# 1. Delete encryption key
rm face_db/.qr_key

# 2. Generate ulang QR codes
python main.py
# Menu 4 → 1 (Generate QR Codes)

# 3. Distribusi ulang QR codes baru
```

## 📝 Logging

QR code scans tercatat di `logs/access.log`:

```
2025-12-15 22:30:00 | INFO | ACCESS | GRANTED | Name: majid_Fahmi Majid_TK-A | Reason: QR Code scan
```

## 🔧 Troubleshooting

### QR Code tidak ter-scan?
- Pastikan QR code jelas (tidak blur)
- Coba lebih dekat/jauh dari kamera
- Pastikan lighting cukup
- Coba kamera lain

### "Decryption Failed"?
- QR code dari system lain (encryption key berbeda)
- QR code rusak/corrupt
- Generate ulang QR code

### "Invalid QR Code"?
- Data dalam QR tidak match dengan database
- Database sudah berubah sejak QR di-generate
- Generate ulang QR code

## 📦 Dependencies

```bash
pip install qrcode[pil] pyzbar cryptography pillow
```

### Platform-specific

**Windows:**
```bash
# pyzbar butuh zbar library
# Download: http://zbar.sourceforge.net/
# Atau install via conda:
conda install -c conda-forge pyzbar
```

**Linux:**
```bash
sudo apt-get install libzbar0
pip install pyzbar
```

**macOS:**
```bash
brew install zbar
pip install pyzbar
```

## 🎨 Customization

### QR Code Size
Edit `qr_manager.py`:
```python
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,  # ← Ubah ini (default: 10)
    border=4,     # ← Ubah ini (default: 4)
)
```

### QR Code Color
```python
img = qr.make_image(
    fill_color="black",   # ← Warna QR
    back_color="white"    # ← Warna background
)
```

## 📊 Statistics

Lihat statistik QR code scans:
```bash
python view_logs.py
# Pilih 4 (View Access Log)
```

Filter QR code scans:
```bash
grep "QR Code scan" logs/access.log
```

## 🔄 Backup & Restore

### Backup
```bash
# Backup QR codes
cp -r qr_codes qr_codes_backup

# Backup encryption key
cp face_db/.qr_key qr_key_backup
```

### Restore
```bash
# Restore QR codes
cp -r qr_codes_backup qr_codes

# Restore encryption key
cp qr_key_backup face_db/.qr_key
```

## 📚 References

- QR Code: https://github.com/lincolnloop/python-qrcode
- pyzbar: https://github.com/NaturalHistoryMuseum/pyzbar
- Cryptography: https://cryptography.io/
- Fernet: https://cryptography.io/en/latest/fernet/

## 🎯 Best Practices

1. **Generate QR codes setelah enrollment selesai**
2. **Cetak dan laminating untuk durability**
3. **Backup encryption key secara terpisah**
4. **Regenerate QR codes jika database berubah**
5. **Log semua QR code scans untuk audit**
6. **Kombinasikan dengan face recognition untuk keamanan maksimal**

---

**QR Code system siap digunakan sebagai backup untuk face recognition!** 🎉
