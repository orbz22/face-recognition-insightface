# Folder ini berisi database wajah terdaftar

File-file di folder ini tidak di-commit ke git karena berisi data pribadi.

## Struktur

```
face_db/
├── embeddings.npy    # Face embeddings (tidak di-commit)
├── labels.json       # Nama/label (tidak di-commit)
└── snapshots/        # Foto snapshot (tidak di-commit)
```

## Cara Menggunakan

1. Jalankan program: `python main.py`
2. Pilih menu 1 untuk enroll wajah
3. Database akan otomatis dibuat di folder ini
