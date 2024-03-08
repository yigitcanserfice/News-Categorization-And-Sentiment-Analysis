import pandas as pd

# İlk CSV dosyasını oku
df_first = pd.read_csv('Datasets/hepsiburada.csv/hepsiburada.csv')

# Yeni CSV dosyası için DataFrame oluştur
df_new = pd.DataFrame(columns=['Metin_Veri', 'Kategori'])

# Rating ve Review değerleriyle formatı değiştir
for index, row in df_first.iterrows():
    rating = row['Rating']
    review = row['Review']

    # Rating değerini pozitif, negatif olarak etiketle
    sentiment_label = 'pozitif' if rating == 1 else 'negatif'

    # Yeni DataFrame'e ekle
    df_new = pd.concat([df_new, pd.DataFrame({'Metin_Veri': [review], 'Kategori': [sentiment_label]})], ignore_index=True)

# İkinci CSV dosyasını oku
df_original_second = pd.read_csv('yeni_yorum_veri.csv')

# İkinci DataFrame'leri birleştir
df_combined = pd.concat([df_new, df_original_second], ignore_index=True)

# Türkçe karakterleri düzelt
df_combined['Metin_Veri'] = df_combined['Metin_Veri'].str.replace('ð', 'ğ')
df_combined['Metin_Veri'] = df_combined['Metin_Veri'].str.replace('ý', 'ı')
df_combined['Metin_Veri'] = df_combined['Metin_Veri'].str.replace('þ', 'ş')
df_combined['Metin_Veri'] = df_combined['Metin_Veri'].str.replace('ý', 'i')
df_combined['Metin_Veri'] = df_combined['Metin_Veri'].str.replace('Ý', 'İ')
df_combined['Metin_Veri'] = df_combined['Metin_Veri'].str.replace('Þ', 'Ş')

# Yeni DataFrame'i CSV dosyasına yaz
df_combined.to_csv('yeni_yorum_veri_artı_hepsiburada.csv', index=False)

# İşlem bitince mesaj ver
print("CSV dosyası düzenlendi ve birleştirildi.")
