#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script untuk melihat dan menganalisis log files
"""

import os
import sys
from logger import get_logger, FaceRecognitionLogger


def print_header(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def view_logs():
    """Menu untuk melihat berbagai log"""
    logger = FaceRecognitionLogger()
    
    while True:
        print_header("LOG VIEWER - Face Recognition System")
        print("1. View System Log")
        print("2. View Enrollment Log")
        print("3. View Recognition Log")
        print("4. View Access Log")
        print("5. Show Enrollment Statistics")
        print("6. Show Recognition Statistics (Last 24h)")
        print("7. Show All Statistics")
        print("8. Exit")
        print("="*60)
        
        choice = input("\nPilih (1-8): ").strip()
        
        if choice == "1":
            show_log_file("logs/system.log", "SYSTEM LOG")
        elif choice == "2":
            show_log_file("logs/enrollment.log", "ENROLLMENT LOG")
        elif choice == "3":
            show_log_file("logs/recognition.log", "RECOGNITION LOG")
        elif choice == "4":
            show_log_file("logs/access.log", "ACCESS LOG")
        elif choice == "5":
            show_enrollment_stats(logger)
        elif choice == "6":
            show_recognition_stats(logger, hours=24)
        elif choice == "7":
            show_all_stats(logger)
        elif choice == "8":
            print("\nExiting...")
            break
        else:
            print("\n[X] Pilihan tidak valid!")


def show_log_file(filepath, title):
    """Tampilkan isi log file"""
    print_header(title)
    
    if not os.path.exists(filepath):
        print(f"\n[!] Log file tidak ditemukan: {filepath}")
        print("    File akan dibuat saat ada aktivitas.")
        input("\nTekan ENTER untuk kembali...")
        return
    
    # Tanya jumlah baris
    print("\nBerapa baris terakhir yang ingin ditampilkan?")
    print("(Tekan ENTER untuk semua, atau masukkan angka)")
    lines_input = input("Jumlah baris: ").strip()
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            print("\n[!] Log file kosong.")
        else:
            if lines_input:
                n = int(lines_input)
                lines = lines[-n:]
            
            print(f"\nMenampilkan {len(lines)} baris:\n")
            for line in lines:
                print(line.rstrip())
        
    except Exception as e:
        print(f"\n[X] Error membaca file: {e}")
    
    input("\nTekan ENTER untuk kembali...")


def show_enrollment_stats(logger):
    """Tampilkan statistik enrollment"""
    print_header("ENROLLMENT STATISTICS")
    
    stats = logger.get_enrollment_stats()
    
    print(f"\nTotal Enrollments: {stats['total']}")
    print(f"  - Success: {stats['success']}")
    print(f"  - Failed: {stats['failed']}")
    print(f"\nRegistered Names ({len(stats['names'])}):")
    
    if stats['names']:
        for i, name in enumerate(stats['names'], 1):
            print(f"  {i}. {name}")
    else:
        print("  (Belum ada)")
    
    input("\nTekan ENTER untuk kembali...")


def show_recognition_stats(logger, hours=24):
    """Tampilkan statistik recognition"""
    print_header(f"RECOGNITION STATISTICS (Last {hours}h)")
    
    stats = logger.get_recognition_stats(hours=hours)
    
    print(f"\nTotal Recognitions: {stats['total']}")
    print(f"  - Recognized: {stats['recognized']}")
    print(f"  - Unknown: {stats['unknown']}")
    
    if stats['total'] > 0:
        recognized_pct = (stats['recognized'] / stats['total']) * 100
        print(f"  - Recognition Rate: {recognized_pct:.1f}%")
    
    print(f"\nUnique Faces Detected ({len(stats['unique_faces'])}):")
    if stats['unique_faces']:
        for i, name in enumerate(stats['unique_faces'], 1):
            print(f"  {i}. {name}")
    else:
        print("  (Belum ada)")
    
    input("\nTekan ENTER untuk kembali...")


def show_all_stats(logger):
    """Tampilkan semua statistik"""
    print_header("ALL STATISTICS")
    
    # Enrollment stats
    enroll_stats = logger.get_enrollment_stats()
    print("\n[ENROLLMENT]")
    print(f"  Total: {enroll_stats['total']}")
    print(f"  Success: {enroll_stats['success']}")
    print(f"  Failed: {enroll_stats['failed']}")
    print(f"  Registered: {len(enroll_stats['names'])} names")
    
    # Recognition stats (24h)
    recog_stats = logger.get_recognition_stats(hours=24)
    print("\n[RECOGNITION - Last 24h]")
    print(f"  Total: {recog_stats['total']}")
    print(f"  Recognized: {recog_stats['recognized']}")
    print(f"  Unknown: {recog_stats['unknown']}")
    
    if recog_stats['total'] > 0:
        rate = (recog_stats['recognized'] / recog_stats['total']) * 100
        print(f"  Recognition Rate: {rate:.1f}%")
    
    # Log files size
    print("\n[LOG FILES]")
    log_dir = "logs"
    if os.path.exists(log_dir):
        for filename in os.listdir(log_dir):
            if filename.endswith('.log'):
                filepath = os.path.join(log_dir, filename)
                size = os.path.getsize(filepath)
                size_kb = size / 1024
                print(f"  {filename}: {size_kb:.1f} KB")
    
    input("\nTekan ENTER untuk kembali...")


if __name__ == "__main__":
    try:
        view_logs()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
