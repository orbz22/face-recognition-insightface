"""
Database Manager untuk Face Recognition System
Menggunakan SQLite untuk data siswa dan orang tua
"""

import sqlite3
import os
from typing import List, Tuple, Optional, Dict


class StudentDatabase:
    """Manage student database (NIS, Nama, Kelas)"""
    
    def __init__(self, db_path: str = "students.db"):
        """
        Initialize student database
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Create tables if not exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table: students (NIS, Nama, Kelas)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                nis TEXT PRIMARY KEY,
                nama TEXT NOT NULL,
                kelas TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table: parents (Link parent face to student)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nis TEXT NOT NULL,
                nama_ortu TEXT NOT NULL,
                embedding_index INTEGER NOT NULL,
                enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (nis) REFERENCES students(nis)
            )
        ''')
        
        # Index untuk faster lookup
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_parents_nis 
            ON parents(nis)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_parents_embedding 
            ON parents(embedding_index)
        ''')
        
        conn.commit()
        conn.close()
    
    def add_student(self, nis: str, nama: str, kelas: str) -> bool:
        """
        Add new student to database
        
        Args:
            nis: Nomor Induk Siswa
            nama: Nama siswa
            kelas: Kelas siswa
            
        Returns:
            True if success, False if already exists
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO students (nis, nama, kelas)
                VALUES (?, ?, ?)
            ''', (nis, nama, kelas))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.IntegrityError:
            # NIS already exists
            return False
    
    def get_student(self, nis: str) -> Optional[Dict[str, str]]:
        """
        Get student info by NIS
        
        Args:
            nis: Nomor Induk Siswa
            
        Returns:
            Dict with student info or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT nis, nama, kelas, created_at
            FROM students
            WHERE nis = ?
        ''', (nis,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'nis': row[0],
                'nama': row[1],
                'kelas': row[2],
                'created_at': row[3]
            }
        return None
    
    def add_parent(self, nis: str, nama_ortu: str, embedding_index: int) -> bool:
        """
        Add parent enrollment
        
        Args:
            nis: Student NIS
            nama_ortu: Parent name
            embedding_index: Index in embeddings.npy
            
        Returns:
            True if success
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO parents (nis, nama_ortu, embedding_index)
            VALUES (?, ?, ?)
        ''', (nis, nama_ortu, embedding_index))
        
        conn.commit()
        conn.close()
        return True
    
    def get_parent_by_index(self, embedding_index: int) -> Optional[Dict]:
        """
        Get parent and student info by embedding index
        
        Args:
            embedding_index: Index in embeddings.npy
            
        Returns:
            Dict with parent and student info
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.id, p.nis, p.nama_ortu, p.embedding_index,
                   s.nama, s.kelas
            FROM parents p
            JOIN students s ON p.nis = s.nis
            WHERE p.embedding_index = ?
        ''', (embedding_index,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'parent_id': row[0],
                'nis': row[1],
                'nama_ortu': row[2],
                'embedding_index': row[3],
                'nama_anak': row[4],
                'kelas': row[5]
            }
        return None
    
    def get_parent_by_nis(self, nis: str) -> Optional[Dict]:
        """
        Get parent info by student NIS
        
        Args:
            nis: Student NIS
            
        Returns:
            Dict with parent info
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.id, p.nis, p.nama_ortu, p.embedding_index,
                   s.nama, s.kelas
            FROM parents p
            JOIN students s ON p.nis = s.nis
            WHERE p.nis = ?
        ''', (nis,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'parent_id': row[0],
                'nis': row[1],
                'nama_ortu': row[2],
                'embedding_index': row[3],
                'nama_anak': row[4],
                'kelas': row[5]
            }
        return None
    
    def list_all_students(self) -> List[Dict]:
        """Get all students"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT nis, nama, kelas FROM students ORDER BY kelas, nama')
        rows = cursor.fetchall()
        conn.close()
        
        return [{'nis': r[0], 'nama': r[1], 'kelas': r[2]} for r in rows]
    
    def list_all_parents(self) -> List[Dict]:
        """Get all enrolled parents"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.id, p.nis, p.nama_ortu, s.nama, s.kelas
            FROM parents p
            JOIN students s ON p.nis = s.nis
            ORDER BY s.kelas, s.nama
        ''')
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            'parent_id': r[0],
            'nis': r[1],
            'nama_ortu': r[2],
            'nama_anak': r[3],
            'kelas': r[4]
        } for r in rows]
    
    def import_students_from_csv(self, csv_file: str) -> Tuple[int, int]:
        """
        Import students from CSV file
        
        CSV format: NIS,Nama,Kelas
        
        Args:
            csv_file: Path to CSV file
            
        Returns:
            (success_count, error_count)
        """
        import csv
        
        success = 0
        errors = 0
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            
            for row in reader:
                if len(row) >= 3:
                    nis, nama, kelas = row[0].strip(), row[1].strip(), row[2].strip()
                    if self.add_student(nis, nama, kelas):
                        success += 1
                    else:
                        errors += 1
        
        return success, errors
    
    def export_students_to_csv(self, csv_file: str) -> int:
        """
        Export students to CSV file
        
        Args:
            csv_file: Path to output CSV file
            
        Returns:
            Number of students exported
        """
        import csv
        
        students = self.list_all_students()
        
        with open(csv_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['NIS', 'Nama', 'Kelas'])
            
            for s in students:
                writer.writerow([s['nis'], s['nama'], s['kelas']])
        
        return len(students)


# Example usage and testing
if __name__ == "__main__":
    # Create database
    db = StudentDatabase("students.db")
    
    # Add sample students
    print("Adding sample students...")
    db.add_student("2024001", "Andi Pratama", "3A")
    db.add_student("2024002", "Rina Sari", "2B")
    db.add_student("2024003", "Riko Saputra", "1C")
    
    # Get student
    print("\nGet student by NIS:")
    student = db.get_student("2024001")
    print(student)
    
    # Add parent
    print("\nAdd parent enrollment:")
    db.add_parent("2024001", "Budi Santoso", 0)  # embedding_index = 0
    
    # Get parent by index
    print("\nGet parent by embedding index:")
    parent = db.get_parent_by_index(0)
    print(parent)
    
    # List all
    print("\nAll students:")
    for s in db.list_all_students():
        print(f"  {s['nis']} - {s['nama']} ({s['kelas']})")
    
    print("\nAll enrolled parents:")
    for p in db.list_all_parents():
        print(f"  {p['nama_ortu']} - Anak: {p['nama_anak']} ({p['kelas']})")
