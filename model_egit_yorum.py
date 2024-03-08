import pandas as pd
from keras.models import Sequential
from keras.utils import to_categorical
from keras.layers import Dense
from matplotlib import pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
import seaborn as sns

# TensorFlow'da eager execution'ı anında çalışmaması için devre dışı bırak.
tf.compat.v1.disable_eager_execution()

# Eğitim için kullanılacak yorum veri setlerini yükle
df = pd.read_csv('yorum_veri_seti_son.csv')

# Gelen verideki NaN değerlerini boş bir dize('') ile değiştir.
df['Metin_Veri'] = df['Metin_Veri'].fillna('')

# Etiketleri sayısal olarak kodla
label_encoder = LabelEncoder()
df['Etiket'] = label_encoder.fit_transform(df['Kategori'])
num_classes = len(label_encoder.classes_)  # Sınıf sayısını dinamik olarak al

print(df)

# Metin verilerini TF-IDF vektörlerine dönüştür.
vectorizer = TfidfVectorizer(
    max_features=5000)  # Sadece max_features kullanarak düzensiz matris kullanımını devre dışı bırak
X = vectorizer.fit_transform(df['Metin_Veri'])

# Veri setinin %80'i ile eğit %20'sini teste sok.
X_train, X_test, y_train, y_test = train_test_split(X, df['Etiket'], test_size=0.2, random_state=42,
                                                    stratify=df['Etiket'])

# Etiketlerin her birini vektöre(one-hot) çevir.
y_train_one_hot = to_categorical(y_train, num_classes=num_classes)
y_test_one_hot = to_categorical(y_test, num_classes=num_classes)

# Keras kütüphanesi ile modeli oluştur
model = Sequential()
model.add(Dense(128, input_dim=X.shape[1], activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(num_classes, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Modeli eğit
model.fit(X_train, y_train_one_hot, epochs=10, batch_size=32, validation_data=(X_test, y_test_one_hot))

# Eğitilen modeli test ederek tahminde bulun.
y_pred_prob = model.predict(X_test)
y_pred = tf.keras.backend.eval(tf.argmax(y_pred_prob, axis=1))

# Karmaşıklık Matrisini ısı haritası ile görselleştirme
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='g', cmap='Blues', xticklabels=label_encoder.classes_,
            yticklabels=label_encoder.classes_)
plt.xlabel('Tahmin Edilen')
plt.ylabel('Gerçek')
plt.title('Karmaşıklık Matrisi')
plt.show()

# Test veri setindeki sınıf dağılımını görselleştrime
plt.figure(figsize=(6, 6))
plt.pie(y_test.value_counts(), labels=label_encoder.classes_, autopct='%1.1f%%', startangle=140)
plt.title('Sınıf Dağılımı')
plt.show()

# Sınıflandırma Raporunu yazdırma
print("\nClassification Report:")
print(classification_report(y_test, y_pred))


def test_yazdır(model, vectorizer, yorumlar, dosya_adı):
    # Yorumları TF-IDF vektörlerine dönüştür
    yorumlar_vector = vectorizer.transform(yorumlar)

    # Tahmini modeli kullanarak yap.
    tahminler = model.predict(yorumlar_vector)
    tahmin_sınıf = tf.keras.backend.eval(tf.argmax(tahminler, axis=1))

    # Tahmin sonuçlarını kaydet
    sonuçlar_df = pd.DataFrame({'Yorum': yorumlar, 'Tahmin Sınıfı': tahmin_sınıf})

    # Sınıf etiketlerini ekleyebilirsiniz
    sonuçlar_df['Tahmin Etiketi'] = label_encoder.inverse_transform(tahmin_sınıf)

    # Sonuçları CSV dosyasına kaydet
    sonuçlar_df.to_csv(dosya_adı, index=False)


# Örnek Test kullanımı:
film_yorumları = [
    "Bu film beni derinden etkiledi. Oyunculuklar harika ve hikaye sürükleyiciydi. Sonunda gözlerimden yaşlar boşandı.",
    "Görsel efektler muazzam! Aksiyon sahneleri nefes kesiciydi. Ancak karakter gelişimi biraz eksik kalmış gibi geldi.",
    "Filmdeki mizahi unsurlar beni kahkahalara boğdu. Senaryo öyle zekice yazılmış ki, her anını keyifle izledim.",
    "Duygusal bir roller coaster! Karakterlerin duygularını hissetmek inanılmazdı. Ancak bazı sahneler biraz uzun sürdü.",
    "Bir başyapıt! Sanat yönetimi, müzik ve atmosfer filmi bambaşka bir seviyeye taşıdı. Ancak benim için bazı detaylar biraz belirsizdi."
]

test_yazdır(model, vectorizer, film_yorumları, dosya_adı='film_analizi.csv')

model.save("model/egitim.h5")
