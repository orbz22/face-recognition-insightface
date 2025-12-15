# QR Code Troubleshooting Guide

## ⚠️ Warning Messages (Normal)

Jika Anda melihat warning seperti ini saat scan QR code:

```
WARNING: .\zbar\decoder\pdf417.c:89: <unknown>: Assertion "g[0] >= 0 && g[1] >= 0 && g[2] >= 0" failed.
```

**Ini NORMAL!** Warning ini dari pyzbar library dan tidak mempengaruhi fungsi QR scanner.

---

## ❌ QR Code Tidak Ter-scan?

### **Checklist:**

#### 1. **Jarak QR Code**
- ✅ Jarak ideal: **20-30cm** dari kamera
- ❌ Terlalu dekat: QR code blur
- ❌ Terlalu jauh: QR code terlalu kecil

#### 2. **Posisi QR Code**
- ✅ QR code **rata** menghadap kamera
- ❌ QR code miring/bengkok
- ❌ QR code terlipat

#### 3. **Lighting**
- ✅ Cahaya cukup terang
- ❌ Terlalu gelap
- ❌ Silau (terlalu terang)
- ❌ Bayangan menutupi QR code

#### 4. **Kualitas QR Code**
- ✅ Print jelas (tidak blur)
- ✅ Kontras bagus (hitam-putih)
- ❌ Print blur/kabur
- ❌ Warna pudar

#### 5. **Kamera**
- ✅ Kamera fokus
- ❌ Kamera blur/kotor
- ❌ Resolusi terlalu rendah

---

## 🔧 Solusi

### **Solusi 1: Cetak QR Code Lebih Besar**

QR code yang lebih besar lebih mudah di-scan:

```python
# Edit qr_manager.py, line ~140
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=30,  # ← Ubah dari 20 ke 30 (lebih besar lagi!)
    border=2,
)
```

Lalu regenerate QR codes:
```bash
python main.py
# Menu 4 → 1 (Generate QR Codes)
```

### **Solusi 2: Print di Kertas Putih**

- Print QR code di kertas putih (bukan kertas berwarna)
- Gunakan printer yang bagus (tidak blur)
- Laminating (optional, untuk durability)

### **Solusi 3: Tampilkan QR di Layar HP**

Jika print tidak bagus, bisa tampilkan QR code di layar HP:

1. Buka file QR code: `qr_codes/nama_ortu.png`
2. Kirim ke HP (WhatsApp/Email)
3. Buka di HP dengan brightness maksimal
4. Scan dari layar HP

### **Solusi 4: Gunakan Kamera yang Lebih Bagus**

Jika kamera terlalu buruk:
```bash
python main.py
# Menu 3 (Switch Camera)
# Coba kamera lain
```

### **Solusi 5: Scan Manual (Fallback)**

Jika QR code tetap tidak bisa di-scan, gunakan **manual verification**:

1. Lihat nama di QR code file: `majid_Fahmi_TK-A.png`
2. Cari di database:
   ```bash
   python view_database.py
   # Pilih 2 (Cari Berdasarkan Nama Anak)
   # Input: Fahmi
   ```
3. Verify manual dengan melihat data

---

## 💡 Tips Terbaik

### **Untuk Scanning:**

1. **Gunakan Lighting yang Bagus**
   - Natural light (siang hari)
   - Atau lampu putih terang

2. **Pegang QR Code Stabil**
   - Jangan goyang
   - Tempelkan di permukaan datar

3. **Bersihkan Kamera**
   - Lap kamera dengan kain lembut
   - Pastikan tidak ada debu/sidik jari

4. **Jarak Optimal**
   - Mulai dari jarak 30cm
   - Perlahan mendekat/menjauh
   - Sampai QR code terdeteksi

### **Untuk Printing:**

1. **Print dengan Kualitas Tinggi**
   - Gunakan printer laser (lebih tajam)
   - Atau inkjet dengan kualitas "Best"

2. **Ukuran Minimal**
   - Minimal 5x5 cm
   - Ideal: 7x7 cm atau lebih besar

3. **Laminating**
   - Protect QR code dari kotor/rusak
   - Lebih tahan lama

---

## 🔍 Debug Mode

Jika ingin lihat proses scanning:

Edit `qr_manager.py`, uncomment line ini:

```python
# Line ~225 (di dalam scan_qr_from_camera)
cv2.imshow("Threshold", thresh)  # ← Uncomment ini
```

Ini akan menampilkan window tambahan yang menunjukkan preprocessing image.

---

## 📊 Perbandingan Metode Scan

| Metode | Kecepatan | Akurasi | Rekomendasi |
|--------|-----------|---------|-------------|
| **Print di Kertas** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ Terbaik |
| **Layar HP** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ Bagus |
| **Print Blur** | ⭐ | ⭐⭐ | ❌ Tidak disarankan |

---

## 🆘 Masih Tidak Bisa?

Jika sudah coba semua cara di atas tapi tetap tidak bisa:

### **Opsi 1: Gunakan Face Recognition Saja**
```bash
python main.py
# Menu 2 (Recognize)
# Scan wajah langsung
```

### **Opsi 2: Manual Entry**
Buat script sederhana untuk manual entry:

```python
# manual_verify.py
from view_database import parse_label

name = input("Nama Orang Tua: ")
# Cari di database
# Verify manual
```

### **Opsi 3: Upgrade Kamera**
- Beli webcam USB yang lebih bagus
- Minimal 720p resolution
- Harga: ~100-200rb

---

## 📝 Catatan Penting

1. **QR Code Simplified**
   - Sudah disederhanakan (box_size=20)
   - Hanya menyimpan index (bukan full data)
   - Lebih mudah di-scan

2. **Encryption Tetap Aman**
   - Meskipun simple, tetap encrypted
   - Tidak bisa diduplikasi tanpa encryption key

3. **Backup Method**
   - QR code adalah backup
   - Face recognition adalah primary method
   - Gunakan QR jika face recognition gagal

---

## ✅ Checklist Sebelum Scan

- [ ] QR code dicetak jelas
- [ ] Lighting cukup terang
- [ ] Kamera bersih dan fokus
- [ ] Jarak 20-30cm
- [ ] QR code rata (tidak miring)
- [ ] Tidak ada bayangan
- [ ] Kamera sudah benar (check dengan menu 3)

---

**Jika masih ada masalah, silakan hubungi developer atau gunakan face recognition sebagai alternatif!** 🚀
