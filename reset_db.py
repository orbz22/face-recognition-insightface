#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script untuk reset/clear database face recognition
"""

import os
import shutil

DB_DIR = "face_db"

def reset_database():
    """Hapus semua data di database dan reset ke kondisi awal"""
    
    print("\n[!] WARNING: Ini akan menghapus SEMUA data face recognition!")
    print(f"   Folder: {DB_DIR}")
    
    confirm = input("\nKetik 'YES' untuk konfirmasi: ").strip()
    
    if confirm != "YES":
        print("[X] Reset dibatalkan.")
        return
    
    # Hapus embeddings.npy
    emb_path = os.path.join(DB_DIR, "embeddings.npy")
    if os.path.exists(emb_path):
        os.remove(emb_path)
        print(f"[OK] Deleted: {emb_path}")
    
    # Reset labels.json ke array kosong
    label_path = os.path.join(DB_DIR, "labels.json")
    with open(label_path, "w", encoding="utf-8") as f:
        f.write("[]")
    print(f"[OK] Reset: {label_path}")
    
    # Hapus snapshots
    snap_dir = os.path.join(DB_DIR, "snapshots")
    if os.path.exists(snap_dir):
        shutil.rmtree(snap_dir)
        print(f"[OK] Deleted: {snap_dir}")
    
    print("\n[OK] Database berhasil di-reset!")
    print("   Silakan jalankan enroll lagi untuk mendaftarkan wajah.\n")


if __name__ == "__main__":
    reset_database()
