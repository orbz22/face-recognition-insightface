# Performance Monitoring Guide

Panduan lengkap untuk monitoring performa Face Recognition System.

## 📊 Features

Performance Monitor track metrics berikut:

- **FPS (Frames Per Second)** - Kecepatan processing frame
- **Frame Time** - Waktu processing per frame (ms)
- **Inference Time** - Waktu face detection & recognition (ms)
- **CPU Usage** - Penggunaan CPU (%)
- **Memory Usage** - Penggunaan RAM (MB dan %)
- **Uptime** - Waktu program berjalan

---

## 🚀 Usage

### Automatic (Default)

Performance monitoring **otomatis aktif** saat menjalankan recognition mode:

```bash
python main.py
# Pilih Menu 2 (Recognize)
```

**On-screen display:**
- Performance stats ditampilkan di bottom screen
- Format: `FPS: 25.3 | Frame: 39.5ms | Inference: 28.2ms | CPU: 45.2% | RAM: 512MB`

**Keyboard controls:**
- `p` - Toggle performance overlay (show/hide)
- `q` - Quit recognition

**Exit summary:**
- Saat keluar, akan tampil performance summary lengkap

---

## 📈 Metrics Explained

### 1. FPS (Frames Per Second)

**What:** Jumlah frame yang diproses per detik

**Good values:**
- ✅ **25-30 FPS** - Excellent (smooth)
- ⚠️ **15-25 FPS** - Good (acceptable)
- ❌ **<15 FPS** - Poor (laggy)

**How to improve:**
- Reduce camera resolution
- Reduce detection size
- Increase frame skip
- Use GPU instead of CPU

---

### 2. Frame Time

**What:** Waktu total untuk process 1 frame (ms)

**Good values:**
- ✅ **<40ms** - Excellent (>25 FPS)
- ⚠️ **40-65ms** - Good (15-25 FPS)
- ❌ **>65ms** - Poor (<15 FPS)

**Components:**
- Inference time (face detection + recognition)
- Drawing/display time
- Other processing

---

### 3. Inference Time

**What:** Waktu untuk face detection + recognition (ms)

**Good values:**
- ✅ **<30ms** - Excellent
- ⚠️ **30-50ms** - Good
- ❌ **>50ms** - Poor

**Factors:**
- Detection size (320 vs 640)
- Camera resolution
- Number of faces in database
- CPU speed

---

### 4. CPU Usage

**What:** Persentase CPU yang digunakan program

**Good values:**
- ✅ **30-60%** - Normal
- ⚠️ **60-80%** - High (might affect other apps)
- ❌ **>80%** - Very high (system slow)

**Note:** 
- CPU usage varies with activity
- Higher during inference
- Lower during idle frames (frame skipping)

---

### 5. Memory Usage

**What:** RAM yang digunakan program (MB)

**Typical values:**
- Model loaded: ~300-500 MB
- During recognition: ~400-600 MB
- With large database: ~500-800 MB

**Warning signs:**
- ⚠️ Continuously increasing (memory leak?)
- ❌ >1GB (check for issues)

---

## 🔧 Performance Tuning

### Scenario 1: Low FPS / High Lag

**Problem:** FPS < 15, Frame time > 65ms

**Solutions:**

1. **Reduce camera resolution:**
   ```python
   # main.py, line ~205
   WIDTH = 320   # Lower from 640
   HEIGHT = 240  # Lower from 480
   ```

2. **Reduce detection size:**
   ```python
   # main.py, line ~207
   DET_SIZE = 160  # Lower from 320
   ```

3. **Increase frame skip:**
   ```python
   # facegate_insightface.py, line ~395
   if frame_count % 5 == 0:  # Change from 3 to 5
   ```

4. **Use GPU (if available):**
   ```python
   # main.py, line ~203
   DEVICE = "cuda"  # Change from "cpu"
   ```

---

### Scenario 2: High CPU Usage

**Problem:** CPU > 80%

**Solutions:**

