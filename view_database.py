#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script untuk melihat dan mengelola database dengan format:
NamaOrtu_NamaAnak_Kelas
"""

import os
import json
import numpy as np
from typing import List, Dict


def parse_label(label: str) -> Dict[str, str]:
    """Parse label format: NamaOrtu_NamaAnak_Kelas"""
    parts = label.split('_')
    
    if len(parts) >= 3:
        return {
            'parent': parts[0],
            'child': parts[1],
            'class': parts[2],
            'full': label
        }
    else:
        # Fallback untuk format lama
        return {
            'parent': label,
            'child': '-',
            'class': '-',
            'full': label
        }


def view_database():
    """Tampilkan isi database dalam format tabel"""
    db_dir = "face_db"
    label_path = os.path.join(db_dir, "labels.json")
    emb_path = os.path.join(db_dir, "embeddings.npy")
    
    if not os.path.exists(label_path):
        print("\n[X] Database tidak ditemukan!")
        print(f"    File: {label_path}")
        return
    
    # Load labels
    with open(label_path, 'r', encoding='utf-8') as f:
        labels = json.load(f)
    
    # Load embeddings
    if os.path.exists(emb_path):
        embeddings = np.load(emb_path)
        total_emb = embeddings.shape[0]
    else:
        total_emb = 0
    
    # Display
    print("\n" + "="*80)
    print("  DATABASE WAJAH ORANG TUA - FACE RECOGNITION SYSTEM")
    print("="*80)
    print(f"Total Terdaftar: {len(labels)} orang")
    print(f"Total Embeddings: {total_emb}")
    print("="*80)
    
    if len(labels) == 0:
        print("\n[!] Database kosong. Belum ada yang terdaftar.")
        return
    
    # Header tabel
    print(f"\n{'No':<4} {'Nama Orang Tua':<25} {'Nama Anak':<25} {'Kelas':<10}")
    print("-" * 80)
    
    # Data
    for i, label in enumerate(labels, 1):
        parsed = parse_label(label)
        print(f"{i:<4} {parsed['parent']:<25} {parsed['child']:<25} {parsed['class']:<10}")
    
    print("="*80)


def search_by_child(child_name: str):
    """Cari orang tua berdasarkan nama anak"""
    db_dir = "face_db"
    label_path = os.path.join(db_dir, "labels.json")
    
    if not os.path.exists(label_path):
        print("\n[X] Database tidak ditemukan!")
        return
    
    with open(label_path, 'r', encoding='utf-8') as f:
        labels = json.load(f)
    
    print(f"\n[*] Mencari anak dengan nama: {child_name}")
    print("="*80)
    
    found = []
    for i, label in enumerate(labels):
        parsed = parse_label(label)
        if child_name.lower() in parsed['child'].lower():
            found.append((i+1, parsed))
    
    if found:
        print(f"\nDitemukan {len(found)} hasil:\n")
        print(f"{'No':<4} {'Nama Orang Tua':<25} {'Nama Anak':<25} {'Kelas':<10}")
        print("-" * 80)
        for idx, parsed in found:
            print(f"{idx:<4} {parsed['parent']:<25} {parsed['child']:<25} {parsed['class']:<10}")
    else:
        print(f"\n[!] Tidak ditemukan anak dengan nama: {child_name}")


def search_by_class(class_name: str):
    """Cari berdasarkan kelas"""
    db_dir = "face_db"
    label_path = os.path.join(db_dir, "labels.json")
    
    if not os.path.exists(label_path):
        print("\n[X] Database tidak ditemukan!")
        return
    
    with open(label_path, 'r', encoding='utf-8') as f:
        labels = json.load(f)
    
    print(f"\n[*] Mencari kelas: {class_name}")
    print("="*80)
    
    found = []
    for i, label in enumerate(labels):
        parsed = parse_label(label)
        if class_name.lower() in parsed['class'].lower():
            found.append((i+1, parsed))
    
    if found:
        print(f"\nDitemukan {len(found)} orang tua di kelas {class_name}:\n")
        print(f"{'No':<4} {'Nama Orang Tua':<25} {'Nama Anak':<25} {'Kelas':<10}")
        print("-" * 80)
        for idx, parsed in found:
            print(f"{idx:<4} {parsed['parent']:<25} {parsed['child']:<25} {parsed['class']:<10}")
    else:
        print(f"\n[!] Tidak ditemukan data untuk kelas: {class_name}")


def export_to_csv():
    """Export database ke CSV"""
    import csv
    
    db_dir = "face_db"
    label_path = os.path.join(db_dir, "labels.json")
    
    if not os.path.exists(label_path):
        print("\n[X] Database tidak ditemukan!")
        return
    
    with open(label_path, 'r', encoding='utf-8') as f:
        labels = json.load(f)
    
    output_file = "database_export.csv"
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['No', 'Nama Orang Tua', 'Nama Anak', 'Kelas', 'Label Lengkap'])
        
        for i, label in enumerate(labels, 1):
            parsed = parse_label(label)
            writer.writerow([i, parsed['parent'], parsed['child'], parsed['class'], parsed['full']])
    
    print(f"\n[OK] Database berhasil di-export ke: {output_file}")
    print(f"     Total: {len(labels)} records")


def main():
    """Main menu"""
    while True:
        print("\n" + "="*80)
        print("  DATABASE VIEWER - Face Recognition System")
        print("="*80)
        print("1. Lihat Semua Data")
        print("2. Cari Berdasarkan Nama Anak")
        print("3. Cari Berdasarkan Kelas")
        print("4. Export ke CSV")
        print("5. Keluar")
        print("="*80)
        
        choice = input("\nPilih (1-5): ").strip()
        
        if choice == "1":
            view_database()
        elif choice == "2":
            child_name = input("\nMasukkan nama anak: ").strip()
            if child_name:
                search_by_child(child_name)
        elif choice == "3":
            class_name = input("\nMasukkan kelas (contoh: 3A): ").strip()
            if class_name:
                search_by_class(class_name)
        elif choice == "4":
            export_to_csv()
        elif choice == "5":
            print("\nKeluar...")
            break
        else:
            print("\n[X] Pilihan tidak valid!")
        
        input("\nTekan ENTER untuk kembali...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nKeluar...")
    except Exception as e:
        print(f"\n[X] Error: {e}")
