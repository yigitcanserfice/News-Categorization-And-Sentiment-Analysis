import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf

tf.compat.v1.disable_eager_execution()

# Kaydedilen modeli yükle
loaded_model = tf.keras.models.load_model('model/egitimHaber.h5')

# Veri setini yükleyip etiketleri sayısal hale getir
df = pd.read_csv('veri_seti_haberler.csv')
label_encoder = LabelEncoder()
df['Etiket'] = label_encoder.fit_transform(df['Kategori'])
num_classes = len(label_encoder.classes_)

# TF-IDF vektörleştirmeyi uygula
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(df['Metin_Veri'])


# Analiz yap ve sonuçları kaydet
def test_yazdır(model, vectorizer, yorumlar, dosya_adı='analiz_sonuçları.csv'):
    yorumlar_vec = vectorizer.transform(yorumlar)
    tahminler = model.predict(yorumlar_vec)
    tahmin_siniflar = tf.keras.backend.eval(tf.argmax(tahminler, axis=1))
    sonuçlar_df = pd.DataFrame({'Yorum': yorumlar, 'Tahmin Sınıfı': tahmin_siniflar})
    sonuçlar_df['Tahmin Etiketi'] = label_encoder.inverse_transform(tahmin_siniflar)
    sonuçlar_df.to_csv(dosya_adı, index=False)


# Dosyadan içeriği oku
with open("output.txt", "r", encoding="utf-8") as file:
    test_verisi = file.readlines()

test_yazdır(loaded_model, vectorizer, test_verisi, dosya_adı='testHaberSonucDeneme.csv')