1. **Increase frame skip** (process less frames)
2. **Reduce resolution** (less pixels to process)
3. **Close other applications**
4. **Use lighter model** (if available)

---

### Scenario 3: High Memory Usage

**Problem:** Memory > 1GB or continuously increasing

**Solutions:**

1. **Restart program** (clear memory)
2. **Reduce database size** (if very large)
3. **Check for memory leaks** (report issue)

---

## 📊 Benchmark Results

### Typical Performance (CPU Mode)

**System:** Intel i5, 8GB RAM, 640x480 resolution

| Metric | Value |
|--------|-------|
| FPS | 25-30 |
| Frame Time | 35-40 ms |
| Inference Time | 25-30 ms |
| CPU Usage | 40-50% |
| Memory | 450-550 MB |

**System:** Intel i3, 4GB RAM, 320x240 resolution

| Metric | Value |
|--------|-------|
| FPS | 20-25 |
| Frame Time | 40-50 ms |
| Inference Time | 30-40 ms |
| CPU Usage | 60-70% |
| Memory | 400-500 MB |

---

## 🛠️ Advanced Usage

### Programmatic Access

```python
from performance_monitor import PerformanceMonitor

# Create monitor
monitor = PerformanceMonitor()

# In your loop
monitor.start_frame()

# ... your processing ...

monitor.end_frame()

# Record inference time
monitor.record_inference_time(inference_time)

# Get stats
stats = monitor.get_stats()
print(f"FPS: {stats['fps']}")
print(f"CPU: {stats['cpu_percent']}%")
print(f"Memory: {stats['memory_mb']} MB")

# Print summary
monitor.print_stats()
```

---

### Logging Performance

```python
from performance_monitor import PerformanceMonitor, PerformanceLogger

monitor = PerformanceMonitor()
logger = PerformanceLogger("logs/performance.log")

# In your loop
monitor.start_frame()
# ... processing ...
monitor.end_frame()

# Log every 30 frames
if frame_count % 30 == 0:
    logger.log(monitor)
```

**Output:** CSV file dengan timestamp dan metrics

---

## 📝 Performance Log Format

**File:** `logs/performance.log`

**Format:** CSV
```csv
timestamp,fps,frame_ms,inference_ms,cpu_percent,memory_mb,memory_percent
2025-12-16 19:30:00,28.5,35.1,26.3,45.2,512.3,6.4
2025-12-16 19:30:01,29.1,34.4,25.8,44.8,513.1,6.4
...
```

**Analysis:**
- Import ke Excel/Google Sheets
- Create charts untuk visualisasi
- Track performance over time
- Identify bottlenecks

---

## 🎯 Optimization Checklist

- [ ] Check FPS (target: >20)
- [ ] Check frame time (target: <50ms)
- [ ] Check inference time (target: <40ms)
- [ ] Check CPU usage (target: <70%)
- [ ] Check memory usage (stable, <800MB)
- [ ] Adjust resolution if needed
- [ ] Adjust detection size if needed
- [ ] Adjust frame skip if needed
- [ ] Test on target hardware
- [ ] Monitor for extended period

---

## 🐛 Troubleshooting

### Performance overlay not showing

**Cause:** psutil not installed

**Solution:**
```bash
pip install psutil
```

### Stats show 0 FPS

**Cause:** No frames processed yet

**Solution:** Wait a few seconds for stats to accumulate

### Memory continuously increasing

**Cause:** Possible memory leak

**Solution:** 
1. Restart program
2. Update to latest version
3. Report issue if persists

---

## 📚 Related Files

- `performance_monitor.py` - Performance monitoring module
- `facegate_insightface.py` - Recognition with monitoring
- `requirements.txt` - Dependencies (includes psutil)

---

## 🎓 Best Practices

1. **Monitor during development** - Catch performance issues early
2. **Test on target hardware** - Performance varies by system
3. **Log performance** - Track over time
4. **Optimize iteratively** - Small changes, measure impact
5. **Balance accuracy vs speed** - Find sweet spot
6. **Document settings** - Note what works best

---

**Happy Monitoring!** 📊🚀
