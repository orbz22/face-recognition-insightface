"""
Performance Log Viewer
Analyze dan visualize performance logs
"""

import os
import sys
from datetime import datetime


def view_performance_log(log_file: str = "logs/performance.log"):
    """View dan analyze performance log"""
    
    if not os.path.exists(log_file):
        print(f"[X] Log file tidak ditemukan: {log_file}")
        print("    Jalankan recognition mode dulu untuk generate log.")
        return
    
    print("\n" + "="*70)
    print("  PERFORMANCE LOG VIEWER")
    print("="*70)
    print(f"File: {log_file}\n")
    
    # Read log file
    with open(log_file, 'r') as f:
        lines = f.readlines()
    
    if len(lines) <= 1:
        print("[!] Log file kosong (hanya header)")
        return
    
    # Parse header
    header = lines[0].strip().split(',')
    
    # Parse data
    data = []
    for line in lines[1:]:
        if line.strip():
            values = line.strip().split(',')
            if len(values) == len(header):
                data.append(values)
    
    if not data:
        print("[!] Tidak ada data di log file")
        return
    
    print(f"Total entries: {len(data)}")
    print(f"Time range: {data[0][0]} to {data[-1][0]}")
    print()
    
    # Calculate statistics
    fps_values = [float(row[1]) for row in data if row[1]]
    frame_ms_values = [float(row[2]) for row in data if row[2]]
    inference_ms_values = [float(row[3]) for row in data if row[3]]
    cpu_values = [float(row[4]) for row in data if row[4]]
    memory_values = [float(row[5]) for row in data if row[5]]
    
    print("="*70)
    print("  STATISTICS")
    print("="*70)
    
    # FPS
    print(f"\nFPS (Frames Per Second):")
    print(f"  Average:  {sum(fps_values)/len(fps_values):.2f}")
    print(f"  Min:      {min(fps_values):.2f}")
    print(f"  Max:      {max(fps_values):.2f}")
    
    # Frame Time
    print(f"\nFrame Time (ms):")
    print(f"  Average:  {sum(frame_ms_values)/len(frame_ms_values):.2f}")
    print(f"  Min:      {min(frame_ms_values):.2f}")
    print(f"  Max:      {max(frame_ms_values):.2f}")
    
    # Inference Time
    print(f"\nInference Time (ms):")
    print(f"  Average:  {sum(inference_ms_values)/len(inference_ms_values):.2f}")
    print(f"  Min:      {min(inference_ms_values):.2f}")
    print(f"  Max:      {max(inference_ms_values):.2f}")
    
    # CPU
    print(f"\nCPU Usage (%):")
    print(f"  Average:  {sum(cpu_values)/len(cpu_values):.2f}")
    print(f"  Min:      {min(cpu_values):.2f}")
    print(f"  Max:      {max(cpu_values):.2f}")
    
    # Memory
    print(f"\nMemory Usage (MB):")
    print(f"  Average:  {sum(memory_values)/len(memory_values):.2f}")
    print(f"  Min:      {min(memory_values):.2f}")
    print(f"  Max:      {max(memory_values):.2f}")
    
    print("\n" + "="*70)
    
    # Performance assessment
    print("\n  PERFORMANCE ASSESSMENT")
    print("="*70)
    
    avg_fps = sum(fps_values)/len(fps_values)
    avg_cpu = sum(cpu_values)/len(cpu_values)
    avg_inference = sum(inference_ms_values)/len(inference_ms_values)
    
    # FPS assessment
    if avg_fps >= 25:
        fps_status = "[OK] Excellent"
    elif avg_fps >= 15:
        fps_status = "[!] Good"
    else:
        fps_status = "[X] Poor"
    
    # CPU assessment
    if avg_cpu <= 60:
        cpu_status = "[OK] Normal"
    elif avg_cpu <= 80:
        cpu_status = "[!] High"
    else:
        cpu_status = "[X] Very High"
    
    # Inference assessment
    if avg_inference <= 30:
        inf_status = "[OK] Fast"
    elif avg_inference <= 50:
        inf_status = "[!] Acceptable"
    else:
        inf_status = "[X] Slow"
    
    print(f"\nFPS:       {avg_fps:.1f} - {fps_status}")
    print(f"CPU:       {avg_cpu:.1f}% - {cpu_status}")
    print(f"Inference: {avg_inference:.1f}ms - {inf_status}")
    
    # Recommendations
    print("\n  RECOMMENDATIONS")
    print("="*70)
    
    if avg_fps < 20:
        print("\n[!] Low FPS detected!")
        print("   - Consider reducing camera resolution")
        print("   - Consider reducing detection size")
        print("   - Consider increasing frame skip")
    
    if avg_cpu > 70:
        print("\n[!] High CPU usage detected!")
        print("   - Close other applications")
        print("   - Reduce processing load")
        print("   - Consider using GPU if available")
    
    if avg_inference > 40:
        print("\n[!] Slow inference detected!")
        print("   - Reduce detection size")
        print("   - Use smaller model if available")
        print("   - Consider GPU acceleration")
    
    if avg_fps >= 25 and avg_cpu <= 60 and avg_inference <= 30:
        print("\n[OK] Performance is excellent! No changes needed.")
    
    print("\n" + "="*70)


def show_recent_entries(log_file: str = "logs/performance.log", n: int = 10):
    """Show last N entries from log"""
    
    if not os.path.exists(log_file):
        print(f"[X] Log file tidak ditemukan: {log_file}")
        return
    
    with open(log_file, 'r') as f:
        lines = f.readlines()
    
    if len(lines) <= 1:
        print("[!] Log file kosong")
        return
    
    print("\n" + "="*70)
    print(f"  RECENT ENTRIES (Last {n})")
    print("="*70)
    
    # Print header
    print(lines[0].strip())
    print("-"*70)
    
    # Print last N entries
    for line in lines[-n:]:
        if line.strip():
            print(line.strip())
    
    print("="*70)


def clear_log(log_file: str = "logs/performance.log"):
    """Clear performance log"""
    
    if not os.path.exists(log_file):
        print(f"[!] Log file tidak ditemukan: {log_file}")
        return
    
    confirm = input(f"\n⚠️  Clear log file {log_file}? (y/n): ").strip().lower()
    
    if confirm == 'y':
        # Recreate with header only
        with open(log_file, 'w') as f:
            f.write("timestamp,fps,frame_ms,inference_ms,cpu_percent,memory_mb,memory_percent\n")
        print("✅ Log file cleared!")
    else:
        print("❌ Cancelled")


def main():
    """Main menu"""
    
    while True:
        print("\n" + "="*70)
        print("  PERFORMANCE LOG VIEWER")
        print("="*70)
        print("1. View full analysis")
        print("2. Show recent entries (last 10)")
        print("3. Show recent entries (last 50)")
        print("4. Clear log file")
        print("5. Exit")
        print("="*70)
        
        choice = input("\nPilih menu (1-5): ").strip()
        
        if choice == "1":
            view_performance_log()
        elif choice == "2":
            show_recent_entries(n=10)
        elif choice == "3":
            show_recent_entries(n=50)
        elif choice == "4":
            clear_log()
        elif choice == "5":
            print("\n[*] Terima kasih!")
            break
        else:
            print("\n[X] Pilihan tidak valid!")
        
        input("\nTekan ENTER untuk kembali...")


if __name__ == "__main__":
    main()
