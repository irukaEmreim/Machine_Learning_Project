import os  
from PIL import Image  

base_dirs = [
    "Artstation/gorseller",
    "DeviantArt/deviantart_images"  # Linkler de vardı orada :(
]

valid_extensions = [".jpg", ".jpeg", ".png"]

min_width = 128
min_height = 128

def temizle_klasor(dizin):
    for root, dirs, files in os.walk(dizin):
        for file in files:
            dosya_yolu = os.path.join(root, file)  
            _, ext = os.path.splitext(dosya_yolu)  # Uzantı
            ext = ext.lower()  

            if ext not in valid_extensions:
                print(f"Siliniyor -->>> {dosya_yolu}")
                os.remove(dosya_yolu)
                continue

            try:
                with Image.open(dosya_yolu) as img:
                    width, height = img.size
                    if width < min_width or height < min_height:
                        print(f"Siliniyor -Boyuttan- : {dosya_yolu}")
                        os.remove(dosya_yolu)

            except Exception as e:
                print(f"Siliniyor -Açılmadı- : {dosya_yolu} -> {e}")
                os.remove(dosya_yolu)

for base_dir in base_dirs:
    temizle_klasor(base_dir)

print("Bitti.")
