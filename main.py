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

# Initialize logger
logger = get_logger()


def print_menu(cam_index):
    print("\n" + "="*50)
    print("  FACE RECOGNITION SYSTEM - InsightFace")
    print("="*50)
    print("1. Enroll (Daftarkan wajah baru)")
    print("2. Recognize (Kenali wajah)")
    print(f"3. Switch Camera (Saat ini: Camera {cam_index})")
    print("4. Exit")
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


def main():
    # Konfigurasi default
    DB_DIR = "face_db"
    MODEL_NAME = "buffalo_l"  # buffalo_l untuk akurasi lebih baik
    DEVICE = "cpu"  # ganti ke "cuda" jika punya GPU
    CAM_INDEX = 1  # Camera index 1 (bisa diubah via menu)
    WIDTH = 1280
    HEIGHT = 720
    DET_SIZE = 640
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
            # Enroll mode
            print("\n[*] ENROLLMENT - Pendaftaran Wajah Orang Tua")
            print("="*50)
            
            # Input data lengkap
            parent_name = input("Nama Orang Tua: ").strip()
            if not parent_name:
                print("[X] Nama orang tua tidak boleh kosong!")
                continue
            
            child_name = input("Nama Anak: ").strip()
            if not child_name:
                print("[X] Nama anak tidak boleh kosong!")
                continue
            
            child_class = input("Kelas Anak (contoh: 3A, 5B): ").strip()
            if not child_class:
                print("[X] Kelas anak tidak boleh kosong!")
                continue
            
            # Format: NamaOrtu_NamaAnak_Kelas
            full_label = f"{parent_name}_{child_name}_{child_class}"
            
            print(f"\n[*] Data yang akan didaftarkan:")
            print(f"   Nama Orang Tua: {parent_name}")
            print(f"   Nama Anak: {child_name}")
            print(f"   Kelas: {child_class}")
            print(f"   Label Database: {full_label}")
            
            confirm = input("\nApakah data sudah benar? (y/n): ").strip().lower()
            if confirm != 'y':
                print("[!] Pendaftaran dibatalkan.")
                continue
            
            print(f"\n[*] Mode Enroll untuk: {parent_name}")
            print("   Instruksi:")
            print("   - Arahkan wajah ke kamera")
            print("   - Tekan 'c' untuk capture sample")
            print("   - Tekan 'q' untuk selesai/batal")
            print(f"   - Target: {SAMPLES} samples")
            print(f"   - Camera: {CAM_INDEX}\n")
            
            input("Tekan ENTER untuk mulai...")
            
            enroll_mode(
                app=app,
                db=db,
                name=full_label,
                cam_index=CAM_INDEX,
                width=WIDTH,
                height=HEIGHT,
                samples=SAMPLES,
                min_det_score=MIN_DET_SCORE,
                save_snapshots=True
            )
        
        elif choice == "2":
            # Recognize mode
            print("\n[*] Mode Recognize")
            print("   Instruksi:")
            print("   - Arahkan wajah ke kamera")
            print("   - Sistem akan otomatis mengenali wajah")
            print("   - Tekan 'q' untuk keluar")
            print(f"   - Camera: {CAM_INDEX}\n")
            
            input("Tekan ENTER untuk mulai...")
            
            recognize_mode(
                app=app,
                db=db,
                cam_index=CAM_INDEX,
                width=WIDTH,
                height=HEIGHT,
                threshold=THRESHOLD,
                min_det_score=MIN_DET_SCORE
            )
        
        elif choice == "3":
            # Switch Camera
            old_index = CAM_INDEX
            CAM_INDEX = switch_camera(CAM_INDEX)
            if old_index != CAM_INDEX:
                logger.log_camera_switch(old_index, CAM_INDEX)
        
        elif choice == "4":
            print("\n[*] Terima kasih! Keluar dari program...")
            logger.log_system("System shutdown")
            sys.exit(0)
        
        else:
            print("\n[X] Pilihan tidak valid! Silakan pilih 1-4.")


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
