# Build EXE - Panduan Lengkap

Panduan untuk membuat executable (.exe) dari Face Recognition System.

## 🎯 Tujuan

Membuat file `.exe` yang bisa dijalankan di Windows tanpa perlu install Python.

## 📋 Prerequisites

1. **Python 3.9+** terinstall
2. **Semua dependencies** terinstall
3. **PyInstaller** terinstall

## 🚀 Cara Build

### Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

### Step 2: Build EXE

**Opsi A: Menggunakan Spec File (Recommended)**

```bash
pyinstaller FaceRecognition.spec
```

**Opsi B: Menggunakan Command Line**

```bash
pyinstaller --name="FaceRecognition" ^
    --onefile ^
    --console ^
    --add-data="models;models" ^
    --add-data="face_db;face_db" ^
    --hidden-import=cv2 ^
    --hidden-import=numpy ^
    --hidden-import=insightface ^
    --hidden-import=onnxruntime ^
    --hidden-import=qrcode ^
    --hidden-import=pyzbar ^
    --hidden-import=cryptography ^
    main.py
```

**Opsi C: Menggunakan Batch File**

```bash
build_exe.bat
```

### Step 3: Test EXE

```bash
cd dist
FaceRecognition.exe
```

## 📁 Output

Setelah build, struktur folder:

```
project/
├── dist/
│   └── FaceRecognition.exe    ← File EXE (distribusi ini)
├── build/                      ← Folder temporary (bisa dihapus)
└── FaceRecognition.spec        ← Spec file
```

## 📦 Yang Perlu Didistribusikan

### Opsi 1: EXE + Models (Lengkap)

**Struktur folder untuk distribusi:**

```
FaceRecognition/
├── FaceRecognition.exe
├── models/
│   └── buffalo_l/
│       ├── det_10g.onnx
│       ├── w600k_r50.onnx
│       ├── genderage.onnx
│       ├── 1k3d68.onnx
│       └── 2d106det.onnx
├── face_db/
│   └── README.md
├── qr_codes/
│   └── (kosong)
└── README.md
```

**Ukuran:** ~400MB (karena model)

**Cara distribusi:**
```bash
# Zip semua
Compress-Archive -Path FaceRecognition -DestinationPath FaceRecognition_v1.0.zip

# Upload ke Google Drive / Dropbox
# Share link ke teman
```

### Opsi 2: EXE Only (Kecil)

**Struktur folder:**

```
FaceRecognition/
├── FaceRecognition.exe
├── README.md
└── INSTALL.md
```

**Ukuran:** ~50MB (tanpa model)

**Catatan:** Model akan auto-download saat pertama kali run.

## ⚙️ Build Options

### Console vs Windowed

**Console (Recommended untuk debugging):**
```python
# Di spec file:
console=True
```

**Windowed (No console window):**
```python
# Di spec file:
console=False
```

### One File vs One Directory

**One File (Single EXE):**
```bash
pyinstaller --onefile main.py
```
- ✅ Mudah distribusi (1 file)
- ❌ Startup lebih lambat
- ❌ Ukuran lebih besar

**One Directory (Folder dengan dependencies):**
```bash
pyinstaller --onedir main.py
```
- ✅ Startup lebih cepat
- ✅ Ukuran lebih kecil
- ❌ Banyak file

## 🐛 Troubleshooting

### Error: "Module not found"

**Solusi:** Tambahkan hidden import

```python
# Di spec file, tambahkan ke hiddenimports:
hiddenimports = [
    'module_name',
]
```

### Error: "Failed to execute script"

**Solusi:** Build dengan console mode untuk lihat error

```bash
pyinstaller --console main.py
```

### Error: "ONNX Runtime not found"

**Solusi:** Pastikan onnxruntime terinstall

```bash
pip install onnxruntime
```

### EXE Terlalu Besar

**Solusi:** Exclude modules yang tidak perlu

```python
# Di spec file:
excludes=['matplotlib', 'scipy', 'pandas']
```

### Model Tidak Ditemukan

**Solusi:** Pastikan models folder ada di folder yang sama dengan EXE

```
FaceRecognition/
├── FaceRecognition.exe
└── models/          ← Harus ada di sini
```

## 📊 Ukuran File

| Component | Size |
|-----------|------|
| EXE only | ~50 MB |
| Models (buffalo_l) | ~340 MB |
| **Total** | **~400 MB** |

## 🔒 Security

### Antivirus False Positive

EXE yang dibuat PyInstaller sering di-flag sebagai virus (false positive).

**Solusi:**
1. **Code signing** (butuh certificate)
2. **Submit ke antivirus vendors** untuk whitelist
3. **Instruksikan user** untuk add exception

### Obfuscation

Untuk protect source code:

```bash
pip install pyarmor
pyarmor obfuscate main.py
pyinstaller obfuscated/main.py
```

## 📝 Best Practices

### 1. Version Control

Tambahkan ke `.gitignore`:

```gitignore
# PyInstaller
build/
dist/
*.spec
```

### 2. Versioning

Tambahkan version info:

```python
# Di main.py
__version__ = "1.0.0"
print(f"Face Recognition System v{__version__}")
```

### 3. Testing

Test EXE di komputer lain (clean install):
- ✅ Windows 10
- ✅ Windows 11
- ✅ Tanpa Python terinstall

### 4. Documentation

Include README.md dengan:
- System requirements
- Installation steps
- Usage guide
- Troubleshooting

## 🚀 Advanced: Auto-Updater

Untuk auto-update EXE:

```python
# check_update.py
import requests

def check_update():
    response = requests.get("https://api.github.com/repos/orbz22/face-recognition-insightface/releases/latest")
    latest_version = response.json()["tag_name"]
    
    if latest_version > __version__:
        print(f"Update available: {latest_version}")
        # Download dan install
```

## 📦 Distribution Platforms

### GitHub Releases

```bash
# Create release
gh release create v1.0.0 dist/FaceRecognition.exe

# Users download:
# https://github.com/orbz22/face-recognition-insightface/releases
```

### Google Drive

```bash
# Upload FaceRecognition.zip
# Share link dengan teman
```

### Microsoft Store (Advanced)

Convert EXE ke MSIX package untuk Microsoft Store.

## 🎯 Checklist Build

- [ ] PyInstaller terinstall
- [ ] Semua dependencies terinstall
- [ ] Models ada di folder models/
- [ ] Test program berjalan normal
- [ ] Build EXE
- [ ] Test EXE di komputer lain
- [ ] Zip untuk distribusi
- [ ] Upload ke platform sharing
- [ ] Share link ke teman

## 📚 Resources

- PyInstaller Docs: https://pyinstaller.org/
- PyInstaller GitHub: https://github.com/pyinstaller/pyinstaller
- Code Signing: https://docs.microsoft.com/en-us/windows/win32/seccrypto/cryptography-tools

---

**Ready to build? Run: `pyinstaller FaceRecognition.spec`** 🚀
