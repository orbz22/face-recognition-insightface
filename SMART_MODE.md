# Smart Mode (Adaptive) Face Recognition

Panduan lengkap untuk Smart Mode - adaptive multi-face recognition.

## 🧠 **What is Smart Mode?**

Smart Mode adalah **adaptive algorithm** yang otomatis menyesuaikan jumlah wajah yang diproses berdasarkan kondisi real-time.

**Goal:** Balance antara **performance** dan **functionality**

---

## ⚡ **How It Works:**

### **Adaptive Logic:**

```python
if num_faces == 1:
    # FAST MODE
    Process: 1 face
    Reason: Single person, fastest path
    
elif num_faces <= 3:
    # ALL MODE
    Process: ALL faces (2-3)
    Reason: Parent + child scenario
    
else:  # num_faces >= 4
    # TOP3 MODE
    Process: Top 3 largest faces
    Reason: Performance balance
```

---

## 📊 **Mode Details:**

### **1. FAST Mode (1 Face)**

**Trigger:** Exactly 1 face detected

**Behavior:**
- Process immediately
- No sorting needed
- Fastest path

**Performance:**
- Inference: ~30ms
- FPS: 25-30
- CPU: 40-50%

**Use Case:**
- Single person verification
- One-on-one scenarios
- Access control

**Display:**
```
Mode: FAST (1/1)
```

---

### **2. ALL Mode (2-3 Faces)**

**Trigger:** 2 or 3 faces detected

**Behavior:**
- Process ALL detected faces
- No face left behind
- Perfect for parent + child

**Performance:**
- 2 faces: ~60ms, 12-15 FPS
- 3 faces: ~90ms, 8-10 FPS
- CPU: 50-70%

**Use Case:**
- Parent + child pickup
- Small group verification
- Family scenarios

**Display:**
```
Mode: ALL (2/2)  ← Processing all 2 faces
Mode: ALL (3/3)  ← Processing all 3 faces
```

---

### **3. TOP3 Mode (4+ Faces)**

**Trigger:** 4 or more faces detected

**Behavior:**
- Sort faces by size (largest first)
- Process top 3 largest
- Ignore smaller/background faces

**Performance:**
- Always ~90ms (3 faces)
- FPS: 8-10 (consistent)
- CPU: 60-70%

**Use Case:**
- Busy entrance
- Crowded scenarios
- Performance critical

**Display:**
```
Mode: TOP3 (3/5)  ← Processing 3 out of 5 faces
Mode: TOP3 (3/7)  ← Processing 3 out of 7 faces
```

---

## 🎯 **Scenarios:**

### **Scenario 1: Single Parent**

```
Detected: 1 face
Mode: FAST
Processed: 1 face
Result: Budi_Andi_3A | sim=0.87
Performance: Excellent (30 FPS)
```

---

### **Scenario 2: Parent + Child**

```
Detected: 2 faces
Mode: ALL
Processed: 2 faces
Result:
  - Budi_Andi_3A | sim=0.87 (Parent)
  - Unknown | sim=0.25 (Child)
Performance: Good (15 FPS)
```

---

### **Scenario 3: Parent + 2 Children**

```
Detected: 3 faces
Mode: ALL
Processed: 3 faces
Result:
  - Budi_Andi_3A | sim=0.87 (Parent)
  - Andi | sim=0.82 (Child 1)
  - Unknown | sim=0.28 (Child 2)
Performance: Acceptable (10 FPS)
```

---

### **Scenario 4: Crowded Entrance**

```
Detected: 7 faces
Mode: TOP3
Processed: 3 largest faces
Result:
  - Budi_Andi_3A | sim=0.87
  - Siti_Rina_2B | sim=0.92
  - Unknown | sim=0.30
Ignored: 4 smaller/background faces
Performance: Stable (10 FPS)
```

---

## 📈 **Performance Comparison:**

| Scenario | Faces Detected | Faces Processed | Mode | Inference | FPS |
|----------|----------------|-----------------|------|-----------|-----|
| Single person | 1 | 1 | FAST | ~30ms | 25-30 |
| Parent + child | 2 | 2 | ALL | ~60ms | 12-15 |
| Small group | 3 | 3 | ALL | ~90ms | 8-10 |
| Medium crowd | 5 | 3 | TOP3 | ~90ms | 8-10 |
| Large crowd | 10 | 3 | TOP3 | ~90ms | 8-10 |

**Key Insight:** TOP3 mode keeps performance **stable** even with many faces!

---

## 🎨 **Visual Display:**

### **FAST Mode (1 Face):**
```
┌─────────────────────────────────────┐
│                  Mode: FAST (1/1)   │
│                                     │
│   ┌──────────────┐                 │
│   │ Budi_Andi_3A │                 │
│   │ sim=0.87     │                 │
│   └──────────────┘                 │
│                                     │
│ FPS: 28.5 | Frame: 35ms | ...      │
└─────────────────────────────────────┘
```

### **ALL Mode (2 Faces):**
```
┌─────────────────────────────────────┐
│                   Mode: ALL (2/2)   │
│                                     │
│   ┌──────────────┐                 │
│   │ Budi_Andi_3A │                 │
│   │ sim=0.87     │                 │
│   └──────────────┘                 │
│              ┌─────────┐           │
│              │ Unknown │           │
│              │ sim=0.25│           │
│              └─────────┘           │
│                                     │
│ FPS: 15.3 | Frame: 65ms | ...      │
└─────────────────────────────────────┘
```

