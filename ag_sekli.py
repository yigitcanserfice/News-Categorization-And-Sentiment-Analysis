from keras.models import load_model
from keras.utils import plot_model

# Eğitilmiş modeli yükle
model_path = "model/egitim.h5"
model = load_model(model_path)

# Modeli görselleştir
plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=True)
