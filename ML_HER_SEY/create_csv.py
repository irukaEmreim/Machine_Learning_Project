import os
import csv

root_folder = "dataset_split"
csv_path = "dataset_labels.csv"

data = []

for split in ['train', 'val', 'test']:
    split_path = os.path.join(root_folder, split)
    if not os.path.exists(split_path):
        continue

    for label in os.listdir(split_path):
        label_path = os.path.join(split_path, label)
        if not os.path.isdir(label_path):
            continue

        for img_name in os.listdir(label_path):
            full_path = os.path.join(split, label, img_name)
            data.append([split, full_path, label])

# CSV dosyasını yaz
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["split", "image_path", "label"])  # Yeni başlık
    writer.writerows(data)

print(f"CSV dosyası oluşturuldu: {csv_path}")
