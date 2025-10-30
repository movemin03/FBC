import os
from PIL import Image
from pathlib import Path

def convert_jpg_to_webp(root_folder, quality=85, delete_original=False):
    """
    Convert all JPG files in folder (including subfolders) to WebP format
    
    Args:
        root_folder (str): Root folder path to search for JPG files
        quality (int): WebP quality (0-100, default 85)
        delete_original (bool): Delete original JPG files after conversion
    """
    
    # Statistics
    stats = {
        'total': 0,
        'success': 0,
        'fail': 0,
        'skipped': 0
    }
    
    # Supported extensions
    jpg_extensions = ['.jpg', '.jpeg', '.JPG', '.JPEG']
    
    print("=" * 70)
    print("JPG to WebP Converter")
    print("=" * 70)
    print(f"Root folder: {root_folder}")
    print(f"Quality: {quality}")
    print(f"Delete original: {'Yes' if delete_original else 'No'}")
    print()
    
    # Walk through all directories
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            # Check if file is JPG
            if any(filename.endswith(ext) for ext in jpg_extensions):
                stats['total'] += 1
                
                input_path = os.path.join(dirpath, filename)
                output_filename = os.path.splitext(filename)[0] + '.webp'
                output_path = os.path.join(dirpath, output_filename)
                
                # Skip if WebP already exists
                if os.path.exists(output_path):
                    print(f"[SKIP] {output_path} already exists")
                    stats['skipped'] += 1
                    continue
                
                try:
                    # Open and convert image
                    img = Image.open(input_path)
                    
                    # Convert RGBA to RGB if necessary
                    if img.mode in ('RGBA', 'LA', 'P'):
                        img = img.convert('RGB')
                    
                    # Save as WebP
                    img.save(output_path, 'webp', quality=quality, method=6)
                    img.close()
                    
                    # Get file sizes for comparison
                    original_size = os.path.getsize(input_path)
                    webp_size = os.path.getsize(output_path)
                    compression_ratio = (1 - webp_size / original_size) * 100
                    
                    print(f"[OK] {input_path}")
                    print(f"     -> {output_path}")
                    print(f"     Size: {original_size:,} bytes -> {webp_size:,} bytes ({compression_ratio:.1f}% reduction)")
                    
                    stats['success'] += 1
                    
                    # Delete original if requested
                    if delete_original:
                        os.remove(input_path)
                        print(f"     [DELETED] Original file removed")
                    
                    print()
                    
                except Exception as e:
                    print(f"[FAIL] {input_path}")
                    print(f"       Error: {str(e)}")
                    print()
                    stats['fail'] += 1
    
    # Print summary
    print()
    print("=" * 70)
    print("Conversion Summary")
    print("=" * 70)
    print(f"Total JPG files found: {stats['total']}")
    print(f"Successfully converted: {stats['success']}")
    print(f"Skipped (already exists): {stats['skipped']}")
    print(f"Failed: {stats['fail']}")
    print("=" * 70)


if __name__ == "__main__":
    # 설정
    ROOT_FOLDER = r"C:\Users\kwony\Desktop\FBC\img"  # 변환할 루트 폴더
    QUALITY = 85  # WebP 품질 (0-100)
    DELETE_ORIGINAL = False  # True로 설정하면 원본 JPG 파일 삭제
    
    # 실행
    convert_jpg_to_webp(ROOT_FOLDER, quality=QUALITY, delete_original=DELETE_ORIGINAL)
    
    input("\nPress Enter to exit...")
