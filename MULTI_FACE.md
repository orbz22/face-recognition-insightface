# Multi-Face Recognition Guide

Panduan lengkap untuk fitur multi-face recognition.

## 🎯 Overview

Sistem sekarang bisa **recognize MULTIPLE faces** dalam 1 frame secara bersamaan!

**Before:**
- ✅ Detect multiple faces
- ❌ Recognize only 1 face (largest)

**After:**
- ✅ Detect multiple faces
- ✅ **Recognize ALL faces** simultaneously

---

## 🚀 Features

### 1. **Simultaneous Recognition**
- Process semua wajah yang terdeteksi dalam 1 frame
- Setiap wajah di-recognize secara independent
- Bounding box untuk setiap wajah

### 2. **Face Count Indicator**
- Display jumlah wajah yang terdeteksi
- Posisi: Top-right corner
- Format: `Faces: N`

### 3. **Individual Labels**
- Setiap wajah punya label sendiri
- Format: `Name | sim=0.XX`
- Color-coded boxes (future enhancement)

---

## 📊 Use Cases

### **Scenario 1: Parent + Child Verification**

**Before:**
```
Frame: Parent dan Child masuk
Result: Hanya Parent recognized (wajah terbesar)
Issue: Child tidak ter-verify
```

**After:**
```
Frame: Parent dan Child masuk
Result: 
  - Parent: Budi_Andi_3A | sim=0.87
  - Child: Unknown | sim=0.25
Status: Parent verified, Child unknown
```

---

### **Scenario 2: Multiple Parents Pickup**

**Before:**
```
Frame: 3 parents waiting
Result: Hanya 1 parent recognized
Issue: Others tidak ter-verify
```

**After:**
```
Frame: 3 parents waiting
Result:
  - Parent 1: Budi_Andi_3A | sim=0.89
  - Parent 2: Siti_Rina_2B | sim=0.92
  - Parent 3: Unknown | sim=0.28
Status: 2 verified, 1 unknown
```

---

### **Scenario 3: Group Attendance**

**Before:**
```
Frame: 5 students
Result: Hanya 1 student recognized
Issue: Manual check untuk others
```

**After:**
```
Frame: 5 students
Result:
  - Student 1: Andi_Budi_3A | sim=0.91
  - Student 2: Rina_Siti_2B | sim=0.88
  - Student 3: Riko_Andi_1C | sim=0.85
  - Student 4: Unknown | sim=0.30
  - Student 5: Unknown | sim=0.25
Status: 3 verified, 2 unknown
```

---

## 🎨 Visual Display

### **On-Screen Elements:**

```
┌─────────────────────────────────────────┐
│                          Faces: 3       │ ← Face count
│                                         │
│   ┌──────────────┐                     │
│   │ Budi_Andi_3A │                     │ ← Face 1
│   │ sim=0.87     │                     │
│   └──────────────┘                     │
│                                         │
│              ┌──────────┐              │
│              │ Unknown  │              │ ← Face 2
│              │ sim=0.25 │              │
│              └──────────┘              │
│                                         │
│   ┌──────────────┐                     │
│   │ Siti_Rina_2B │                     │ ← Face 3
│   │ sim=0.92     │                     │
│   └──────────────┘                     │
│                                         │
│ FPS: 25.3 | Frame: 39.5ms | ...       │ ← Performance
└─────────────────────────────────────────┘
```

---

## ⚡ Performance Impact

### **Inference Time Scaling:**

| Faces | Inference Time | FPS Impact |
|-------|----------------|------------|
| 1 face | ~30ms | Baseline (25-30 FPS) |
| 2 faces | ~60ms | -50% (12-15 FPS) |
| 3 faces | ~90ms | -66% (8-10 FPS) |
| 4 faces | ~120ms | -75% (6-8 FPS) |
| 5 faces | ~150ms | -80% (5-6 FPS) |

**Note:** Linear scaling - N faces = N × inference time

---

### **Performance Tips:**

#### **If FPS too low with multiple faces:**

1. **Reduce frame skip:**
   ```python
   # facegate_insightface.py, line ~421
   if frame_count % 5 == 0:  # Change from 3 to 5
   ```

2. **Reduce resolution:**
   ```python
   # main.py, line ~205
   WIDTH = 320   # Lower from 640
   HEIGHT = 240  # Lower from 480
   ```

3. **Reduce detection size:**
   ```python
   # main.py, line ~207
   DET_SIZE = 160  # Lower from 320
   ```

