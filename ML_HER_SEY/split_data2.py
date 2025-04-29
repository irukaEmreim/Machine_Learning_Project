import os               
import shutil           
import random           

categories = ["abstract_digital", "anime", "comic", "digital_realism", "fantasy", "pixel_art", "simple_illustration"]

source_dirs = [
    ".",  
    "./gorseller"  
]

base_output_dir = "dataset_split_2"
splits = ["train", "test"]

for split in splits:
    for category in categories:
        os.makedirs(os.path.join(base_output_dir, split, category), exist_ok=True)

for category in categories:
    all_images = []

    for source in source_dirs:
        folder_path = os.path.join(source, category)
        if not os.path.exists(folder_path):
            continue  

        for filename in os.listdir(folder_path):
            ext = os.path.splitext(filename)[-1].lower()  
            if ext not in [".jpg", ".jpeg", ".png"]:
                continue  

            src_path = os.path.join(folder_path, filename)

            prefix = os.path.basename(source)  
            if prefix == ".":
                prefix = category
            else:
                prefix = f"{prefix}_{category}"

            new_filename = f"{prefix}_{filename}"  
            all_images.append((src_path, new_filename))  

    random.shuffle(all_images)
    total = len(all_images)
    train_end = int(total * 0.8)   # %80'i train

    split_data = {
        "train": all_images[:train_end],
        "test": all_images[train_end:]
    }

    for split, images in split_data.items():
        for src, new_name in images:
            dst_path = os.path.join(base_output_dir, split, category, new_name)
            shutil.copy2(src, dst_path)  

print("OKAYYY")
