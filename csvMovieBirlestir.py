import pandas as pd

# İlk CSV dosyasını oku
df_original = pd.read_csv('Datasets/turkish_movie_sentiment/turkish_movie_sentiment_dataset.csv')

# Yeni CSV dosyası için DataFrame oluştur
df_new = pd.DataFrame(columns=['Metin_Veri', 'Kategori'])

# Comment ve point değerleriyle formatı değiştir
for index, row in df_original.iterrows():
    comment = row['comment']
    film_name = row['film_name']
    point = row['point']

    # Türkçe karakterleri düzelt
    comment = comment.replace('ð', 'ğ')
    comment = comment.replace('ý', 'ı')
    comment = comment.replace('þ', 'ş')
    comment = comment.replace('ý', 'i')
    comment = comment.replace('Ý', 'İ')
    comment = comment.replace('Þ', 'Ş')

    # Point sütunundaki virgülü noktaya çevir ve float'a dönüştür
    try:
        point = float(point.replace(',', '.'))
    except ValueError:
        print(f"Hata: Point değeri geçersiz: {point}")
        continue  # Geçersiz point değerleri almadan geç

    # Punları pozitif, tarafsız, negatif olarak etiketle
    if 3.6 <= point <= 5.0:
        sentiment_label = 'pozitif'
    elif 2.1 <= point <= 3.5:
        sentiment_label = 'tarafsiz'
    elif 0.0 <= point <= 2.0:
        sentiment_label = 'negatif'

    # Yeni DataFrame'e ekle
    df_new = pd.concat([df_new, pd.DataFrame({'Metin_Veri': [comment], 'Kategori': [sentiment_label]})], ignore_index=True)

# İkinci CSV dosyasını oku
df_original_second = pd.read_csv('veri_seti555.csv')

# DataFrame'leri birleştir
df_combined = pd.concat([df_new, df_original_second], ignore_index=True)

# Türkçe karakterleri düzelt
df_combined['Metin_Veri'] = df_combined['Metin_Veri'].str.replace('ð', 'ğ')
df_combined['Metin_Veri'] = df_combined['Metin_Veri'].str.replace('ý', 'ı')
df_combined['Metin_Veri'] = df_combined['Metin_Veri'].str.replace('þ', 'ş')
df_combined['Metin_Veri'] = df_combined['Metin_Veri'].str.replace('ý', 'i')
df_combined['Metin_Veri'] = df_combined['Metin_Veri'].str.replace('Ý', 'İ')
df_combined['Metin_Veri'] = df_combined['Metin_Veri'].str.replace('Þ', 'Ş')

# Yeni DataFrame'i CSV dosyasına yazdır
df_combined.to_csv('yeni_yorum_veri.csv', index=False)

# İşlem bitince mesaj ver
print("CSV dosyası düzenlendi ve birleştirildi.")
