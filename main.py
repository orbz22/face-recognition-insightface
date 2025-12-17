#!/usr/bin/env python3
"""
Main entry point untuk Face Recognition System
Simplified interface untuk enroll dan recognize
"""

import sys
import cv2
from facegate_insightface import (
    build_face_app,
    FaceDB,
    enroll_mode,
    recognize_mode,
    open_camera
)
from logger import get_logger

# Try to import QR manager (optional - may fail if DLLs missing)
try:
    from qr_manager import QRCodeManager
    QR_AVAILABLE = True
except Exception as e:
    print(f"[!] QR Code feature unavailable: {e}")
    print("    Program will continue without QR code support.")
    QR_AVAILABLE = False
    QRCodeManager = None

# Initialize logger
logger = get_logger()


def print_menu(cam_index):
    print("\n" + "="*50)
    print("  FACE RECOGNITION SYSTEM - InsightFace")
    print("="*50)
    print("1. Enroll (Daftarkan wajah baru)")
    print("2. Recognize (Kenali wajah)")
    print(f"3. Switch Camera (Saat ini: Camera {cam_index})")
    
    if QR_AVAILABLE:
        print("4. QR Code Menu")
    else:
        print("4. QR Code Menu (UNAVAILABLE - DLL missing)")
    
    print("5. Exit")
    print("="*50)


