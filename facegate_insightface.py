import os
import sys
import json
import time
import argparse
from dataclasses import dataclass
from typing import List, Optional, Tuple

import cv2
import numpy as np

# InsightFace
from insightface.app import FaceAnalysis

# Logger
from logger import get_logger

logger = get_logger()


# =========================
# Utils
# =========================

def l2_normalize(x: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    n = np.linalg.norm(x) + eps
    return x / n

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    # a, b already normalized
    return float(np.dot(a, b))

def ensure_dir(p: str) -> None:
    os.makedirs(p, exist_ok=True)

def now_str() -> str:
    return time.strftime("%Y%m%d_%H%M%S")


# =========================
# DB Storage
# =========================

@dataclass
class FaceDB:
    db_dir: str
    emb_path: str
    label_path: str

    def __init__(self, db_dir: str = "face_db"):
        self.db_dir = db_dir
        ensure_dir(db_dir)
        self.emb_path = os.path.join(db_dir, "embeddings.npy")
        self.label_path = os.path.join(db_dir, "labels.json")

    def load(self) -> Tuple[np.ndarray, List[str]]:
        if os.path.exists(self.emb_path) and os.path.exists(self.label_path):
            try:
                embs = np.load(self.emb_path).astype(np.float32)
                
                # Check if load failed
                if embs is None:
                    print(f"Warning: Failed to load embeddings from {self.emb_path}")
                    return np.zeros((0, 512), dtype=np.float32), []
                
                with open(self.label_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if not content:
                        # File kosong, return empty
                        return np.zeros((0, 512), dtype=np.float32), []
                    labels = json.loads(content)
                
                # Check if labels is valid
                if labels is None:
                    print(f"Warning: Failed to load labels from {self.label_path}")
                    return np.zeros((0, 512), dtype=np.float32), []
                
                # Validasi: pastikan jumlah embeddings dan labels sama
                if embs.shape[0] != len(labels):
                    print(f"⚠️  Warning: Database mismatch! Embeddings: {embs.shape[0]}, Labels: {len(labels)}")
                    print(f"   Database corrupted. Please delete {self.db_dir} and re-enroll.")
                    return np.zeros((0, 512), dtype=np.float32), []
                
                # Normalize for cosine search
                embs = np.stack([l2_normalize(e) for e in embs], axis=0) if len(embs) else embs
                return embs, labels
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Warning: Error loading DB files ({e}). Returning empty DB.")
                return np.zeros((0, 512), dtype=np.float32), []
            except Exception as e:
                print(f"Warning: Unexpected error loading DB ({e}). Returning empty DB.")
                return np.zeros((0, 512), dtype=np.float32), []
        return np.zeros((0, 512), dtype=np.float32), []

    def save(self, embs: np.ndarray, labels: List[str]) -> None:
        np.save(self.emb_path, embs.astype(np.float32))
        with open(self.label_path, "w", encoding="utf-8") as f:
            json.dump(labels, f, ensure_ascii=False, indent=2)

    def add(self, emb: np.ndarray, label: str) -> None:
        embs, labels = self.load()
        emb = l2_normalize(emb.astype(np.float32))
        if embs.shape[0] == 0:
            # infer dim from embedding
            embs = emb.reshape(1, -1)
        else:
            # guard dimension mismatch
            if emb.shape[0] != embs.shape[1]:
                raise ValueError(f"Embedding dim mismatch: got {emb.shape[0]}, expected {embs.shape[1]}")
            embs = np.vstack([embs, emb.reshape(1, -1)])
        labels.append(label)
        self.save(embs, labels)


# =========================
# InsightFace App
# =========================

def build_face_app(model_name: str = "buffalo_l", det_size: int = 640, device: str = "cpu", model_root: str = None) -> FaceAnalysis:
    """
    Load InsightFace model dari folder lokal project.
    
    Args:
        model_name: nama model (default: "buffalo_l")
        det_size: ukuran detection (default: 640)
        device: "cpu" atau "cuda"
        model_root: path ke folder root. Jika None, akan gunakan direktori script
                   (InsightFace akan otomatis menambahkan subfolder 'models')
    
    Returns:
        FaceAnalysis app yang sudah di-prepare
    """
    # Tentukan model root path
    if model_root is None:
        # Check if running from PyInstaller
        if getattr(sys, 'frozen', False):
            # Running from PyInstaller EXE
            # sys.executable points to the EXE file
            # We want the directory containing the EXE
            model_root = os.path.dirname(sys.executable)
        else:
            # Running from Python script
            model_root = os.path.dirname(os.path.abspath(__file__))
    
    # InsightFace akan cari di: model_root/models/model_name
    expected_model_path = os.path.join(model_root, "models", model_name)
    
    # Jika tidak ditemukan, coba cari di parent directory (untuk compatibility)
    if not os.path.exists(expected_model_path):
        parent_root = os.path.dirname(model_root)
        alternative_path = os.path.join(parent_root, "models", model_name)
        if os.path.exists(alternative_path):
            model_root = parent_root
            expected_model_path = alternative_path
    
    if not os.path.exists(expected_model_path):
        raise FileNotFoundError(
            f"Model tidak ditemukan di: {expected_model_path}\n"
            f"Pastikan folder 'models/{model_name}' ada dan berisi file .onnx\n"
            f"Model root: {model_root}\n"
            f"Coba copy folder 'models' ke: {model_root}"
        )
    
    print(f"Loading model dari: {expected_model_path}")
    
    # Setup providers
    providers = None
    if device.lower() == "cuda":
        # kalau kamu pakai onnxruntime-gpu
        providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
    else:
        providers = ["CPUExecutionProvider"]

    # Load model dari folder lokal
    # root parameter akan membuat InsightFace cari di <root>/models/<name>
    app = FaceAnalysis(name=model_name, root=model_root, providers=providers)
    app.prepare(ctx_id=0 if device.lower() == "cuda" else -1,
                det_size=(det_size, det_size))
    return app

def pick_largest_face(faces) -> Optional[object]:
    if not faces:
        return None
    # pilih wajah terbesar (asumsi subjek utama)
    areas = []
    for f in faces:
        x1, y1, x2, y2 = f.bbox.astype(int)
        areas.append((x2 - x1) * (y2 - y1))
    return faces[int(np.argmax(areas))]


# =========================
# Camera Loop
# =========================

def open_camera(cam_index: int, width: int, height: int) -> cv2.VideoCapture:
    cap = cv2.VideoCapture(cam_index)
    if not cap.isOpened():
        raise RuntimeError(f"Camera {cam_index} cannot be opened.")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    return cap

def draw_box_and_text(img, face, text: str):
    """Draw bounding box and text. Supports formatted labels: ParentName_ChildName_Class"""
    x1, y1, x2, y2 = face.bbox.astype(int)
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    # Parse label jika format: NamaOrtu_NamaAnak_Kelas
    if '_' in text and text.count('_') >= 2:
        parts = text.split('|')[0].strip()  # Ambil bagian sebelum '|' (jika ada similarity)
        
        if '_' in parts:
            label_parts = parts.split('_')
            if len(label_parts) >= 3:
                parent = label_parts[0]
                child = label_parts[1]
                class_name = label_parts[2]
                
                # Display multi-line
                y_offset = max(10, y1 - 60)
                cv2.putText(img, f"Ortu: {parent}", (x1, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(img, f"Anak: {child}", (x1, y_offset + 20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(img, f"Kelas: {class_name}", (x1, y_offset + 40), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
                
                # Tampilkan similarity jika ada
                if '|' in text:
                    similarity_text = text.split('|')[1].strip()
                    cv2.putText(img, similarity_text, (x1, y_offset + 60), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
                return
    
    # Fallback: tampilan biasa
    y = max(0, y1 - 10)
    cv2.putText(img, text, (x1, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)


# =========================
# Modes
# =========================

def enroll_mode(app: FaceAnalysis,
                db: FaceDB,
                name: str,
                cam_index: int = 0,
                width: int = 1280,
                height: int = 720,
                samples: int = 10,
                min_det_score: float = 0.6,
                save_snapshots: bool = True):
    """
    Ambil beberapa sample embedding lalu rata-ratakan -> satu embedding per orang (lebih stabil).
    Tekan:
      - 'c' capture sample
      - 'q' quit
    """
    snap_dir = os.path.join(db.db_dir, "snapshots", name.replace(" ", "_"))
    if save_snapshots:
        ensure_dir(snap_dir)

    cap = open_camera(cam_index, width, height)
    collected = []

    print("\n[ENROLL]")
    print("Arahkan wajah ke kamera. Tekan 'c' untuk capture sample.")
    print(f"Target samples: {samples}. Tekan 'q' untuk selesai.\n")

    while True:
        ok, frame = cap.read()
        if not ok:
            print("Gagal baca frame.")
            break

        faces = app.get(frame)
        face = pick_largest_face(faces)

        disp = frame.copy()
        if face is not None and float(face.det_score) >= min_det_score:
            draw_box_and_text(disp, face, f"{name} | det={face.det_score:.2f} | samples={len(collected)}/{samples}")
        else:
            cv2.putText(disp, "No face / low confidence", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.imshow("Enroll - press c to capture, q to quit", disp)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            if face is None or float(face.det_score) < min_det_score:
                print("Wajah belum terdeteksi jelas. Coba lagi (lebih dekat / pencahayaan lebih terang).")
                continue

            emb = face.normed_embedding  # biasanya sudah L2 normalized
            collected.append(emb.astype(np.float32))

            if save_snapshots:
                fn = os.path.join(snap_dir, f"{now_str()}_{len(collected)}.jpg")
                cv2.imwrite(fn, frame)

            print(f"Captured sample {len(collected)}/{samples}")

            if len(collected) >= samples:
                break

        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if len(collected) == 0:
        print("Tidak ada sample. Enroll dibatalkan.")
        logger.log_enrollment(name, 0, success=False, camera_index=cam_index, 
                            notes="No samples collected")
        return

    # rata-rata lalu normalize
    avg_emb = np.mean(np.stack(collected, axis=0), axis=0)
    avg_emb = l2_normalize(avg_emb)

    db.add(avg_emb, name)
    logger.log_enrollment(name, len(collected), success=True, camera_index=cam_index)
    print(f"\n✅ Enroll selesai. '{name}' ditambahkan ke database ({db.db_dir}).")
    
    # AUTO-GENERATE QR CODE
    try:
        from qr_manager import QRCodeManager
        qr_manager = QRCodeManager(db_dir=db.db_dir)
        
        # Get index (last added)
        index = len(db.load()[1]) - 1
        
        print(f"\n[*] Generating QR code...")
        success = qr_manager.generate_qr_code(name, index, silent=True)
        
        if success:
            print(f"✅ QR code generated: qr_codes/{name}.png")
            print(f"   Cetak dan berikan QR code ini ke orang tua sebagai backup.")
        else:
            print(f"⚠️  QR code generation failed (enrollment tetap berhasil)")
    except Exception as e:
        print(f"⚠️  QR code generation error: {e} (enrollment tetap berhasil)")


def recognize_mode(app: FaceAnalysis,
                   db: FaceDB,
                   cam_index: int = 0,
                   width: int = 1280,
                   height: int = 720,
                   threshold: float = 0.35,
                   min_det_score: float = 0.6):
    """
    Real-time recognition:
    - ambil embedding wajah terbesar
    - hitung cosine similarity ke semua embedding di DB
    - jika sim >= threshold => dikenal
    Catatan:
    - threshold perlu dikalibrasi (0.3 - 0.5 tergantung model & kondisi).
    """
    embs, labels = db.load()
    
    # Check if database is empty or invalid
    if embs is None or labels is None:
        print(f"DB error. Tidak bisa load database. (folder: {db.db_dir})")
        return
    
    if embs.shape[0] == 0:
        print(f"DB kosong. Jalankan enroll dulu. (folder: {db.db_dir})")
        return

    cap = open_camera(cam_index, width, height)
    print("\n[RECOGNIZE]")
    print("Tekan 'q' untuk keluar.\n")

    frame_count = 0
    last_result = None  # Cache last recognition result
    
    while True:
        ok, frame = cap.read()
        if not ok:
            print("Gagal baca frame.")
            break

        frame_count += 1
        disp = frame.copy()
        
        # Process every 3rd frame for better performance
        # Display cached result on skipped frames
        if frame_count % 3 == 0:
            faces = app.get(frame)
            face = pick_largest_face(faces)

            if face is not None and float(face.det_score) >= min_det_score:
                emb = face.normed_embedding.astype(np.float32)
                emb = l2_normalize(emb)

                # cosine similarity: embs already normalized
                sims = embs @ emb  # (N,)
                best_idx = int(np.argmax(sims))
                best_sim = float(sims[best_idx])

                if best_sim >= threshold:
                    name = labels[best_idx]
                    last_result = (face, f"{name} | sim={best_sim:.2f}", True)
                    logger.log_recognition(name, best_sim, cam_index, threshold)
                else:
                    last_result = (face, f"Unknown | sim={best_sim:.2f}", False)
                    logger.log_recognition(None, best_sim, cam_index, threshold)
            else:
                last_result = None
        
        # Draw last result (even on skipped frames for smooth display)
        if last_result is not None:
            face, text, _ = last_result
            draw_box_and_text(disp, face, text)
        else:
            cv2.putText(disp, "No face / low confidence", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.imshow("Recognize - press q to quit", disp)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# =========================
# Main
# =========================

def main():
    parser = argparse.ArgumentParser(description="Face recognition using InsightFace (ArcFace embeddings).")
    parser.add_argument("--mode", choices=["enroll", "recognize"], required=True)
    parser.add_argument("--name", type=str, default="", help="Name/ID for enroll")
    parser.add_argument("--db", type=str, default="face_db", help="DB folder")
    parser.add_argument("--model", type=str, default="buffalo_l", help="InsightFace model pack name (e.g., buffalo_l)")
    parser.add_argument("--device", type=str, default="cpu", choices=["cpu", "cuda"], help="Runtime device")
    parser.add_argument("--cam", type=int, default=1, help="Camera index")
    parser.add_argument("--w", type=int, default=1280)
    parser.add_argument("--h", type=int, default=720)
    parser.add_argument("--det", type=int, default=640, help="det_size (square)")
    parser.add_argument("--min_det", type=float, default=0.6, help="Minimum detection score")
    parser.add_argument("--samples", type=int, default=10, help="Enroll samples")
    parser.add_argument("--thr", type=float, default=0.35, help="Cosine similarity threshold for 'known'")
    args = parser.parse_args()

    db = FaceDB(args.db)
    app = build_face_app(model_name=args.model, det_size=args.det, device=args.device)

    if args.mode == "enroll":
        if not args.name.strip():
            raise ValueError("Mode enroll but --name is empty. Example: --name \"Raihan\"")
        enroll_mode(app, db, name=args.name.strip(),
                    cam_index=args.cam, width=args.w, height=args.h,
                    samples=args.samples, min_det_score=args.min_det)
    else:
        recognize_mode(app, db,
                       cam_index=args.cam, width=args.w, height=args.h,
                       threshold=args.thr, min_det_score=args.min_det)


if __name__ == "__main__":
    main()
