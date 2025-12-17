# 3.X Entity Relationship Diagram (ERD)

## 3.X.1 Pendahuluan

Entity Relationship Diagram (ERD) merupakan representasi visual dari struktur basis data yang digunakan dalam sistem face recognition untuk verifikasi orang tua siswa. ERD ini menggambarkan entitas-entitas yang terlibat, atribut-atributnya, serta relasi antar entitas dalam sistem.

Sistem ini menggunakan SQLite sebagai database management system (DBMS) untuk menyimpan data siswa dan orang tua, serta file eksternal (NumPy array dan PNG) untuk menyimpan data face embeddings dan QR codes.

## 3.X.2 Entitas dalam Sistem

Sistem ini terdiri dari 4 (empat) entitas utama:

### 3.X.2.1 Entitas Students

Entitas **students** menyimpan data master siswa yang terdaftar di sekolah.

**Tabel 3.X: Struktur Tabel Students**

| Atribut | Tipe Data | Constraint | Keterangan |
|---------|-----------|------------|------------|
| nis | VARCHAR | PRIMARY KEY | Nomor Induk Siswa (unique identifier) |
| nama | VARCHAR | NOT NULL | Nama lengkap siswa |
| kelas | VARCHAR | NOT NULL | Kelas siswa (contoh: 1B, 3A, TK-A) |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Waktu pendaftaran siswa |

**Fungsi:** Menyimpan informasi dasar siswa yang menjadi referensi utama untuk enrollment orang tua.

### 3.X.2.2 Entitas Parents

Entitas **parents** menyimpan data orang tua yang telah melakukan enrollment wajah.

**Tabel 3.X: Struktur Tabel Parents**

| Atribut | Tipe Data | Constraint | Keterangan |
|---------|-----------|------------|------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | ID unik untuk setiap enrollment |
| nis | VARCHAR | NOT NULL, FOREIGN KEY | Referensi ke tabel students |
| nama_ortu | VARCHAR | NOT NULL | Nama lengkap orang tua/wali |
| embedding_index | INTEGER | NOT NULL, UNIQUE | Index di file embeddings.npy |
| enrolled_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Waktu enrollment wajah |

**Fungsi:** Menghubungkan data orang tua dengan siswa dan face embedding mereka.

**Index:**
- `idx_parents_nis`: Index pada kolom nis untuk mempercepat pencarian berdasarkan NIS
- `idx_parents_embedding`: Index pada kolom embedding_index untuk mempercepat pencarian berdasarkan embedding

### 3.X.2.3 Entitas Face Embeddings

Entitas **face_embeddings** merepresentasikan data face embeddings yang disimpan dalam file eksternal.

**Tabel 3.X: Struktur Face Embeddings**

| Atribut | Tipe Data | Keterangan |
|---------|-----------|------------|
| index | INTEGER (PRIMARY KEY) | Index array (0, 1, 2, ...) |
| embedding | FLOAT ARRAY[512] | Vector embedding wajah 512 dimensi |

**Storage:** File `face_db/embeddings.npy` (NumPy array format)

**Fungsi:** Menyimpan representasi numerik wajah hasil ekstraksi dari model ArcFace ResNet50.

### 3.X.2.4 Entitas QR Codes

Entitas **qr_codes** merepresentasikan QR codes yang di-generate untuk setiap enrollment.

**Tabel 3.X: Struktur QR Codes**

| Atribut | Tipe Data | Keterangan |
|---------|-----------|------------|
| nis | VARCHAR (PRIMARY KEY) | NIS siswa (format filename: NIS.png) |
| qr_content | VARCHAR | Konten QR (format: hash:nis) |

**Storage:** File `qr_codes/*.png`

**Fungsi:** Menyediakan metode verifikasi backup menggunakan QR code yang berisi NIS terenkripsi.

**Catatan:** Satu QR code per siswa (bukan per orang tua). Semua orang tua dari siswa yang sama menggunakan QR code yang sama.

## 3.X.3 Relasi Antar Entitas

### 3.X.3.1 Relasi Students - Parents