def test_camera(cam_index, width=640, height=480):
    """Test kamera untuk memastikan berfungsi"""
    print(f"\n[TEST CAMERA {cam_index}]")
    print("Tekan 'q' untuk keluar dari preview.\n")
    
    try:
        cap = open_camera(cam_index, width, height)
        print(f"Camera {cam_index} berhasil dibuka!")
        print("Menampilkan preview...\n")
        
        while True:
            ok, frame = cap.read()
            if not ok:
                print("Gagal membaca frame dari kamera.")
                break
            
            # Tampilkan info di frame
            cv2.putText(frame, f"Camera {cam_index} - Press 'q' to quit", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow(f"Camera {cam_index} Test", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        return True
        
    except Exception as e:
        print(f"[X] Error: Camera {cam_index} tidak dapat dibuka.")
        print(f"    Detail: {e}")
        return False


def switch_camera(current_index):
    """Menu untuk switch camera"""
    print("\n" + "="*50)
    print("  SWITCH CAMERA")
    print("="*50)
    print(f"Camera saat ini: {current_index}")
    print("\nPilihan:")
    print("1. Test camera saat ini")
    print("2. Ganti ke camera index lain")
    print("3. Kembali ke menu utama")
    print("="*50)
    
    choice = input("\nPilih (1-3): ").strip()
    
    if choice == "1":
        # Test camera saat ini
        test_camera(current_index)
        return current_index
        
    elif choice == "2":
        # Ganti camera index
        try:
            new_index = int(input("\nMasukkan camera index baru (0, 1, 2, ...): ").strip())
            
            # Test camera baru
            print(f"\nMencoba membuka camera {new_index}...")
            if test_camera(new_index):
                print(f"\n[OK] Camera {new_index} berfungsi dengan baik!")
                confirm = input(f"Gunakan camera {new_index}? (y/n): ").strip().lower()
                if confirm == 'y':
                    print(f"\n[OK] Camera diubah ke index {new_index}")
                    return new_index
                else:
                    print(f"\n[!] Tetap menggunakan camera {current_index}")
                    return current_index
            else:
                print(f"\n[X] Camera {new_index} tidak tersedia.")
                print(f"    Tetap menggunakan camera {current_index}")
                return current_index
                
        except ValueError:
            print("\n[X] Input tidak valid! Harus berupa angka.")
            return current_index
        except Exception as e:
            print(f"\n[X] Error: {e}")
            return current_index
    
    else:
        # Kembali ke menu utama
        return current_index


def qr_code_menu(cam_index: int):
    """Menu untuk QR Code operations"""
    qr_manager = QRCodeManager()
    
    while True:
        print("\n" + "="*50)
        print("  QR CODE MENU")
        print("="*50)
        print("1. Generate QR Codes untuk Semua")
        print("2. Scan QR Code")
        print("3. Kembali ke Menu Utama")
        print("="*50)
        
        choice = input("\nPilih (1-3): ").strip()
        
        if choice == "1":
            # Generate QR codes
            print("\n[*] Generating QR Codes...")
            count = qr_manager.generate_qr_for_all()
            
            if count > 0:
                print(f"\n[OK] {count} QR codes telah di-generate!")
                print(f"     Lokasi: qr_codes/")
                print("\n[!] QR codes ini bisa dicetak dan diberikan ke orang tua")
                print("    sebagai backup jika face recognition gagal.")
            
            input("\nTekan ENTER untuk kembali...")
        
        elif choice == "2":
            # Scan QR code
            print(f"\n[*] Membuka camera {cam_index} untuk scan QR code...")
            result = qr_manager.scan_qr_from_camera(cam_index=cam_index)
            
            if result:
                print(f"\n[OK] QR Code berhasil di-scan!")
                print(f"     Label: {result['label']}")
                
                # Parse label
                parts = result['label'].split('_')
                if len(parts) >= 3:
                    print(f"     Nama Ortu: {parts[0]}")
                    print(f"     Nama Anak: {parts[1]}")
                    print(f"     Kelas: {parts[2]}")
                
                # Verify
                if qr_manager.verify_qr_data(result):
                    print(f"     Status: VALID ✓")
                    logger.log_access(result['label'], granted=True, reason="QR Code scan")
                else:
                    print(f"     Status: INVALID ✗")
                    logger.log_access(result['label'], granted=False, reason="Invalid QR Code")
            else:
                print("\n[!] Tidak ada QR code yang ter-scan.")
            
            input("\nTekan ENTER untuk kembali...")
        
        elif choice == "3":
            break
        
        else:
            print("\n[X] Pilihan tidak valid!")


def main():
    # Konfigurasi default
    DB_DIR = "face_db"
    MODEL_NAME = "buffalo_l"  # buffalo_l untuk akurasi lebih baik
    DEVICE = "cpu"  # ganti ke "cuda" jika punya GPU
    CAM_INDEX = 1  # Camera index 1 (bisa diubah via menu)
    WIDTH = 640   # Reduced from 1280 for better performance
    HEIGHT = 480  # Reduced from 720 for better performance
    DET_SIZE = 320  # Reduced from 640 for faster detection
    MIN_DET_SCORE = 0.6
    SAMPLES = 10
    THRESHOLD = 0.35
    
    print("\n[*] Memuat model InsightFace...")
    print(f"   Model: {MODEL_NAME}")
    print(f"   Device: {DEVICE}")
    print(f"   Camera: {CAM_INDEX}")
    
    logger.log_system(f"System started | Model: {MODEL_NAME} | Device: {DEVICE} | Camera: {CAM_INDEX}")
    
    # Inisialisasi
    db = FaceDB(DB_DIR)
    
    try:
        app = build_face_app(model_name=MODEL_NAME, det_size=DET_SIZE, device=DEVICE)
        logger.log_model_load(MODEL_NAME, DEVICE, success=True)
        print("[OK] Model berhasil dimuat!\n")
    except Exception as e:
        logger.log_model_load(MODEL_NAME, DEVICE, success=False)
        logger.log_error("ModelLoadError", str(e))
        raise
    
    while True:
        print_menu(CAM_INDEX)
        choice = input(f"\nPilih menu (1-4): ").strip()
        
        if choice == "1":
            # Enroll mode with NIS
            print("\n[*] ENROLLMENT - Pendaftaran Wajah Orang Tua")
            print("="*50)
            
            # Input NIS
            nis = input("NIS Siswa: ").strip()
            if not nis:
                print("[X] NIS tidak boleh kosong!")
                continue
            
            # Lookup student dari database
            from student_database import StudentDatabase
            student_db = StudentDatabase("students.db")
            
            student = student_db.get_student(nis)
            if not student:
                print(f"[X] NIS '{nis}' tidak ditemukan di database!")
                print("    Silakan hubungi admin untuk menambahkan data siswa.")
                continue
            
            # Display student info
            print(f"\n[*] Data Siswa Ditemukan:")
            print(f"   NIS: {student['nis']}")
            print(f"   Nama: {student['nama']}")
            print(f"   Kelas: {student['kelas']}")
            
            # Input parent name
            parent_name = input("\nNama Orang Tua: ").strip()
            if not parent_name:
                print("[X] Nama orang tua tidak boleh kosong!")
                continue
            
            # Confirm
            print(f"\n[*] Data yang akan didaftarkan:")
            print(f"   Orang Tua: {parent_name}")
            print(f"   Anak: {student['nama']} (NIS: {nis})")
            print(f"   Kelas: {student['kelas']}")
            
            confirm = input("\nApakah data sudah benar? (y/n): ").strip().lower()
            if confirm != 'y':
                print("[!] Pendaftaran dibatalkan.")
                continue
            
            print(f"\n[*] Mode Enroll untuk: {parent_name}")
            print(f"   Anak: {student['nama']} ({student['kelas']})")
            print(f"   Instruksi:")
            print(f"   - Posisikan wajah di depan kamera")
            print(f"   - Tekan 'c' untuk capture (10x)")
            print(f"   - Tekan 'q' untuk batal")
            print(f"   - Camera: {CAM_INDEX}\n")
            
            input("Tekan ENTER untuk mulai...")
            
            try:
                # Get current embedding count (untuk index)
                embs, labels = db.load()
                embedding_index = embs.shape[0]  # Next index
                
                # Enroll face (using temporary label)
                temp_label = f"{parent_name}_{student['nama']}_{student['kelas']}"
                
                enroll_mode(
                    app=app,
                    db=db,
                    name=temp_label,
                    cam_index=CAM_INDEX,
                    width=WIDTH,
                    height=HEIGHT,
                    samples=SAMPLES,
                    min_det_score=MIN_DET_SCORE,
                    save_snapshots=True
                )
                
                # Save to student database
                student_db.add_parent(nis, parent_name, embedding_index)
                print(f"\n[OK] Data orang tua disimpan ke database!")
                
                # Generate QR code with NIS
                if QR_AVAILABLE:
                    try:
                        qr_manager.generate_qr_code(nis, parent_name, silent=False)
                    except Exception as e:
                        print(f"[!] QR generation error: {e}")
                
            except Exception as e:
                print(f"\n[X] Error saat enrollment: {e}")
                logger.log_error("EnrollmentError", str(e))
                input("\nTekan ENTER untuk kembali...")
        
        elif choice == "2":
            # Recognize mode
            print("\n[*] Mode Recognize")
            print("   Instruksi:")
            print("   - Arahkan wajah ke kamera")
            print("   - Sistem akan otomatis mengenali wajah")
            print("   - Tekan 'q' untuk keluar")
            print(f"   - Camera: {CAM_INDEX}\n")
            
            input("Tekan ENTER untuk mulai...")
            
            try:
                recognize_mode(
                    app=app,
                    db=db,
                    cam_index=CAM_INDEX,
                    width=WIDTH,
                    height=HEIGHT,
                    threshold=THRESHOLD,
                    min_det_score=MIN_DET_SCORE
                )
            except Exception as e:
                print(f"\n[X] Error saat recognition: {e}")
                logger.log_error("RecognitionError", str(e))
                input("\nTekan ENTER untuk kembali...")
        
        elif choice == "3":
            # Switch Camera
            old_index = CAM_INDEX
            CAM_INDEX = switch_camera(CAM_INDEX)
            if old_index != CAM_INDEX:
                logger.log_camera_switch(old_index, CAM_INDEX)
        
        elif choice == "4":
            # QR Code Menu
            if QR_AVAILABLE:
                qr_code_menu(CAM_INDEX)
            else:
                print("\n[X] QR Code feature tidak tersedia!")
                print("    Pyzbar DLL (libiconv.dll) tidak ditemukan.")
                print("    Program tetap bisa digunakan tanpa fitur QR code.")
                input("\nTekan ENTER untuk kembali...")
        
        elif choice == "5":
            print("\n[*] Terima kasih! Keluar dari program...")
            logger.log_system("System shutdown")
            sys.exit(0)
        
        else:
            print("\n[X] Pilihan tidak valid! Silakan pilih 1-5.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[*] Program dihentikan oleh user. Bye!")
        logger.log_system("System interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[X] Error: {e}")
        logger.log_error("SystemError", str(e), context="main")
        sys.exit(1)
