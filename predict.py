import numpy as np
import tensorflow
import pickle

model = tensorflow.keras.models.load_model('model.h5')
with open('encoder.h5' , 'wb') as f:
    label_encoder = pickle.load(f)

max_length = 32

def predict_password_strength(password):
    if len(password) > max_length:
        password = password[:max_length]
    
    password_encoded = np.array([ord(c) for c in password]).reshape(1, -1)
    password_encoded = np.pad(password_encoded, ((0, 0), (0, max_length - password_encoded.shape[1])), 'constant')
    prediction = model.predict(password_encoded)
    predicted_class = np.argmax(prediction)
    return label_encoder.inverse_transform([predicted_class])[0]