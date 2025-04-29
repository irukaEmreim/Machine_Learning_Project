import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# CSV dosyasını oku (dosyanın yolu senin konumuna göre değişebilir)
df = pd.read_csv("dataset_labels.csv")

# İlk birkaç satırı kontrol et
# print(df.head())

print("Eksik Veri Sayısı:\n", df.isnull().sum())
print (" _________________________ ") 

plt.figure(figsize=(10, 6))
sns.heatmap(df.isnull(), cbar=False, cmap="Reds", yticklabels=False)
plt.title("Eksik Veri Isı Haritası", fontsize=14)
plt.tight_layout()
plt.show()