**Jenis Relasi:** One-to-Many (1:N)

**Penjelasan:** Satu siswa dapat memiliki beberapa orang tua yang terdaftar (ayah, ibu, wali, dll), namun setiap data enrollment orang tua hanya terhubung ke satu siswa.

**Implementasi:** Foreign key `nis` pada tabel parents yang mereferensi primary key `nis` pada tabel students.

**Constraint:**
- ON DELETE: CASCADE (jika siswa dihapus, data orang tua ikut terhapus)
- ON UPDATE: CASCADE (jika NIS diupdate, referensi ikut terupdate)

### 3.X.3.2 Relasi Parents - Face Embeddings

**Jenis Relasi:** One-to-One (1:1)

**Penjelasan:** Setiap enrollment orang tua memiliki tepat satu face embedding, dan setiap face embedding hanya dimiliki oleh satu orang tua.

**Implementasi:** Kolom `embedding_index` pada tabel parents yang mereferensi index pada file embeddings.npy.

**Karakteristik:**
- Unique constraint pada embedding_index memastikan tidak ada duplikasi
- Index digunakan sebagai foreign key logis ke array embeddings

### 3.X.3.3 Relasi Students - QR Codes

**Jenis Relasi:** One-to-One (1:1)

**Penjelasan:** Setiap siswa memiliki tepat satu QR code, dan setiap QR code hanya terhubung ke satu siswa. QR code ini dapat digunakan oleh semua orang tua dari siswa tersebut.

**Implementasi:** Kolom `nis` pada tabel qr_codes yang mereferensi primary key `nis` pada tabel students.

**Karakteristik:**
- Primary key pada qr_codes.nis memastikan hanya satu QR per siswa
- Filename format: `{NIS}.png` (contoh: `111.png`)
- QR code di-generate pada enrollment pertama untuk siswa tersebut
- Enrollment berikutnya untuk siswa yang sama menggunakan QR yang sudah ada

## 3.X.4 Diagram ERD

Berikut adalah Entity Relationship Diagram sistem face recognition:

```
┌─────────────────────┐
│     students        │
│─────────────────────│
│ nis (PK)            │◄────────┐
│ nama                │         │
│ kelas               │         │ 1
│ created_at          │         │
└─────────────────────┘         │
                                │
                                │ N
                    ┌───────────┴──────────────────┐
                    │                              │
                    │ N                            │ 1:1
        ┌───────────▼────────┐        ┌────────────▼──────┐
        │      parents       │        │    qr_codes       │
        │────────────────────│        │───────────────────│
        │ id (PK)            │        │ nis (PK)          │
        │ nis (FK)           │        │ qr_content        │
        │ nama_ortu          │        └───────────────────┘
        │ embedding_index    │
        │ enrolled_at        │
        └────────┬───────────┘
                 │
                 │ 1:1
                 │
        ┌────────▼────────────┐
        │  face_embeddings    │
        │─────────────────────│
        │ index (PK)          │
        │ embedding[512]      │
        └─────────────────────┘
```

**Gambar 3.X: Entity Relationship Diagram Sistem Face Recognition**

*Catatan: Diagram di atas dapat di-generate menggunakan tool dbdiagram.io dengan kode DBML yang tersedia di file `database_erd.dbml`*

## 3.X.5 Penjelasan Alur Data

### 3.X.5.1 Alur Enrollment

1. Admin menambahkan data siswa ke tabel **students** (NIS, nama, kelas)
2. Orang tua melakukan enrollment wajah:
   - Input: NIS siswa + Nama orang tua
   - System lookup data siswa dari tabel **students**
   - Capture wajah → Extract embedding (512-D vector)
   - Simpan embedding ke **face_embeddings** (embeddings.npy) → dapat index
   - Simpan data orang tua ke tabel **parents** dengan embedding_index
   - Generate QR code dengan NIS terenkripsi → simpan ke **qr_codes** (hanya jika belum ada)

### 3.X.5.2 Alur Recognition

