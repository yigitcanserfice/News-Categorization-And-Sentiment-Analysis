import os
import pandas as pd

# Verileri çek
ana_dizin = 'Datasets/comments/'

# Tüm kategorileri oluştur
kategoriler = ['negatif', 'pozitif', 'tarafsiz']

# Boş listeler oluşturun
metin_verileri = []
kategori_listesi = []

# Her kategori dizinini dön
for kategori in kategoriler:
    kategori_dizini = os.path.join(ana_dizin, kategori)

    # Her TXT dosyasını dön
    for txt_dosyasi in os.listdir(kategori_dizini):
        txt_dosya_yolu = os.path.join(kategori_dizini, txt_dosyasi)

        try:
            # 'utf-8' formatında okuma
            with open(txt_dosya_yolu, 'r', encoding='utf-8') as dosya:
                metin_verisi = dosya.read().replace('\n', ' ')
                metin_verileri.append(metin_verisi)
                kategori_listesi.append(kategori)
        except UnicodeDecodeError:
            try:
                # 'latin-1' formatında okuma
                with open(txt_dosya_yolu, 'r', encoding='latin-1') as dosya:
                    metin_verisi = dosya.read().replace('\n', ' ')
                    metin_verileri.append(metin_verisi)
                    kategori_listesi.append(kategori)
            except UnicodeDecodeError:
                # 'ISO-8859-1' formatında okuma
                with open(txt_dosya_yolu, 'r', encoding='ISO-8859-1') as dosya:
                    metin_verisi = dosya.read().replace('\n', ' ')
                    metin_verileri.append(metin_verisi)
                    kategori_listesi.append(kategori)

# Listeleri DataFrame'e çevirin
df = pd.DataFrame({'Metin_Veri': metin_verileri, 'Kategori': kategori_listesi})

# Türkçe karakter sorununu çöz
df['Metin_Veri'] = df['Metin_Veri'].str.replace('ð', 'ğ')
df['Metin_Veri'] = df['Metin_Veri'].str.replace('ý', 'ı')
df['Metin_Veri'] = df['Metin_Veri'].str.replace('þ', 'ş')
df['Metin_Veri'] = df['Metin_Veri'].str.replace('ý', 'i')
df['Metin_Veri'] = df['Metin_Veri'].str.replace('Ý', 'İ')
df['Metin_Veri'] = df['Metin_Veri'].str.replace('Þ', 'Ş')

# DataFrame'i CSV dosyasına yaz
df.to_csv('veri_seti555.csv', index=False)
