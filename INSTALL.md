# Panduan Instalasi - Face Recognition System

Panduan lengkap untuk instalasi Face Recognition System menggunakan InsightFace.

## 📋 Prasyarat

### Sistem Operasi
- Windows 10/11
- Linux (Ubuntu 20.04+)
- macOS (10.15+)
- Raspberry Pi OS (Bullseye+)

### Python
- Python 3.8 atau lebih baru
- pip (package manager)

### Hardware
- Kamera (webcam/USB camera)
- RAM minimal 4GB (8GB recommended)
- Storage: ~500MB untuk model

## 🚀 Instalasi

### Metode 1: Menggunakan requirements.txt (Recommended)

#### Windows

```powershell
# 1. Buat virtual environment (optional tapi recommended)
python -m venv venv
.\venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verifikasi instalasi
python -c "import insightface; import cv2; import numpy; print('OK!')"
```

#### Linux / macOS / Raspberry Pi

```bash
# 1. Buat virtual environment (optional tapi recommended)
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verifikasi instalasi
python -c "import insightface; import cv2; import numpy; print('OK!')"
```

### Metode 2: Manual Install

```bash
pip install numpy>=1.26.0
pip install opencv-python>=4.8.0
pip install insightface>=0.7.3
pip install onnxruntime>=1.19.0
```

### Untuk GPU (NVIDIA CUDA)

Jika Anda memiliki GPU NVIDIA dengan CUDA:

```bash
# Install onnxruntime-gpu sebagai pengganti onnxruntime
pip install numpy opencv-python insightface onnxruntime-gpu
```

**Catatan**: Pastikan CUDA dan cuDNN sudah terinstall di sistem Anda.

## 🔍 Verifikasi Instalasi

### Test Import Modules

```bash
python -c "import insightface; print('InsightFace:', insightface.__version__)"
python -c "import cv2; print('OpenCV:', cv2.__version__)"
python -c "import numpy; print('NumPy:', numpy.__version__)"
python -c "import onnxruntime; print('ONNX Runtime:', onnxruntime.__version__)"
```

### Test Camera

```bash
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK!' if cap.isOpened() else 'Camera Error'); cap.release()"
```

### Test Model Loading

```bash
python -c "from facegate_insightface import build_face_app; app = build_face_app(); print('Model loaded successfully!')"
```

## 🛠️ Troubleshooting

### Error: "No module named 'insightface'"

```bash
pip install insightface
```

### Error: "Camera cannot be opened"

1. Pastikan kamera tidak digunakan aplikasi lain
2. Coba camera index berbeda (0, 1, 2)
3. Periksa permission kamera (Windows/macOS)

### Error: "ONNX Runtime error"

Untuk CPU:
```bash
pip uninstall onnxruntime onnxruntime-gpu
pip install onnxruntime
```

Untuk GPU:
```bash
pip uninstall onnxruntime onnxruntime-gpu
pip install onnxruntime-gpu
```

### Error: "Model not found"

Pastikan folder `models/buffalo_l/` ada dan berisi file .onnx:
```bash
ls models/buffalo_l/
# Harus ada: det_10g.onnx, w600k_r50.onnx, dll
```

### Raspberry Pi: Memory Error

Jika RAM terbatas, gunakan swap:

```bash
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# Ubah CONF_SWAPSIZE=2048
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

## 📦 Development Setup

Untuk development dengan testing tools:

```bash
pip install -r requirements-dev.txt
```

Ini akan menginstall:
- pytest (testing)
- black (code formatting)
- flake8 (linting)
- mypy (type checking)
- jupyter (notebook)

## 🔄 Update Dependencies

```bash
# Update semua packages
pip install --upgrade -r requirements.txt

# Update package tertentu
pip install --upgrade insightface
```

## ✅ Checklist Instalasi

- [ ] Python 3.8+ terinstall
- [ ] Virtual environment dibuat (optional)
- [ ] Dependencies terinstall (`pip install -r requirements.txt`)
- [ ] Import modules berhasil
- [ ] Camera terdeteksi
- [ ] Model berhasil di-load
- [ ] Program `main.py` bisa dijalankan

## 🎯 Next Steps

Setelah instalasi selesai:

1. Jalankan program: `python main.py`
2. Pilih menu 3 untuk test camera
3. Pilih menu 1 untuk enroll wajah pertama
4. Pilih menu 2 untuk test recognition

## 📞 Support

Jika mengalami masalah:
1. Cek versi Python: `python --version`
2. Cek versi pip: `pip --version`
3. Cek installed packages: `pip list`
4. Baca error message dengan teliti
5. Cek dokumentasi InsightFace: https://github.com/deepinsight/insightface

## 📝 Notes

- **Virtual Environment**: Sangat direkomendasikan untuk menghindari konflik dependencies
- **GPU**: Opsional, CPU sudah cukup untuk real-time recognition
- **Model Size**: Model buffalo_l ~340MB, pastikan ada space cukup
- **Internet**: Diperlukan saat pertama kali install dependencies
