"""
Initialize database dengan data siswa
"""

from student_database import StudentDatabase

# Create database
db = StudentDatabase("students.db")

# Add student: Majid, NIS: 111, Kelas: 1B
print("Adding student...")
success = db.add_student("111", "Majid", "1B")

if success:
    print("[OK] Student added successfully!")
    print("\nStudent data:")
    student = db.get_student("111")
    print(f"  NIS: {student['nis']}")
    print(f"  Nama: {student['nama']}")
    print(f"  Kelas: {student['kelas']}")
else:
    print("[X] Failed to add student (may already exist)")

print("\nAll students in database:")
for s in db.list_all_students():
    print(f"  {s['nis']} - {s['nama']} ({s['kelas']})")

