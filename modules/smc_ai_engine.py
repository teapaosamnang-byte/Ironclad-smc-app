import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout
from sklearn.preprocessing import StandardScaler

MODEL_FILE = os.path.join(os.path.dirname(__file__), "..", "configs", "smc_deep_learning_model.h5")
SCALER_FILE = os.path.join(os.path.dirname(__file__), "..", "configs", "smc_scaler.npy")

def build_deep_learning_model(input_dim):
    """សាងສង់โครงสร้าง Neural Network (Deep Learning) សម្រាប់ចម្រោះសញ្ញា"""
    model = Sequential([
        Dense(64, activation='relu', input_dim=input_dim),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dropout(0.2),
        Dense(1, activation='sigmoid') # លទ្ធផលចេញជាភាគរយប្រូបាប៊ីលីតេ (0 ដល់ 1)
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def train_ai_filter(X_train, y_train):
    """បង្ហាត់ម៉ូដែល Deep Learning ជាមួយទិន្នន័យប្រវត្តិសាស្ត្រ"""
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_train)
    
    model = build_deep_learning_model(input_dim=X_scaled.shape[1])
    
    # Train ម៉ូដែល
    model.fit(X_scaled, y_train, epochs=50, batch_size=16, verbose=0)
    
    # រក្សាទុក Model និង Scaler ទុកប្រើប្រាស់ពេលក្រោយ
    os.makedirs(os.path.dirname(MODEL_FILE), exist_ok=True)
    model.save(MODEL_FILE)
    np.save(SCALER_FILE, [scaler.mean_, scaler.scale_])
    
    return model

def evaluate_signal_with_ai(signal_features):
    """
    តម្រងចុងក្រោយ (External AI Filter):
    ពិនិត្យមើលលក្ខណៈសម្បត្តិបច្ចុប្បន្ន ថាាតើគួរអនុញ្ញាតឱ្យចេញសញ្ញា ឬប្តូរទៅជា WAIT
    """
    if not os.path.exists(MODEL_FILE) or not os.path.exists(SCALER_FILE):
        # បើទាន់មាន Model ຜ່ານការ Train ទេ អនុញ្ញាតឱ្យឆ្លងកាត់ធម្មតា
        return True 

    try:
        model = load_model(MODEL_FILE)
        mean_scale, var_scale = np.load(SCALER_FILE, allow_pickle=True)
        
        # ធ្វើ Standardization លើទិន្នន័យបញ្ចូល
        features = np.array([signal_features])
        scaled_features = (features - mean_scale) / var_scale
        
        # រំពឹងទុកភាគរយជោគជ័យ (Prediction Probability)
        prediction = model.predict(scaled_features, verbose=0)[0][0]
        
        # កំណត់កម្រិត Threshold ឧទាហរណ៍៖ ត្រូវតែមានភាគរយជោគជ័យ > 0.65 (65%) ទើបអនុញ្ញាត
        if prediction >= 0.65:
            return True # អនុញ្ញាតឱ្យចេញសញ្ញា (BUY / SELL)
        else:
            return False # ហាមឃាត់ និងប្តូរលទ្ធផលមកជា WAIT ដើម្បីការពារទុន
            
    except Exception as e:
        print(f"AI Filter Error: {e}")
        return True