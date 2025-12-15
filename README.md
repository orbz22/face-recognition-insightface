# Face Recognition System - InsightFace

Sistem face recognition menggunakan InsightFace (buffalo_l model) dengan ArcFace embeddings.

## 📁 Struktur Project

```
face_recog_insightface/
├── main.py                    # Entry point utama (menu interaktif)
├── facegate_insightface.py    # Core library
├── reset_db.py                # Utility untuk reset database
├── models/                    # Model InsightFace (lokal)
│   └── buffalo_l/            # Model buffalo_l
│       ├── det_10g.onnx      # Face detection
│       ├── w600k_r50.onnx    # Face recognition (embedding)
│       ├── genderage.onnx    # Gender & age estimation
│       ├── 1k3d68.onnx       # 3D landmark
│       └── 2d106det.onnx     # 2D landmark
└── face_db/                   # Database wajah
    ├── embeddings.npy         # Face embeddings
    ├── labels.json            # Nama/label
    └── snapshots/             # Foto snapshot saat enroll
```

## 🚀 Cara Menggunakan

### 1. Jalankan Program

```bash
python main.py
```

### 2. Menu Interaktif

**Menu 1: Enroll (Daftarkan Wajah Baru)**
- Masukkan nama orang
- Arahkan wajah ke kamera
- Tekan `c` untuk capture sample (10x)
- Sistem akan menyimpan rata-rata embedding

**Menu 2: Recognize (Kenali Wajah)**
- Sistem akan otomatis mengenali wajah dari database
- Menampilkan nama dan similarity score
- Tekan `q` untuk keluar

**Menu 3: Switch Camera**
- Test kamera saat ini
- Ganti ke camera index lain (0, 1, 2, ...)
- Preview kamera sebelum menggunakan

**Menu 4: Exit**
- Keluar dari program

### 3. Reset Database (Jika Perlu)

```bash
python reset_db.py
```

Ketik `YES` untuk konfirmasi penghapusan semua data.

## ⚙️ Konfigurasi

Edit `main.py` untuk mengubah konfigurasi:

```python
DB_DIR = "face_db"           # Folder database
MODEL_NAME = "buffalo_l"     # Nama model
DEVICE = "cpu"               # "cpu" atau "cuda"
CAM_INDEX = 1                # Index kamera (0, 1, 2, ...)
WIDTH = 1280                 # Resolusi kamera
HEIGHT = 720
DET_SIZE = 640               # Detection size
MIN_DET_SCORE = 0.6          # Minimum detection confidence
SAMPLES = 10                 # Jumlah sample saat enroll
THRESHOLD = 0.35             # Similarity threshold untuk recognize
```

## 🔧 Mode Advanced (CLI)

Gunakan `facegate_insightface.py` langsung untuk kontrol lebih detail:

### Enroll
```bash
python facegate_insightface.py --mode enroll --name "Nama Orang" --cam 1
```

### Recognize
```bash
python facegate_insightface.py --mode recognize --cam 1 --thr 0.35
```

### Opsi Lengkap
```bash
python facegate_insightface.py --help
```

## 📦 Instalasi

### 1. Clone/Download Project

```bash
cd face_recog_insightface
```

### 2. Install Dependencies

**Menggunakan requirements.txt (Recommended):**

```bash
# Untuk CPU (Raspberry Pi / PC tanpa GPU)
pip install -r requirements.txt

# Untuk Development (dengan testing tools)
pip install -r requirements-dev.txt
```

**Manual Install:**

```bash
pip install numpy>=1.26.0 opencv-python>=4.8.0 insightface>=0.7.3 onnxruntime>=1.19.0
```

**Untuk GPU (NVIDIA CUDA):**

```bash
# Ganti onnxruntime dengan onnxruntime-gpu
pip install numpy opencv-python insightface onnxruntime-gpu
```

### 3. Verifikasi Instalasi

```bash
python -c "import insightface; import cv2; import numpy; print('All dependencies installed successfully!')"
```

## 📋 Requirements

File `requirements.txt` berisi semua dependencies yang diperlukan:

- **numpy** >= 1.26.0 - Array operations
- **opencv-python** >= 4.8.0 - Computer vision & camera
- **insightface** >= 0.7.3 - Face recognition models
- **onnxruntime** >= 1.19.0 - Model inference (CPU)

Untuk GPU: gunakan `onnxruntime-gpu` sebagai pengganti `onnxruntime`.

## 🎯 Fitur

- ✅ **Portable**: Model disimpan lokal di folder project
- ✅ **Multi-sample enrollment**: Rata-rata 10 samples untuk akurasi lebih baik
- ✅ **Real-time recognition**: Deteksi dan kenali wajah secara real-time
- ✅ **Switch Camera**: Ganti kamera tanpa restart program
- ✅ **Camera Preview**: Test kamera sebelum digunakan
- ✅ **Snapshot**: Simpan foto saat enroll untuk audit
- ✅ **Cosine similarity**: Menggunakan normalized embeddings
- ✅ **Database validation**: Otomatis cek integritas database
- ✅ **Easy reset**: Script untuk reset database dengan aman

## 📝 Catatan

- **Threshold**: Nilai 0.35 adalah default. Sesuaikan berdasarkan kondisi:
  - 0.3 - 0.4: Lebih permisif (bisa false positive)
  - 0.4 - 0.5: Lebih ketat (lebih akurat tapi bisa false negative)
  
- **Camera Index**: 
  - 0 = Kamera default (biasanya webcam laptop)
  - 1 = Kamera eksternal pertama
  - 2+ = Kamera tambahan

- **Lighting**: Pencahayaan yang baik sangat penting untuk akurasi

## 🔒 Model Location

Model sekarang disimpan di folder `models/` dalam project, bukan di home directory user.
Ini membuat project lebih portable dan mudah di-deploy.

Path model: `./models/buffalo_l/*.onnx`

## 📄 License

Project ini menggunakan InsightFace yang memiliki lisensi sendiri.
Silakan cek: https://github.com/deepinsight/insightface