1. System detect wajah → Extract embedding
2. Matching dengan semua embeddings di **face_embeddings**
3. Jika match (similarity ≥ threshold):
   - Dapatkan embedding_index
   - Lookup tabel **parents** berdasarkan embedding_index
   - Dapatkan NIS dari parents
   - Lookup tabel **students** berdasarkan NIS
   - Display: "Ortu: [Nama Ortu] | Anak: [Nama Anak] ([Kelas])"

### 3.X.5.3 Alur QR Code Verification

1. Scan QR code → Dapatkan encrypted NIS
2. Decrypt → Dapatkan NIS plaintext
3. Verify hash untuk keamanan
4. Lookup tabel **students** berdasarkan NIS
5. Lookup tabel **parents** berdasarkan NIS
6. Display informasi lengkap orang tua dan siswa

## 3.X.6 Normalisasi Database

Database sistem ini telah menerapkan normalisasi hingga **Third Normal Form (3NF)**:

### 3.X.6.1 First Normal Form (1NF)
- ✅ Setiap kolom berisi nilai atomic (tidak ada multi-value)
- ✅ Setiap baris unik (ada primary key)
- ✅ Tidak ada repeating groups

### 3.X.6.2 Second Normal Form (2NF)
- ✅ Memenuhi 1NF
- ✅ Tidak ada partial dependency (semua non-key attributes fully dependent pada primary key)

### 3.X.6.3 Third Normal Form (3NF)
- ✅ Memenuhi 2NF
- ✅ Tidak ada transitive dependency
- ✅ Data siswa terpisah dari data orang tua (menghindari redundansi)

## 3.X.7 Integritas Data

### 3.X.7.1 Entity Integrity
- Setiap tabel memiliki primary key yang unik dan not null
- Primary key: students.nis, parents.id, face_embeddings.index, qr_codes.nis

### 3.X.7.2 Referential Integrity
- Foreign key parents.nis → students.nis dengan constraint CASCADE
- Logical foreign key parents.embedding_index → face_embeddings.index
- Logical foreign key qr_codes.nis → students.nis

### 3.X.7.3 Domain Integrity
- Constraint NOT NULL pada field-field penting
- Constraint UNIQUE pada embedding_index (mencegah duplikasi)
- Default value CURRENT_TIMESTAMP untuk tracking waktu

## 3.X.8 Keunggulan Desain Database

1. **Single Source of Truth**: Data siswa hanya disimpan di satu tempat (tabel students), menghindari redundansi dan inkonsistensi

2. **Scalability**: Struktur relasional memudahkan penambahan data baru tanpa mengubah struktur

3. **Flexibility**: Mudah untuk menambahkan field baru atau relasi baru sesuai kebutuhan

4. **Performance**: Index pada kolom yang sering di-query (nis, embedding_index) meningkatkan kecepatan pencarian

5. **Data Integrity**: Foreign key constraints memastikan konsistensi data antar tabel

6. **Separation of Concerns**: Data metadata (SQLite) terpisah dari data binary (NumPy array, PNG files)

## 3.X.9 Kesimpulan

Entity Relationship Diagram yang telah dirancang memberikan struktur database yang solid, terorganisir, dan efisien untuk sistem face recognition. Desain ini memenuhi prinsip-prinsip normalisasi database, menjaga integritas data, dan mendukung operasi CRUD (Create, Read, Update, Delete) dengan performa optimal.

Penggunaan kombinasi SQLite untuk metadata dan file eksternal untuk data binary (embeddings, QR codes) memberikan keseimbangan antara kemudahan query dan efisiensi storage, sesuai dengan best practices dalam pengembangan sistem face recognition.

---

**Referensi:**
- Elmasri, R., & Navathe, S. B. (2015). *Fundamentals of Database Systems* (7th ed.). Pearson.
- Date, C. J. (2003). *An Introduction to Database Systems* (8th ed.). Addison-Wesley.
- Connolly, T., & Begg, C. (2014). *Database Systems: A Practical Approach to Design, Implementation, and Management* (6th ed.). Pearson.
