# Logging System - Face Recognition

Sistem logging lengkap untuk tracking semua aktivitas face recognition.

## 📁 Log Files

Semua log disimpan di folder `logs/`:

```
logs/
├── system.log        # System events (startup, shutdown, errors)
├── enrollment.log    # Enrollment events
├── recognition.log   # Recognition events
└── access.log        # Access control events
```

## 📝 Log Format

Format log: `TIMESTAMP | LEVEL | MESSAGE`

Example:
```
2025-12-15 21:45:56 | INFO | System started | Model: buffalo_l | Device: cpu | Camera: 1
```

## 🎯 Log Types

### 1. System Log (`system.log`)
Mencatat event sistem:
- System startup/shutdown
- Model loading
- Camera switches
- Errors

**Example:**
```
2025-12-15 21:00:00 | INFO | System started | Model: buffalo_l | Device: cpu | Camera: 1
2025-12-15 21:05:30 | INFO | CAMERA_SWITCH | From: 1 | To: 0
2025-12-15 21:10:00 | INFO | System shutdown
```

### 2. Enrollment Log (`enrollment.log`)
Mencatat proses enrollment:
- Enrollment success/failed
- Nama orang
- Jumlah samples
- Camera yang digunakan

**Example:**
```
2025-12-15 21:02:00 | INFO | ENROLL | SUCCESS | Name: Alice | Samples: 10 | Camera: 1
2025-12-15 21:05:00 | INFO | ENROLL | FAILED | Name: Bob | Samples: 0 | Camera: 1 | Notes: No samples collected
```

### 3. Recognition Log (`recognition.log`)
Mencatat hasil recognition:
- Nama yang terdeteksi
- Similarity score
- Threshold
- Camera

**Example:**
```
2025-12-15 21:10:00 | INFO | RECOGNIZE | RECOGNIZED | Name: Alice | Similarity: 0.856 | Threshold: 0.35 | Camera: 1
2025-12-15 21:10:05 | INFO | RECOGNIZE | UNKNOWN | Similarity: 0.245 | Threshold: 0.35 | Camera: 1
```

### 4. Access Log (`access.log`)
Mencatat access control (jika digunakan):
- Access granted/denied
- Nama
- Alasan (jika ditolak)

**Example:**
```
2025-12-15 21:15:00 | INFO | ACCESS | GRANTED | Name: Alice
2025-12-15 21:15:30 | INFO | ACCESS | DENIED | Name: Unknown | Reason: Not in database
```

## 🔍 Viewing Logs

### Opsi 1: Menggunakan view_logs.py (Recommended)

```bash
python view_logs.py
```

Menu interaktif dengan fitur:
- View log files
- Show statistics
- Filter by time
- Export data

### Opsi 2: Manual

```bash
# View system log
cat logs/system.log

# View last 10 lines
tail -n 10 logs/enrollment.log

# View in real-time
tail -f logs/recognition.log

# Windows PowerShell
Get-Content logs\system.log -Tail 10
Get-Content logs\recognition.log -Wait
```

## 📊 Statistics

### Enrollment Statistics

```python
from logger import get_logger

logger = get_logger()
stats = logger.get_enrollment_stats()

print(f"Total: {stats['total']}")
print(f"Success: {stats['success']}")
print(f"Names: {stats['names']}")
```

### Recognition Statistics

```python
from logger import get_logger

logger = get_logger()
stats = logger.get_recognition_stats(hours=24)  # Last 24 hours

print(f"Total: {stats['total']}")
print(f"Recognized: {stats['recognized']}")
print(f"Unknown: {stats['unknown']}")
print(f"Unique faces: {stats['unique_faces']}")
```

## 🛠️ Custom Logging

### Dalam Code Anda

```python
from logger import get_logger

logger = get_logger()

# Log system event
logger.log_system("Custom event", level="INFO")

# Log enrollment
logger.log_enrollment("John", samples=10, success=True, camera_index=1)

# Log recognition
logger.log_recognition("John", similarity=0.85, camera_index=1, threshold=0.35)

# Log access
logger.log_access("John", granted=True)

# Log error
logger.log_error("CustomError", "Error message", context="my_function")
```

## 📈 Log Analysis

### Enrollment Success Rate

```bash
# Count successful enrollments
grep "SUCCESS" logs/enrollment.log | wc -l

# Count failed enrollments
grep "FAILED" logs/enrollment.log | wc -l
```

### Recognition Rate

```bash
# Count recognized faces
grep "RECOGNIZED" logs/recognition.log | wc -l

# Count unknown faces
grep "UNKNOWN" logs/recognition.log | wc -l
```

### Most Recognized Person

```bash
# Extract names and count
grep "RECOGNIZED" logs/recognition.log | grep -o "Name: [^|]*" | sort | uniq -c | sort -rn
```

## 🔄 Log Rotation

Log files akan terus bertambah. Untuk menghindari file terlalu besar:

### Manual Rotation

```bash
# Backup dan clear logs
mkdir logs/backup
mv logs/*.log logs/backup/
# Logs akan dibuat ulang otomatis
```

### Automated Rotation (Linux/macOS)

Tambahkan ke crontab:
```bash
# Rotate logs setiap minggu
0 0 * * 0 cd /path/to/project && mkdir -p logs/backup/$(date +\%Y\%m\%d) && mv logs/*.log logs/backup/$(date +\%Y\%m\%d)/
```

## 🔒 Privacy & Security

**PENTING:**
- Log files berisi informasi pribadi (nama, waktu akses)
- **JANGAN** commit log files ke git (sudah ada di `.gitignore`)
- Backup logs secara terpisah
- Hapus logs lama secara berkala

## 📝 Log Levels

- **INFO**: Normal operations
- **WARNING**: Perhatian diperlukan (database reset, dll)
- **ERROR**: Error yang terjadi
- **DEBUG**: Debugging information (tidak digunakan secara default)

## 🎯 Use Cases

### 1. Audit Trail
Track siapa saja yang sudah di-enroll dan kapan:
```bash
grep "ENROLL | SUCCESS" logs/enrollment.log
```

### 2. Attendance Tracking
Lihat siapa saja yang terdeteksi hari ini:
```bash
grep "$(date +%Y-%m-%d)" logs/recognition.log | grep "RECOGNIZED"
```

### 3. System Monitoring
Monitor errors dan warnings:
```bash
grep "ERROR\|WARNING" logs/system.log
```

### 4. Performance Analysis
Analisis similarity scores untuk tuning threshold:
```bash
grep "Similarity:" logs/recognition.log | grep -o "Similarity: [0-9.]*"
```

## 📦 Export Logs

### To CSV

```python
import csv
from datetime import datetime

# Parse enrollment log to CSV
with open('logs/enrollment.log', 'r') as f_in:
    with open('enrollment_export.csv', 'w', newline='') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(['Timestamp', 'Status', 'Name', 'Samples', 'Camera'])
        
        for line in f_in:
            # Parse log line
            # ... (implement parsing logic)
            pass
```

## 🔧 Troubleshooting

**Log files tidak dibuat?**
- Pastikan folder `logs/` ada (dibuat otomatis)
- Check permissions

**Log files terlalu besar?**
- Implement log rotation
- Hapus logs lama

**Tidak bisa membaca logs?**
- Check encoding (UTF-8)
- Gunakan `view_logs.py`

## 📚 References

- Python logging: https://docs.python.org/3/library/logging.html
- Log analysis tools: grep, awk, sed
- Log rotation: logrotate (Linux)
