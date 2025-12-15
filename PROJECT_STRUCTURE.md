# Struktur Project - Face Recognition System

Dokumentasi lengkap struktur file dan folder project.

## 📁 Tree Structure

```
face_recog_insightface/
│
├── 📄 main.py                      # Entry point utama dengan menu interaktif
├── 📄 facegate_insightface.py      # Core library (FaceDB, build_face_app, modes)
├── 📄 reset_db.py                  # Utility untuk reset database
│
├── 📄 requirements.txt             # Dependencies untuk production
├── 📄 requirements-dev.txt         # Dependencies untuk development
├── 📄 .gitignore                   # Git ignore rules
│
├── 📄 README.md                    # Dokumentasi utama
├── 📄 INSTALL.md                   # Panduan instalasi lengkap
├── 📄 PROJECT_STRUCTURE.md         # Dokumentasi struktur (file ini)
│
├── 📁 models/                      # Model InsightFace (lokal)
│   └── 📁 buffalo_l/               # Model buffalo_l (~340MB)
│       ├── det_10g.onnx            # Face detection (17MB)
│       ├── w600k_r50.onnx          # Face recognition/embedding (174MB)
│       ├── genderage.onnx          # Gender & age estimation (1.3MB)
│       ├── 1k3d68.onnx             # 3D facial landmark (144MB)
│       └── 2d106det.onnx           # 2D facial landmark (5MB)
│
└── 📁 face_db/                     # Database wajah terdaftar
    ├── embeddings.npy              # Face embeddings (numpy array)
    ├── labels.json                 # Nama/label untuk setiap embedding
    └── 📁 snapshots/               # Foto snapshot saat enrollment
        └── 📁 [nama_orang]/        # Folder per orang
            └── *.jpg               # Snapshot images
```

## 📄 File Descriptions

### Core Files

#### `main.py`
- **Fungsi**: Entry point utama program
- **Fitur**:
  - Menu interaktif (Enroll, Recognize, Switch Camera, Exit)
  - Konfigurasi default (camera, model, threshold, dll)
  - Error handling
- **Dependencies**: facegate_insightface.py, cv2

#### `facegate_insightface.py`
- **Fungsi**: Core library untuk face recognition
- **Classes**:
  - `FaceDB`: Manajemen database (load, save, add)
- **Functions**:
  - `build_face_app()`: Load InsightFace model
  - `enroll_mode()`: Mode enrollment wajah
  - `recognize_mode()`: Mode recognition real-time
  - `pick_largest_face()`: Pilih wajah terbesar
  - `open_camera()`: Buka kamera
  - `draw_box_and_text()`: Draw bounding box
- **Dependencies**: insightface, cv2, numpy

#### `reset_db.py`
- **Fungsi**: Utility untuk reset/clear database
- **Fitur**:
  - Konfirmasi sebelum delete
  - Hapus embeddings.npy
  - Reset labels.json
  - Hapus snapshots
- **Usage**: `python reset_db.py`

### Configuration Files

#### `requirements.txt`
- **Fungsi**: Production dependencies
- **Packages**:
  - numpy >= 1.26.0
  - opencv-python >= 4.8.0
  - insightface >= 0.7.3
  - onnxruntime >= 1.19.0
- **Usage**: `pip install -r requirements.txt`

#### `requirements-dev.txt`
- **Fungsi**: Development dependencies
- **Packages**: pytest, black, flake8, mypy, jupyter
- **Usage**: `pip install -r requirements-dev.txt`

#### `.gitignore`
- **Fungsi**: Git ignore rules
- **Ignores**: __pycache__, venv, .vscode, dll

### Documentation Files

#### `README.md`
- **Fungsi**: Dokumentasi utama project
- **Isi**:
  - Overview project
  - Cara menggunakan
  - Konfigurasi
  - Fitur
  - Catatan penting

#### `INSTALL.md`
- **Fungsi**: Panduan instalasi lengkap
- **Isi**:
  - Prasyarat sistem
  - Langkah instalasi (Windows/Linux/macOS/RPi)
  - Verifikasi instalasi
  - Troubleshooting
  - Development setup

#### `PROJECT_STRUCTURE.md`
- **Fungsi**: Dokumentasi struktur project (file ini)
- **Isi**:
  - Tree structure
  - Deskripsi setiap file
  - Flow diagram
  - Data format

## 📁 Directory Descriptions

