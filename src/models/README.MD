# NeuroWarn BCI Models

This directory contains the machine learning models that power the NeuroWarn BCI system's prediction capabilities.

## Key Components

- LSTM Neural Networks - Deep learning models for EEG signal processing
- Data Preprocessing - Scalers and data transformation utilities
- Training Notebooks - Jupyter notebooks documenting the model development process
- Saved Models - Pre-trained models ready for deployment

## Model Files

- model.keras - Primary model used by the backend for real-time predictions
- best_model_weights.keras - Best performing model weights from training
- scaler.joblib - StandardScaler for normalizing input data

## Data Files

- emotiv_latest.csv - Latest collected EEG data
- emotiv_no_ohe.csv - EEG data without one-hot encoding
- testset.csv - Test dataset for model evaluation

## Data Flow

1. Data Collection: EEG data is collected from the Emotiv Insight headset via Cortex API
2. Preprocessing: Raw EEG data is normalized using StandardScaler
3. Model Input: Processed data is fed into the LSTM model in a sliding window of 5 time steps
4. Prediction: Model outputs command predictions (forward, left, right, backward)
5. Backend Integration: Predictions are sent to the backend for wheelchair control

## Using the Models

The models are automatically loaded by the backend's ai_copypaste.py file. The system:

1. Loads the pre-trained model and scaler
2. Collects EEG data in real-time
3. Processes the data using the scaler
4. Makes predictions using the model
5. Sends commands to control the wheelchair

## Model Architecture

The LSTM model architecture consists of:

- Input layer accepting 5 channels of EEG data
- LSTM layers for temporal pattern recognition
- Dense layers for classification
- Output layer predicting movement commands

## Training Process

To train a new model:

1. Collect EEG data using the Emotiv headset
2. Save the data to CSV format
3. Run the training notebook (LSTM_Model_Multi_Var.ipynb)
4. Save the resulting model as model.keras
5. Save the scaler as scaler.joblib