4. **Limit max faces (future):**
   ```python
   # Process only top 3 faces
   faces_sorted = sorted(faces, key=lambda f: area(f), reverse=True)
   faces_to_process = faces_sorted[:3]
   ```

---

## 📝 Logging

### **Multiple Face Logging:**

**Before:**
```
2025-12-16 10:30:00 | RECOGNITION | Budi_Andi_3A | 0.87 | Camera: 1
```

**After (multiple entries per frame):**
```
2025-12-16 10:30:00 | RECOGNITION | Budi_Andi_3A | 0.87 | Camera: 1
2025-12-16 10:30:00 | RECOGNITION | Unknown | 0.25 | Camera: 1
2025-12-16 10:30:00 | RECOGNITION | Siti_Rina_2B | 0.92 | Camera: 1
```

**Note:** Setiap wajah di-log secara terpisah dengan timestamp yang sama

---

## 🔧 Configuration

### **Current Settings:**

```python
# facegate_insightface.py
def recognize_mode(...):
    # Process ALL detected faces
    for face in faces:
        if float(face.det_score) >= min_det_score:
            # Recognize this face
            ...
```

### **Customization Options:**

#### **Option 1: Limit Max Faces**
```python
MAX_FACES = 3  # Process max 3 faces

faces_to_process = faces[:MAX_FACES] if len(faces) > MAX_FACES else faces
```

#### **Option 2: Confidence Threshold**
```python
MIN_DET_SCORE = 0.7  # Higher = more strict

for face in faces:
    if float(face.det_score) >= MIN_DET_SCORE:
        # Only process high-confidence faces
```

#### **Option 3: Size Filter**
```python
MIN_FACE_SIZE = 50  # Minimum face size (pixels)

for face in faces:
    width = face.bbox[2] - face.bbox[0]
    height = face.bbox[3] - face.bbox[1]
    
    if width >= MIN_FACE_SIZE and height >= MIN_FACE_SIZE:
        # Only process large enough faces
```

---

## 🎯 Best Practices

### **1. Database Organization**

**For parent-child verification:**
```
Database entries:
- Budi_Andi_3A (Parent)
- Andi (Child) ← Optional: enroll child separately
```

**Benefits:**
- Verify both parent and child
- Extra security layer
- Track who picks up

---

### **2. Threshold Tuning**

**For multiple faces:**
```python
THRESHOLD = 0.40  # Slightly higher than single face (0.35)
```

**Reason:**
- More faces = more chance of false positives
- Higher threshold = more strict
- Better accuracy

---

### **3. Performance Monitoring**

**Watch these metrics:**
- FPS should stay >15 for usability
- Inference time per face should be <40ms
- CPU usage should be <80%

**If performance poor:**
- Reduce resolution
- Increase frame skip
- Limit max faces

---

## 📊 Statistics

### **Face Count Distribution:**

Monitor how many faces typically appear:

```python
# Add to performance log
face_count_stats = {
    1: 0,  # Single face frames
    2: 0,  # Two faces
    3: 0,  # Three faces
    # ...
}
```

**Useful for:**
- Optimize for common case
- Capacity planning
- Performance tuning

---

## 🚀 Future Enhancements

### **Planned Features:**

1. **Color-coded boxes:**
   - Green: Recognized
   - Red: Unknown
   - Yellow: Low confidence

2. **Face tracking:**
   - Track same face across frames
   - Reduce re-recognition
   - Smoother display

3. **Group verification:**
   - Verify parent-child pairs
   - Family group recognition
   - Access control logic

4. **Performance optimization:**
   - Batch inference (process multiple faces together)
   - GPU acceleration
   - Model quantization

---

## ✅ Testing Checklist

- [ ] Test with 1 face (should work as before)
- [ ] Test with 2 faces (both should be recognized)
- [ ] Test with 3+ faces (all should be recognized)
- [ ] Check FPS with multiple faces
- [ ] Verify logging (multiple entries per frame)
- [ ] Check face count indicator display
- [ ] Test with unknown faces
- [ ] Test with mix of known/unknown
- [ ] Monitor performance metrics
- [ ] Verify on target hardware

---

## 🎉 Summary

**What Changed:**
- ❌ Single face recognition (old)
- ✅ **Multi-face recognition (new)**

**Benefits:**
- ✅ Recognize multiple people simultaneously
- ✅ Better for group scenarios
- ✅ More comprehensive logging
- ✅ Face count indicator

**Trade-offs:**
- ⚠️ Lower FPS with many faces
- ⚠️ Higher CPU usage
- ⚠️ More log entries

**Overall:** **Much more powerful and flexible!** 🚀

---

**Enjoy multi-face recognition!** 👥✨
