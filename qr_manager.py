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
    
    def generate_qr_code(self, label: str, index: int, silent: bool = False) -> bool:
        """
        Generate QR code untuk satu orang
        
        Args:
            label: Label dari database (NamaOrtu_NamaAnak_Kelas)
            index: Index di database
            silent: Jika True, tidak print message
        
        Returns:
            True jika berhasil
        """
        try:
            # SIMPLIFIED: Hanya simpan index (lebih kecil, lebih mudah di-scan)
            # Data minimal untuk QR code yang lebih sederhana
            data = str(index)  # Hanya index saja!
            
            # Encrypt (data sudah minimal)
            encrypted = self.encrypt_data(data)
            
            # Generate QR code dengan setting untuk kamera low-res
            qr = qrcode.QRCode(
                version=1,  # Versi terkecil
                error_correction=qrcode.constants.ERROR_CORRECT_L,  # Low error correction (lebih simple)
                box_size=20,  # DIPERBESAR dari 10 ke 20 (kotak lebih besar)
                border=2,     # Border dikurangi dari 4 ke 2
            )
            qr.add_data(encrypted)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save dengan nama yang aman
            safe_filename = label.replace('/', '_').replace('\\', '_')
            filename = f"{safe_filename}.png"
            filepath = os.path.join(self.qr_dir, filename)
            
            img.save(filepath)
            
            if not silent:
                print(f"  [OK] {label} -> {filename}")  # Changed arrow to ASCII
            return True
            
        except Exception as e:
            if not silent:
                print(f"  [X] Error generating QR for {label}: {e}")
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
                # Get encrypted data
                encrypted_data = obj.data.decode('utf-8')
                
                # Decrypt
                decrypted = self.decrypt_data(encrypted_data)
                
                if decrypted:
                    try:
                        # Data sekarang hanya index (string)
                        index = int(decrypted)
                        
                        # Load labels untuk get label dari index
                        label_path = os.path.join(self.db_dir, "labels.json")
                        if os.path.exists(label_path):
                            with open(label_path, 'r', encoding='utf-8') as f:
                                labels = json.load(f)
                            
                            if index < len(labels):
                                label = labels[index]
                                
                                # Prepare result
                                data = {
                                    'index': index,
                                    'label': label,
                                    'id': self._generate_id(label, index)
                                }
                                
                                # Draw rectangle around QR code
                                points = obj.polygon
                                if len(points) == 4:
                                    pts = [(point.x, point.y) for point in points]
                                    cv2.polylines(frame, [np.array(pts, dtype=np.int32)], True, (0, 255, 0), 3)
                                
                                # Display info
                                cv2.putText(frame, "QR Code Detected!", (10, 30),
                                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                                cv2.putText(frame, f"Label: {data['label']}", (10, 60),
                                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                                
                                result = data
                            else:
                                cv2.putText(frame, "Invalid Index", (10, 30),
                                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        
                    except (json.JSONDecodeError, ValueError):
                        cv2.putText(frame, "Invalid QR Code", (10, 30),
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                else:
                    cv2.putText(frame, "Decryption Failed", (10, 30),
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
