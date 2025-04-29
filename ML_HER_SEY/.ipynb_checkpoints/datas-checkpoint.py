import pandas as pd
import matplotlib.pyplot as plt

# CSV dosyasını oku
df = pd.read_csv("dataset_labels.csv")

# Her bir label (stil) için kaç görsel var onu say
label_counts = df['label'].value_counts()

# Grafik oluştur
plt.figure(figsize=(10, 6))
label_counts.plot(kind='bar', color='skyblue')

plt.title("Sınıflara Göre Görsel Sayısı")
plt.xlabel("Çizim Stili")
plt.ylabel("Görsel Sayısı")
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.show()
