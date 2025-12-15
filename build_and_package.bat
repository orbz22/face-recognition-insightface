@echo off
REM ============================================
REM Face Recognition - Build & Package Script
REM Otomatis build EXE dan siap distribusi
REM ============================================

echo.
echo ================================================
echo   FACE RECOGNITION - AUTO BUILD SCRIPT
echo ================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python tidak ditemukan!
    echo     Install Python dulu: https://python.org
    pause
    exit /b 1
)

echo [*] Step 1: Install PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo [X] Gagal install PyInstaller!
    pause
    exit /b 1
)

echo.
echo [*] Step 2: Building EXE...
echo     Ini akan memakan waktu beberapa menit...
echo.

pyinstaller --onefile --console --name="FaceRecognition" ^
    --exclude-module PyQt5 ^
    --exclude-module PyQt6 ^
    --exclude-module PySide2 ^
    --exclude-module PySide6 ^
    --exclude-module tkinter ^
    --exclude-module IPython ^
    --exclude-module jupyter ^
    --exclude-module notebook ^
    --exclude-module pandas ^
    --exclude-module pytest ^
    main.py

if errorlevel 1 (
    echo [X] Build gagal!
    pause
    exit /b 1
)

echo.
echo [*] Step 3: Membuat folder distribusi...

REM Buat folder distribusi
if exist "FaceRecognition_Package" rmdir /s /q "FaceRecognition_Package"
mkdir "FaceRecognition_Package"

REM Copy EXE
echo     - Copying EXE...
copy "dist\FaceRecognition.exe" "FaceRecognition_Package\"

REM Copy models
echo     - Copying models...
if exist "models" (
    xcopy /E /I /Y "models" "FaceRecognition_Package\models"
) else (
    echo     [!] Models tidak ditemukan, akan auto-download saat run
)

REM Buat folder face_db kosong
echo     - Creating face_db folder...
mkdir "FaceRecognition_Package\face_db"
echo Folder untuk database wajah > "FaceRecognition_Package\face_db\README.txt"

REM Buat folder qr_codes kosong
echo     - Creating qr_codes folder...
mkdir "FaceRecognition_Package\qr_codes"
echo Folder untuk QR codes > "FaceRecognition_Package\qr_codes\README.txt"

REM Copy README
echo     - Copying documentation...
if exist "README.md" copy "README.md" "FaceRecognition_Package\"

REM Buat file instruksi
echo     - Creating user instructions...
(
echo ================================================
echo   FACE RECOGNITION SYSTEM
echo ================================================
echo.
echo CARA PAKAI:
echo.
echo 1. Double-click FaceRecognition.exe
echo 2. Pilih menu yang diinginkan:
echo    - Menu 1: Enroll ^(daftar wajah baru^)
echo    - Menu 2: Recognize ^(kenali wajah^)
echo    - Menu 3: Switch Camera
echo    - Menu 4: QR Code Menu
echo    - Menu 5: Exit
echo.
echo ENROLL WAJAH:
echo 1. Pilih menu 1
echo 2. Input: Nama Ortu, Nama Anak, Kelas
echo 3. Tekan 'c' untuk capture ^(10x^)
echo 4. QR code otomatis di-generate
echo.
echo SYSTEM REQUIREMENTS:
echo - Windows 10/11
echo - Webcam
echo - Internet ^(untuk download model pertama kali^)
echo.
echo TROUBLESHOOTING:
echo - Jika antivirus block, add exception
echo - Jika kamera tidak terdeteksi, coba menu 3
echo - Jika ada error, jalankan sebagai Administrator
echo.
echo ================================================
) > "FaceRecognition_Package\CARA_PAKAI.txt"

echo.
echo [*] Step 4: Membuat ZIP file...

REM Zip menggunakan PowerShell
powershell -command "Compress-Archive -Path 'FaceRecognition_Package\*' -DestinationPath 'FaceRecognition_v1.0.zip' -Force"

if errorlevel 1 (
    echo [!] Gagal membuat ZIP, tapi folder sudah siap
) else (
    echo     [OK] ZIP created: FaceRecognition_v1.0.zip
)

REM Cleanup build files
echo.
echo [*] Step 5: Cleanup...
if exist "build" rmdir /s /q "build"
if exist "main.spec" del "main.spec"
if exist "FaceRecognition.spec" del "FaceRecognition.spec"

echo.
echo ================================================
echo   BUILD SELESAI!
echo ================================================
echo.
echo Output:
echo   - Folder: FaceRecognition_Package\
echo   - ZIP   : FaceRecognition_v1.0.zip
echo.
echo Ukuran:
if exist "models" (
    echo   ~400 MB ^(dengan models^)
) else (
    echo   ~50 MB ^(tanpa models, auto-download^)
)
echo.
echo Cara distribusi:
echo   1. Upload FaceRecognition_v1.0.zip ke Google Drive
echo   2. Share link ke teman
echo   3. Teman extract dan jalankan FaceRecognition.exe
echo.
echo ================================================

REM Buka folder
explorer "FaceRecognition_Package"

pause
