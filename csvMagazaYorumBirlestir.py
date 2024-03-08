import pandas as pd

# İlk CSV dosyasını oku
df_combined_previous = pd.read_csv('yeni_yorum_veri_artı_hepsiburada.csv')

# Yeni CSV dosyasını oku
df_new_data = pd.read_csv('magaza_yorumlari_duygu_analizi.csv', encoding='utf-16')

# Türkçe karakter sorununu çöz
df_new_data['Metin_Veri'] = df_new_data['Metin_Veri'].str.replace('ð', 'ğ')
df_new_data['Metin_Veri'] = df_new_data['Metin_Veri'].str.replace('ý', 'ı')
df_new_data['Metin_Veri'] = df_new_data['Metin_Veri'].str.replace('þ', 'ş')
df_new_data['Metin_Veri'] = df_new_data['Metin_Veri'].str.replace('ý', 'i')
df_new_data['Metin_Veri'] = df_new_data['Metin_Veri'].str.replace('Ý', 'İ')
df_new_data['Metin_Veri'] = df_new_data['Metin_Veri'].str.replace('Þ', 'Ş')

# "Durum" sütunundaki değerleri uygun formata çevir
df_new_data['Kategori'] = df_new_data['Kategori'].replace({'Olumlu': 'pozitif', 'Olumsuz': 'negatif', 'Tarafsız': 'tarafsiz'})

# Metin_Veri ve Kategori değerlerini kullanarak yeni formata çevir
for index, row in df_new_data.iterrows():
    review = row['Metin_Veri']
    label = row['Kategori']

    # Yeni DataFrame'e ekle
    df_combined_previous = pd.concat([df_combined_previous, pd.DataFrame({'Metin_Veri': [review], 'Kategori': [label]})], ignore_index=True)

# Türkçe karakterleri düzelt
df_combined_previous['Metin_Veri'] = df_combined_previous['Metin_Veri'].str.replace('ð', 'ğ')
df_combined_previous['Metin_Veri'] = df_combined_previous['Metin_Veri'].str.replace('ý', 'ı')
df_combined_previous['Metin_Veri'] = df_combined_previous['Metin_Veri'].str.replace('þ', 'ş')
df_combined_previous['Metin_Veri'] = df_combined_previous['Metin_Veri'].str.replace('ý', 'i')
df_combined_previous['Metin_Veri'] = df_combined_previous['Metin_Veri'].str.replace('Ý', 'İ')
df_combined_previous['Metin_Veri'] = df_combined_previous['Metin_Veri'].str.replace('Þ', 'Ş')

# Yeni DataFrame'i CSV dosyasına yaz
df_combined_previous.to_csv('yorum_veri_seti_son.csv', index=False)

# İşlem bitince mesaj ver
print("CSV dosyası düzenlendi ve birleştirildi.")
