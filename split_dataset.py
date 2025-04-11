import os
import shutil
import random
from math import floor

# 📁 Veri kaynak klasörü (temizlenmiş görsellerin olduğu yer)
SOURCE_DIR = "DeviantArt/deviantart_images"
# 🎯 Hedef klasör (buraya train/val/test yapısı oluşturulacak)
DEST_DIR = "FinalDataset/split_dataset"

# 🔢 Oranlar
SPLIT_RATIOS = {
    "train": 0.7,
    "val": 0.15,
    "test": 0.15
}

def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def split_class(class_name):
    class_source = os.path.join(SOURCE_DIR, class_name)
    images = [f for f in os.listdir(class_source) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    random.shuffle(images)

    total = len(images)
    train_end = floor(total * SPLIT_RATIOS["train"])
    val_end = train_end + floor(total * SPLIT_RATIOS["val"])

    split_data = {
        "train": images[:train_end],
        "val": images[train_end:val_end],
        "test": images[val_end:]
    }

    for split_name, image_list in split_data.items():
        split_class_dir = os.path.join(DEST_DIR, split_name, class_name)
        ensure_dir_exists(split_class_dir)

        for img_name in image_list:
            src_path = os.path.join(class_source, img_name)
            dst_path = os.path.join(split_class_dir, img_name)
            shutil.copy2(src_path, dst_path)

    print(f"✅ {class_name} sınıfı bölündü: {len(images)} görsel ({train_end} train, {val_end - train_end} val, {total - val_end} test)")

def main():
    print("🔧 Veri seti bölme işlemi başlatıldı...\n")

    # Stil klasörlerini al (linkler klasörünü dışla)
    class_dirs = [d for d in os.listdir(SOURCE_DIR)
                  if os.path.isdir(os.path.join(SOURCE_DIR, d)) and d != "linkler"]

    for class_name in class_dirs:
        split_class(class_name)

    print("\n🎉 Tüm veri seti başarıyla bölündü!")

if __name__ == "__main__":
    main()