### `models/`
- **Fungsi**: Menyimpan model InsightFace lokal
- **Size**: ~340MB
- **Format**: ONNX (.onnx)
- **Model**: buffalo_l (high accuracy)
- **Portable**: Ya, bisa di-copy ke komputer lain

### `models/buffalo_l/`
- **det_10g.onnx**: Face detector (RetinaFace)
- **w600k_r50.onnx**: Face recognizer (ArcFace ResNet50)
- **genderage.onnx**: Gender & age estimator
- **1k3d68.onnx**: 3D landmark detector (68 points)
- **2d106det.onnx**: 2D landmark detector (106 points)

### `face_db/`
- **Fungsi**: Database wajah terdaftar
- **Format**: NumPy array + JSON
- **Portable**: Ya, bisa di-backup/restore

#### `embeddings.npy`
- **Format**: NumPy array (N x 512)
- **N**: Jumlah wajah terdaftar
- **512**: Dimensi embedding (ArcFace)
- **Type**: float32
- **Normalized**: Ya (L2 normalized)

#### `labels.json`
- **Format**: JSON array of strings
- **Example**: `["Alice", "Bob", "Charlie"]`
- **Encoding**: UTF-8
- **Index**: Sesuai dengan row di embeddings.npy

#### `snapshots/`
- **Fungsi**: Menyimpan foto saat enrollment
- **Format**: JPEG
- **Struktur**: `snapshots/[nama]/[timestamp]_[sample_num].jpg`
- **Purpose**: Audit, debugging, re-training

## 🔄 Data Flow

### Enrollment Flow
```
User Input (nama) 
  → Camera Capture (10 samples)
  → Face Detection (det_10g.onnx)
  → Face Embedding (w600k_r50.onnx)
  → Average Embeddings
  → L2 Normalize
  → Save to embeddings.npy + labels.json
  → Save snapshots (optional)
```

### Recognition Flow
```
Camera Stream
  → Face Detection (det_10g.onnx)
  → Pick Largest Face
  → Face Embedding (w600k_r50.onnx)
  → L2 Normalize
  → Cosine Similarity vs Database
  → Threshold Check (>= 0.35)
  → Display Result (Name + Similarity)
```

## 💾 Data Format

### embeddings.npy
```python
# Shape: (N, 512) where N = number of registered faces
# Type: numpy.ndarray, dtype=float32
# Range: [-1, 1] (L2 normalized)
# Example:
array([
    [0.123, -0.456, 0.789, ...],  # Person 1
    [0.234, -0.567, 0.890, ...],  # Person 2
], dtype=float32)
```

### labels.json
```json
[
  "Alice",
  "Bob",
  "Charlie"
]
```

## 🔧 Configuration

### Default Settings (main.py)
```python
DB_DIR = "face_db"           # Database folder
MODEL_NAME = "buffalo_l"     # Model name
DEVICE = "cpu"               # cpu or cuda
CAM_INDEX = 1                # Camera index
WIDTH = 1280                 # Camera width
HEIGHT = 720                 # Camera height
DET_SIZE = 640               # Detection size
MIN_DET_SCORE = 0.6          # Min detection confidence
SAMPLES = 10                 # Enrollment samples
THRESHOLD = 0.35             # Recognition threshold
```

## 📊 File Sizes

| File/Folder | Size | Description |
|-------------|------|-------------|
| models/buffalo_l/ | ~340MB | ONNX models |
| face_db/embeddings.npy | ~2KB per face | Face embeddings |
| face_db/labels.json | ~50B per face | Labels |
| face_db/snapshots/ | ~100KB per sample | JPEG images |
| main.py | ~7KB | Main script |
| facegate_insightface.py | ~13KB | Core library |

## 🎯 Key Features by File

| Feature | File | Description |
|---------|------|-------------|
| Interactive Menu | main.py | User-friendly CLI |
| Face Detection | facegate_insightface.py | RetinaFace detector |
| Face Recognition | facegate_insightface.py | ArcFace embeddings |
| Database Management | facegate_insightface.py | FaceDB class |
| Camera Switch | main.py | Dynamic camera selection |
| Camera Preview | main.py | Test camera before use |
| Database Reset | reset_db.py | Safe database cleanup |
| Model Loading | facegate_insightface.py | Local model support |

## 📝 Notes

- **Portability**: Semua file bisa di-copy ke komputer lain
- **Backup**: Backup folder `face_db/` untuk preserve data
- **Model**: Model di folder `models/` tidak perlu re-download
- **Database**: Format NumPy + JSON mudah di-manipulasi
- **Snapshots**: Optional, bisa dinonaktifkan untuk save space
