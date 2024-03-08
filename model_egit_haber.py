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
df = pd.read_csv('veri_seti_haberler.csv')

# Gelen verideki NaN değerlerini boş bir dize('') ile değiştir.
df['Metin_Veri'] = df['Metin_Veri'].fillna('')

# Etiketleri sayısal olarak kodla
label_encoder = LabelEncoder()
df['Etiket'] = label_encoder.fit_transform(df['Kategori'])
num_classes = len(label_encoder.classes_)  # Sınıf sayısını hesapla

print(df)

# Metin verilerini TF-IDF vektörlerine dönüştür.
vectorizer = TfidfVectorizer(
    max_features=5000)
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
model.fit(X_train, y_train_one_hot, epochs=10, batch_size=32, validation_data=(X_test, y_test_one_hot)) #epochs modelin tüm eğitim veri setini bir kez geçmesi. Burada 10 kez dönüyor. # batch_size Modelin güncellenmesinde kaç örnek kullanılacağını belirler.

# Eğitilen modeli test ederek tahminde bulun.
y_pred_prob = model.predict(X_test)
y_pred = tf.keras.backend.eval(tf.argmax(y_pred_prob, axis=1))

# Karmaşıklık Matrisini ısı haritası ile görselleştirme
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='g', cmap='Blues', xticklabels=label_encoder.classes_,
            yticklabels=label_encoder.classes_)
plt.xlabel('Tahmin')
plt.ylabel('Gerçek')
plt.title('Sınıflandırma Sonuçları')
plt.show()

# Test veri setindeki sınıf dağılımını görselleştrime
plt.figure(figsize=(6, 6))
plt.pie(y_test.value_counts(), labels=label_encoder.classes_, autopct='%1.1f%%', startangle=140)
plt.title('Sınıf Frekansları')
plt.show()

# Sınıflandırma Raporunu yazdırma
print("\nClassification Report:")
print(classification_report(y_test, y_pred))


def test_yazdır(model, vectorizer, haberler, dosya_adı):
    # Haberler TF-IDF vektörlerine çevir
    haberler_vector = vectorizer.transform(haberler)

    # Tahmini modeli kullanarak yap.
    tahmin = model.predict(haberler_vector)
    tahmin_sınıf = tf.keras.backend.eval(tf.argmax(tahmin, axis=1))

    # Tahmin sonuçlarını kaydet
    sonuçlar_df = pd.DataFrame({'Haber': haberler, 'Tahmin': tahmin_sınıf})

    # Sınıf etiketlerini ekleyebilirsiniz
    sonuçlar_df['Tahmin Etiketi'] = label_encoder.inverse_transform(tahmin_sınıf)

    # Sonuçları CSV dosyasına kaydet
    sonuçlar_df.to_csv(dosya_adı, index=False)


# Örnek Test kullanımı:
ornek_haberler = [
    "Samsung s23 akıllı telefonu kamera açısından bir çok yenilik getirdi. Rakip cihaz olarak görülen iphone 14 ile kıyaslandığında ise aradaki fark gözle görülür bir şekilde bariz."
    "Kripto para piyasalarında yaşanan yükselişle birlikte, öncü dijital para birimi Bitcoin, 60,000 dolar seviyesini aşarak tarihi bir rekora imza attı. Yatırımcılar, dijital varlıklara olan ilginin arttığı bu dönemde piyasadaki gelişmeleri yakından takip ediyor.",
    "Şehirde düzenlenen uluslararası film festivali başlıyor. Festival kapsamında dünya çapından öne çıkan bağımsız filmler, belgeseller ve sanatçıların katılımıyla sinemaseverlerle buluşacak.",
    "Futbol liginde zirve yarışı kızışıyor. İki önemli rakip takım arasındaki karşılaşma, şampiyonluk yolunda kritik bir maç olarak öne çıkıyor.",
    "Sevilen bir oyuncu, yeni bir sinema projesi için kamera karşısına geçti. Film, oyuncunun farklı bir karakterle izleyicilerle buluşacağı bir dram türünde olacak.",

    "Şehirdeki bir sanat galerisi, çağdaş heykel sanatının en iyi örneklerini sergilemek üzere kapılarını açtı. Sergide yer alan heykeller, sanatseverlere farklı malzeme ve tekniklerle oluşturulmuş çeşitli eserleri keşfetme fırsatı sunuyor.",
    "Klasik müzik tutkunları için düzenlenen bir festival, ünlü bir orkestra ve solistleri ağırlıyor. Festival kapsamında, klasik repertuarın yanı sıra çağdaş bestecilere ait eserler de dinleyicilerle buluşacak.",
    "Uluslararası bir tenis turnuvasında, sıralamada altta yer alan bir oyuncu, favori olarak gösterilen rakibini yenerek sürpriz bir zafer elde etti.",
    "Ülke, gelecek yıl düzenlenecek olan Yaz Olimpiyatları için hazırlıklarını hızlandırıyor. Sporcular, antrenman ve kamplarla kendilerini en iyi şekilde hazırlayarak uluslararası arenada ülkelerini temsil etmeye hazırlanıyor.",

    "Ülke, gelecek yıl düzenlenecek olan Yaz Olimpiyatları için hazırlıklarını hızlandırıyor. Sporcular, antrenman ve kamplarla kendilerini en iyi şekilde hazırlayarak uluslararası arenada ülkelerini temsil etmeye hazırlanıyor.",
    "Bir e-ticaret devi, yerel küçük işletmelerin dijital dönüşümüne katkı sağlamak amacıyla yeni bir destek programını başlattı. Program kapsamında, küçük işletmelere dijital pazarlama, e-ticaret platformlarına entegrasyon ve lojistik konularında eğitim ve kaynak sağlanacak.",
    "Sevilen bir oyuncu, yeni bir sinema projesi için kamera karşısına geçti. Film, oyuncunun farklı bir karakterle izleyicilerle buluşacağı bir dram türünde olacak.",
    "Bir moda ikonu, sürdürülebilir moda ve çevre dostu üretim konularında farkındalığı artırmak amacıyla bir kampanyaya katıldı. Moda dünyasındaki etkisiyle, çevre dostu ve adil üretim konularında toplumsal bilinç oluşturmayı hedefliyor."
]

test_yazdır(model, vectorizer, ornek_haberler, dosya_adı='haber_analizi.csv')

model.save("model/egitimHaber.h5")