### **TOP3 Mode (5 Faces, 3 Processed):**
```
┌─────────────────────────────────────┐
│                  Mode: TOP3 (3/5)   │ ← 3 processed, 5 detected
│                                     │
│   ┌──────────────┐                 │
│   │ Budi_Andi_3A │  ← Largest      │
│   │ sim=0.87     │                 │
│   └──────────────┘                 │
│              ┌──────────────┐      │
│              │ Siti_Rina_2B │      │
│              │ sim=0.92     │      │
│              └──────────────┘      │
│   ┌─────────┐                      │
│   │ Unknown │  ← 3rd largest       │
│   │ sim=0.30│                      │
│   └─────────┘                      │
│                                     │
│   [2 smaller faces not processed]  │
│                                     │
│ FPS: 10.2 | Frame: 98ms | ...      │
└─────────────────────────────────────┘
```

---

## 🔧 **Configuration:**

### **Current Settings:**

```python
# facegate_insightface.py

# SMART MODE THRESHOLDS
SINGLE_FACE_THRESHOLD = 1      # 1 face = FAST mode
ALL_FACES_THRESHOLD = 3        # ≤3 faces = ALL mode
TOP_N_FACES = 3                # 4+ faces = TOP3 mode
```

### **Customization:**

#### **Option 1: Adjust ALL mode threshold**
```python
# Process all faces up to 5 (instead of 3)
elif num_faces <= 5:  # Change from 3 to 5
    faces_to_process = faces
    mode_text = "ALL"
```

**Effect:** More faces in ALL mode, but lower FPS

---

#### **Option 2: Adjust TOP N**
```python
# Process top 5 faces (instead of 3)
faces_to_process = faces_sorted[:5]  # Change from 3 to 5
mode_text = "TOP5"
```

**Effect:** More faces processed in crowded scenes, but lower FPS

---

#### **Option 3: Add size filter**
```python
# Only process faces larger than 80x80 pixels
MIN_FACE_SIZE = 80

faces_filtered = [f for f in faces 
                  if (f.bbox[2]-f.bbox[0]) >= MIN_FACE_SIZE 
                  and (f.bbox[3]-f.bbox[1]) >= MIN_FACE_SIZE]
```

**Effect:** Ignore small/distant faces

---

## 📊 **Statistics & Monitoring:**

### **Track Mode Usage:**

```python
mode_stats = {
    'FAST': 0,   # Single face count
    'ALL': 0,    # 2-3 faces count
    'TOP3': 0    # 4+ faces count
}

# In recognition loop
if mode_text == 'FAST':
    mode_stats['FAST'] += 1
elif mode_text == 'ALL':
    mode_stats['ALL'] += 1
elif mode_text == 'TOP3':
    mode_stats['TOP3'] += 1
```

**Useful for:**
- Understanding usage patterns
- Optimizing thresholds
- Capacity planning

---

## 🎯 **Best Practices:**

### **1. Monitor Performance**
- Watch FPS in different scenarios
- Adjust thresholds if needed
- Balance accuracy vs speed

### **2. Optimize for Common Case**
- If mostly single person → Current settings perfect
- If mostly groups → Increase ALL threshold
- If very crowded → Reduce TOP N

### **3. Test Edge Cases**
- Test with 1, 2, 3, 5, 10 faces
- Verify mode switching
- Check performance stability

### **4. User Feedback**
- Clear mode indicator
- Show processed/detected count
- Performance overlay

---

## ✅ **Advantages:**

1. **Automatic Adaptation**
   - No manual configuration needed
   - Adjusts to real-time conditions
   - Smart performance management

2. **Performance Stability**
   - FPS never drops below ~8-10
   - Predictable behavior
   - No system overload

3. **Functionality Balance**
   - Single person: Maximum speed
   - Small group: Full coverage
   - Large crowd: Focus on main subjects

4. **Resource Efficient**
   - Process only what's needed
   - Ignore background faces
   - Optimal CPU usage

---

## 🚀 **Future Enhancements:**

### **Planned Features:**

1. **Dynamic Thresholds**
   - Adjust based on CPU usage
   - Adapt to system load
   - Real-time optimization

2. **Face Tracking**
   - Track faces across frames
   - Reduce re-recognition
   - Smoother experience

3. **Priority System**
   - Prioritize known faces
   - Focus on main subjects
   - Ignore background people

4. **Machine Learning**
   - Learn optimal thresholds
   - Predict mode based on time/location
   - Adaptive to usage patterns

---

## 📝 **Summary:**

**Smart Mode = Intelligent + Adaptive + Efficient**

| Mode | Trigger | Processed | Performance | Use Case |
|------|---------|-----------|-------------|----------|
| **FAST** | 1 face | 1 | Excellent | Single person |
| **ALL** | 2-3 faces | All | Good | Parent + child |
| **TOP3** | 4+ faces | Top 3 | Stable | Crowded |

**Key Benefits:**
- ✅ Automatic adaptation
- ✅ Performance stability
- ✅ Optimal resource usage
- ✅ Best user experience

---

**Enjoy Smart Mode!** 🧠⚡
