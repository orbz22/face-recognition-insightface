# Setup Guide untuk Teman

Panduan lengkap untuk setup Face Recognition System di komputer teman Anda.

## 📋 System Requirements

- **Python:** 3.9, 3.10, 3.11, atau 3.12
- **OS:** Windows 10/11, Linux, atau macOS
- **RAM:** Minimal 4GB (8GB recommended)
- **Webcam:** Built-in atau USB webcam
- **Internet:** Untuk download model pertama kali

---

## 🚀 Quick Start

### Step 1: Clone Repository

```bash
git clone https://github.com/orbz22/face-recognition-insightface.git
cd face-recognition-insightface
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Catatan:** Instalasi akan memakan waktu beberapa menit.

### Step 4: Run Program

```bash
python main.py
```

Program akan otomatis download model InsightFace (~340MB) saat pertama kali run.

---

## 🐛 Troubleshooting

### Issue 1: Python Version

**Error:**
```
Python version not supported
```

**Solution:**
- Pastikan Python 3.9 - 3.12
- Check version: `python --version`
- Download dari: https://python.org

### Issue 2: pip not found

**Error:**
```
'pip' is not recognized
```

**Solution:**
```bash
python -m pip install -r requirements.txt
```

### Issue 3: NumPy 2.0 Conflict

**Error:**
```
numpy 2.0 incompatible
```

**Solution:**
```bash
pip install "numpy<2.0"
pip install -r requirements.txt
```

### Issue 4: pyzbar DLL Error

**Error:**
```
Failed to load dynlib/dll 'libiconv.dll'
```

**Solution:**
- QR code feature akan auto-disabled
- Program tetap jalan normal
- Face recognition tetap works 100%

**Optional fix (Windows):**
```bash
# Download zbar from: https://sourceforge.net/projects/zbar/
# Install zbar
# Restart program
```

### Issue 5: Camera Not Found

**Error:**
```
Camera 1 cannot be opened
```

**Solution:**
```bash
# Jalankan program
# Pilih Menu 3 (Switch Camera)
# Coba camera index 0, 1, 2, dst
```

### Issue 6: Model Download Failed

**Error:**
```
Failed to download model
```

**Solution:**
1. **Manual download:**
   - Download dari: https://github.com/deepinsight/insightface/releases/download/v0.7/buffalo_l.zip
   - Extract ke folder `models/`
   - Struktur: `models/buffalo_l/*.onnx`

2. **Check internet connection**

3. **Retry:**
   ```bash
   python main.py
   ```

---

## 📁 Project Structure

```
face-recognition-insightface/
├── main.py                  ← Program utama
├── facegate_insightface.py  ← Face recognition logic
├── logger.py                ← Logging system
├── qr_manager.py            ← QR code (optional)
├── view_database.py         ← Database viewer
├── reset_db.py              ← Database reset
├── requirements.txt         ← Dependencies
├── models/                  ← InsightFace models
│   └── buffalo_l/
├── face_db/                 ← Database wajah
│   ├── embeddings.npy
│   └── labels.json
├── qr_codes/                ← QR codes (optional)
└── logs/                    ← Log files
    ├── access.log
    └── system.log
```

---

## 🎯 Usage

### Enroll Wajah Baru

```bash
python main.py
# Pilih Menu 1 (Enroll)
# Input: Nama Ortu, Nama Anak, Kelas
# Tekan 'c' untuk capture (10x)
# Selesai!
```

### Recognize Wajah

```bash
python main.py
# Pilih Menu 2 (Recognize)
# Arahkan wajah ke kamera
# Sistem otomatis recognize
# Tekan 'q' untuk keluar
```

### View Database

```bash
python view_database.py
# Pilih opsi yang diinginkan
```

### Reset Database

```bash
python reset_db.py
# Konfirmasi untuk reset
```

---

## 🔧 Configuration

Edit `main.py` untuk custom settings:

```python
# Line ~200-210
CAM_INDEX = 1      # Camera index (0, 1, 2, ...)
WIDTH = 640        # Camera width
HEIGHT = 480       # Camera height
DET_SIZE = 320     # Detection size
THRESHOLD = 0.35   # Recognition threshold
SAMPLES = 10       # Enrollment samples
```

---

## 📊 Performance Tips

### Jika Lag/Slow:

1. **Reduce resolution:**
   ```python
   WIDTH = 320
   HEIGHT = 240
   ```

2. **Reduce detection size:**
   ```python
   DET_SIZE = 160
   ```

3. **Increase frame skip:**
   Edit `facegate_insightface.py` line ~390:
   ```python
   if frame_count % 5 == 0:  # Skip more frames
   ```

### Jika Ingin Akurasi Lebih Tinggi:

1. **Increase resolution:**
   ```python
   WIDTH = 1280
   HEIGHT = 720
   ```

2. **Increase detection size:**
   ```python
   DET_SIZE = 640
   ```

3. **Lower threshold:**
   ```python
   THRESHOLD = 0.30  # More strict
   ```

---

## 🌐 Sharing Database

### Cara 1: Share Entire Database

```bash
# Zip database
zip -r face_db.zip face_db/

# Kirim face_db.zip ke teman
# Teman extract di project folder
```

### Cara 2: Add to Existing Database

```bash
# Teman enroll wajah baru
python main.py
# Menu 1 (Enroll)

# Kirim file baru:
# - face_db/embeddings.npy
# - face_db/labels.json
```

### Cara 3: Merge Databases

```bash
# Belum ada script otomatis
# Manual: Copy embeddings dan labels
# Atau gunakan view_database.py untuk export/import
```

---

## 🔐 Security Notes

**Files yang JANGAN di-share public:**
- `face_db/embeddings.npy` - Face data (private)
- `face_db/labels.json` - Personal info (private)
- `face_db/.qr_key` - Encryption key (secret)
- `qr_codes/*.png` - QR codes (private)
- `logs/*.log` - Access logs (private)

**Files yang OK untuk share:**
- Source code (`.py` files)
- Documentation (`.md` files)
- `requirements.txt`

---

## 📞 Support

Jika ada masalah:

1. **Check logs:**
   ```bash
   # Windows
   type logs\system.log
   
   # Linux/Mac
   cat logs/system.log
   ```

2. **Check GitHub Issues:**
   https://github.com/orbz22/face-recognition-insightface/issues

3. **Contact developer**

---

## ✅ Checklist Setup

- [ ] Python 3.9-3.12 terinstall
- [ ] Git terinstall (optional)
- [ ] Clone/download repository
- [ ] Create virtual environment
- [ ] Install dependencies (`pip install -r requirements.txt`)
- [ ] Run program (`python main.py`)
- [ ] Model downloaded successfully
- [ ] Camera detected
- [ ] Enroll test face
- [ ] Recognition works
- [ ] Done! 🎉

---

## 🚀 Next Steps

1. **Enroll semua wajah** yang diperlukan
2. **Test recognition** dengan berbagai kondisi
3. **Backup database** secara berkala
4. **Monitor logs** untuk troubleshooting
5. **Enjoy!** 😊

---

**Happy Face Recognition!** 🎉
