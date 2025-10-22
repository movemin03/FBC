import os
import shutil
from pathlib import Path

def move_webp_files(source_folder, destination_folder, maintain_structure=False):
    """
    Move all WebP files from source folder (including subfolders) to destination folder
    
    Args:
        source_folder (str): Source folder to search for WebP files
        destination_folder (str): Destination folder to move WebP files
        maintain_structure (bool): If True, maintain original folder structure
    """
    
    # Statistics
    stats = {
        'total': 0,
        'moved': 0,
        'skipped': 0,
        'failed': 0
    }
    
    print("=" * 70)
    print("WebP File Mover")
    print("=" * 70)
    print(f"Source folder: {source_folder}")
    print(f"Destination folder: {destination_folder}")
    print(f"Maintain structure: {'Yes' if maintain_structure else 'No'}")
    print()
    
    # Create destination folder if not exists
    os.makedirs(destination_folder, exist_ok=True)
    
    # Walk through all directories
    for dirpath, dirnames, filenames in os.walk(source_folder):
        for filename in filenames:
            # Check if file is WebP
            if filename.lower().endswith('.webp'):
                stats['total'] += 1
                
                source_path = os.path.join(dirpath, filename)
                
                # Determine destination path
                if maintain_structure:
                    # Maintain original folder structure
                    rel_path = os.path.relpath(dirpath, source_folder)
                    dest_dir = os.path.join(destination_folder, rel_path)
                    os.makedirs(dest_dir, exist_ok=True)
                    dest_path = os.path.join(dest_dir, filename)
                else:
                    # Move all files to root of destination folder
                    dest_path = os.path.join(destination_folder, filename)
                
                # Check if file already exists
                if os.path.exists(dest_path):
                    print(f"[SKIP] {filename} already exists in destination")
                    stats['skipped'] += 1
                    continue
                
                try:
                    # Move the file
                    shutil.move(source_path, dest_path)
                    print(f"[OK] Moved: {source_path}")
                    print(f"     -> {dest_path}")
                    stats['moved'] += 1
                    
                except Exception as e:
                    print(f"[FAIL] {source_path}")
                    print(f"       Error: {str(e)}")
                    stats['failed'] += 1
    
    # Print summary
    print()
    print("=" * 70)
    print("Move Summary")
    print("=" * 70)
    print(f"Total WebP files found: {stats['total']}")
    print(f"Successfully moved: {stats['moved']}")
    print(f"Skipped (already exists): {stats['skipped']}")
    print(f"Failed: {stats['failed']}")
    print("=" * 70)


if __name__ == "__main__":
    # 설정
    SOURCE_FOLDER = r"C:\Users\kwony\Desktop\FBC\img"  # WebP 파일을 찾을 소스 폴더
    DESTINATION_FOLDER = r"C:\Users\kwony\Desktop\FBC\webp_img"  # WebP 파일을 옮길 목적지 폴더
    MAINTAIN_STRUCTURE = False  # True: 원본 폴더 구조 유지, False: 모든 파일을 한 폴더에
    
    # 실행
    move_webp_files(SOURCE_FOLDER, DESTINATION_FOLDER, maintain_structure=MAINTAIN_STRUCTURE)
    
    input("\nPress Enter to exit...")
