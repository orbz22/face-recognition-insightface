# Build Script untuk Create EXE
# Menggunakan PyInstaller

# Install PyInstaller dulu
pip install pyinstaller

# Build command
pyinstaller --name="FaceRecognition" ^
    --onefile ^
    --windowed ^
    --icon=icon.ico ^
    --add-data="models;models" ^
    --add-data="face_db;face_db" ^
    --add-data="README.md;." ^
    --hidden-import=cv2 ^
    --hidden-import=numpy ^
    --hidden-import=insightface ^
    --hidden-import=onnxruntime ^
    --hidden-import=qrcode ^
    --hidden-import=pyzbar ^
    --hidden-import=cryptography ^
    main.py

# Output akan ada di folder dist/
# File: dist/FaceRecognition.exe
