from PIL import Image
import os

# ✅ Ayarlar
ROOT_DIR = "DeviantArt/deviantart_images"
MIN_WIDTH = 128
MIN_HEIGHT = 128

def remove_corrupt_images(folder_path):
    """
    Açılmayan ya da bozuk görselleri siler.
    """
    print("🔍 Bozuk görseller taranıyor...")
    deleted = 0
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with Image.open(file_path) as img:
                    img.verify()
            except Exception:
                print(f"🗑️ Hatalı silindi: {file_path}")
                os.remove(file_path)
                deleted += 1
    print(f"✅ Bozuk görsel temizliği tamamlandı. Silinen: {deleted} dosya\n")

def remove_low_resolution_images(folder_path, min_width=128, min_height=128):
    """
    Belirli boyutlardan küçük olan görselleri siler.
    """
    print("1 Küçük boyutlu görseller taranıyor...")
    deleted = 0
    for root, _, files in os.walk(folder_path):
        if "linkler" in root:
            continue
        
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with Image.open(file_path) as img:
                    img.load()
                    width, height = img.size
                    if width < min_width or height < min_height:
                        print(f"🗑️ Küçük boyutlu silindi: {file_path} ({width}x{height})")
                        os.remove(file_path)
                        deleted += 1
            except:
                pass
    print(f"✅ Boyut kontrolü tamamlandı. Silinen: {deleted} dosya\n")

if __name__ == "__main__":
    print("🧼 Görsel temizleme başlatıldı...\n")
    remove_corrupt_images(ROOT_DIR)
    remove_low_resolution_images(ROOT_DIR, MIN_WIDTH, MIN_HEIGHT)
    print("🎉 Tüm temizlik işlemleri tamamlandı.")
