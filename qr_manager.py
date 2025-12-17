#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QR Code Module untuk Face Recognition System
Generate dan scan QR code dengan enkripsi
"""

import os
import json
import qrcode
import cv2
from cryptography.fernet import Fernet
from pyzbar.pyzbar import decode
from typing import Optional, Dict
import base64
import hashlib


class QRCodeManager:
    """Manager untuk generate dan scan QR code dengan enkripsi"""
    
    def __init__(self, db_dir: str = "face_db", qr_dir: str = "qr_codes"):
        """
        Initialize QR Code Manager
        
        Args:
            db_dir: Directory database
            qr_dir: Directory untuk menyimpan QR codes
        """
        self.db_dir = db_dir
        self.qr_dir = qr_dir
        self.key_file = os.path.join(db_dir, ".qr_key")
        
        os.makedirs(qr_dir, exist_ok=True)
        
        # Load atau generate encryption key
        self.cipher = self._load_or_create_key()
    
    def _load_or_create_key(self) -> Fernet:
        """Load encryption key atau buat baru jika belum ada"""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                key = f.read()
        else:
            # Generate key baru
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            print(f"[*] Encryption key created: {self.key_file}")
        
        # Store key for SHA256 hashing
        self.key = key
        
        return Fernet(key)
    
    def _generate_id(self, label: str, index: int) -> str:
        """
        Generate unique ID untuk label
        Format: HASH(label + index)
        """
        data = f"{label}_{index}".encode()
        hash_obj = hashlib.sha256(data)
        return hash_obj.hexdigest()[:16]  # 16 char ID
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt data dan return base64 string"""
        encrypted = self.cipher.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt_data(self, encrypted_data: str) -> Optional[str]:
        """Decrypt data dari base64 string"""
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted = self.cipher.decrypt(encrypted_bytes)
            return decrypted.decode()
        except Exception as e:
            print(f"[X] Decryption error: {e}")
            return None
    
    def generate_qr_for_all(self) -> int:
        """
        Generate QR code untuk semua orang di database
        
        Returns:
            Jumlah QR code yang di-generate
        """
        label_path = os.path.join(self.db_dir, "labels.json")
        
        if not os.path.exists(label_path):
            print("[X] Database tidak ditemukan!")
            return 0
        
        with open(label_path, 'r', encoding='utf-8') as f:
            labels = json.load(f)
        
        if not labels:
            print("[!] Database kosong!")
            return 0
        
        print(f"\n[*] Generating QR codes untuk {len(labels)} orang...")
        
        count = 0
        for idx, label in enumerate(labels):
            success = self.generate_qr_code(label, idx)
            if success:
                count += 1
        
        print(f"\n[OK] {count} QR codes berhasil di-generate!")
        print(f"     Lokasi: {self.qr_dir}/")
        
        return count
    
    
    def generate_qr_code(self, nis: str, silent: bool = False) -> bool:
        """
        Generate QR code untuk satu siswa (1 QR per student)
        
        Args:
            nis: NIS siswa
            silent: Jika True, tidak print message
        
        Returns:
            True jika berhasil
        """
        try:
            # OPTIMIZED: Use SHA256 hash (fixed 64 chars, much shorter than Fernet)
            # Hash NIS with secret key for security
            import hashlib
            
            # Combine NIS with secret key
            secret = self.key.decode() if isinstance(self.key, bytes) else str(self.key)
            combined = f"{nis}:{secret}"
            
            # Generate SHA256 hash (64 hex characters)
            hash_obj = hashlib.sha256(combined.encode())
            qr_data = hash_obj.hexdigest()  # 64 characters (vs 100+ with Fernet)
            
            # Format: hash:nis
            qr_content = f"{qr_data[:16]}:{nis}"  # Use first 16 chars of hash + NIS
            
            # Generate QR code dengan setting OPTIMAL untuk kamera low-res
            qr = qrcode.QRCode(
                version=1,  # Versi terkecil (21x21 modules)
                error_correction=qrcode.constants.ERROR_CORRECT_L,  # Low = paling simple
                box_size=30,  # Box besar untuk scan mudah
                border=2,     # Border minimal
            )
            qr.add_data(qr_content)
            qr.make(fit=True)
            
            # Create image dengan ukuran besar
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Filename: NIS.png (simple, one per student)
            filename = f"{nis}.png"
            
            filepath = os.path.join(self.qr_dir, filename)
            img.save(filepath)
            
            if not silent:
                print(f"[OK] QR code generated: {filename}")
                print(f"     NIS: {nis}")
                print(f"     Data: Hash + NIS ({len(qr_content)} chars)")
            
            return True
            
        except Exception as e:
            if not silent:
                print(f"[X] Error generating QR code for NIS {nis}: {e}")
            return False
    
    def scan_qr_from_camera(self, cam_index: int = 0, width: int = 640, height: int = 480) -> Optional[Dict]:
        """
        Scan QR code dari kamera
        
        Args:
            cam_index: Index kamera
            width: Lebar frame
            height: Tinggi frame
        
        Returns:
            Dict dengan info jika berhasil, None jika gagal
        """
        cap = cv2.VideoCapture(cam_index)
        if not cap.isOpened():
            print(f"[X] Tidak bisa membuka camera {cam_index}")
            return None
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
        print("\n[*] QR CODE SCANNER")
        print("    Arahkan QR code ke kamera")
        print("    Tekan 'q' untuk keluar\n")
        
        result = None
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Decode QR codes
            decoded_objects = decode(frame)
            
            for obj in decoded_objects:
                # Get QR data (hash:nis format)
                qr_data = obj.data.decode('utf-8')
                
                try:
                    # QR format: hash:nis
                    if ':' in qr_data:
                        hash_part, nis = qr_data.split(':', 1)
                        
                        # Verify hash (optional - for extra security)
                        import hashlib
                        secret = self.key.decode() if isinstance(self.key, bytes) else str(self.key)
                        combined = f"{nis}:{secret}"
                        expected_hash = hashlib.sha256(combined.encode()).hexdigest()[:16]
                        
                        if hash_part == expected_hash:
                            # Valid QR code
                            data = {
                                'nis': nis,
                                'raw_data': qr_data,
                                'verified': True
                            }
                        else:
                            # Hash mismatch - possible tampering
                            data = {
                                'nis': nis,
                                'raw_data': qr_data,
                                'verified': False
                            }
                    else:
                        # Old format (plain NIS) - still support
                        nis = qr_data.strip()
                        data = {
                            'nis': nis,
                            'raw_data': qr_data,
                            'verified': False  # No hash to verify
                        }
                    
                    # Draw rectangle around QR code
                    points = obj.polygon
                    if len(points) == 4:
                        pts = [(point.x, point.y) for point in points]
                        cv2.polylines(frame, [np.array(pts, dtype=np.int32)], True, (0, 255, 0), 3)
                    
                    # Display info
                    cv2.putText(frame, "QR Code Detected!", (10, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame, f"NIS: {data['nis']}", (10, 60),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    
                    result = data
                    
                except Exception as e:
                    cv2.putText(frame, "Invalid QR Code", (10, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            # Display
            cv2.imshow("QR Code Scanner - Press 'q' to quit", frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or result is not None:
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        return result
    
    def verify_qr_data(self, data: Dict) -> bool:
        """
        Verify QR code data dengan database
        
        Args:
            data: Data dari QR code
        
        Returns:
            True jika valid
        """
        label_path = os.path.join(self.db_dir, "labels.json")
        
        if not os.path.exists(label_path):
            return False
        
        with open(label_path, 'r', encoding='utf-8') as f:
            labels = json.load(f)
        
        # Check index
        if data['index'] >= len(labels):
            return False
        
        # Check label match
        if labels[data['index']] != data['label']:
            return False
        
        # Verify ID
        expected_id = self._generate_id(data['label'], data['index'])
        if data['id'] != expected_id:
            return False
        
        return True


# Import numpy untuk QR detection
import numpy as np


if __name__ == "__main__":
    # Test
    qr_manager = QRCodeManager()
    
    print("QR Code Manager Test")
    print("1. Generate QR codes")
    print("2. Scan QR code")
    
    choice = input("\nPilih (1/2): ").strip()
    
    if choice == "1":
        qr_manager.generate_qr_for_all()
    elif choice == "2":
        result = qr_manager.scan_qr_from_camera()
        if result:
            print(f"\n[OK] QR Code scanned successfully!")
            print(f"     Label: {result['label']}")
            print(f"     Index: {result['index']}")
            print(f"     ID: {result['id']}")
            
            if qr_manager.verify_qr_data(result):
                print(f"     Status: VALID ✓")
            else:
                print(f"     Status: INVALID ✗")
