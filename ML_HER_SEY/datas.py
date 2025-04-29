import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("dataset_labels.csv")

label_counts = df['label'].value_counts()

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Bar 
label_counts.plot(kind='bar', ax=axes[0], color='red', edgecolor='black')
axes[0].set_title("Sınıflara Göre Görsel Sayısı")
axes[0].set_xlabel("Çizim Stili")
axes[0].set_ylabel("Görsel Sayısı")
axes[0].tick_params(axis='x', rotation=45)
axes[0].grid(axis='y', linestyle='--', alpha=0.7)

# Pasta 
label_counts.plot(kind='pie', ax=axes[1], autopct='%1.1f%%', startangle=140, textprops={'fontsize': 10})
axes[1].set_title("Çizim Stili Dağılımı")
axes[1].set_ylabel("")  

plt.tight_layout()
plt.show()
