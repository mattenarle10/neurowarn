from cortex import Cortex
# import serial
import time
import joblib
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Reshape
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Dense, BatchNormalization, SpatialDropout1D
from tensorflow.keras.regularizers import l2
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
import time
import csv
import os
import pandas as pd

class Subcribe():
    """
    A class to subscribe data stream.

    Attributes
    ----------
    c : Cortex
        Cortex communicate with Emotiv Cortex Service

    Methods
    -------
    start():
        start data subscribing process.
    sub(streams):
        To subscribe to one or more data streams.
    on_new_data_labels(*args, **kwargs):
        To handle data labels of subscribed data 
    on_new_eeg_data(*args, **kwargs):
        To handle eeg data emitted from Cortex
    on_new_mot_data(*args, **kwargs):
        To handle motion data emitted from Cortex
    on_new_dev_data(*args, **kwargs):
        To handle device information data emitted from Cortex
    on_new_met_data(*args, **kwargs):
        To handle performance metrics data emitted from Cortex
    on_new_pow_data(*args, **kwargs):
        To handle band power data emitted from Cortex
    """
    window = np.empty((1,0,25))
    
    # Check if the model file exists
    if os.path.exists('model.keras'):
        loaded_model = load_model('model.keras')
    else:
        print("Error: 'model.keras' not found.")

    # Check if the scaler file exists
    if os.path.exists('scaler.joblib'):
        scaler = joblib.load('scaler.joblib')
    else:
        print("Error: 'scaler.joblib' not found.")

    def __init__(self, app_client_id, app_client_secret, **kwargs):
        """
        Constructs cortex client and bind a function to handle subscribed data streams
        If you do not want to log request and response message , set debug_mode = False. The default is True
        """
        print("Subscribe _init_")
        self.c = Cortex(app_client_id, app_client_secret, debug_mode=False, **kwargs)
        self.c.bind(create_session_done=self.on_create_session_done)
        self.c.bind(new_mot_data=self.on_new_mot_data)
        self.c.bind(inform_error=self.on_inform_error)
        self.c.bind(new_com_data=self.on_new_com_data)
        self.c.bind(new_pow_data=self.on_new_pow_data)
        # self.ser = serial
        self.action = ''
        self.motion = {}
        self.motion_prev = 0
        self.prev_value = False

    def start(self, streams, headsetId='', profile_name = ''):
        """
        To start data subscribing process as below workflow
        (1)check access right -> authorize -> connect headset->create session
        (2) subscribe streams data
        'eeg': EEG
        'mot' : Motion
        'dev' : Device information
        'met' : Performance metric
        'pow' : Band power
        'eq' : EEQ Quality

        Parameters
        ----------
        streams : list, required
            list of streams. For example, ['eeg', 'mot']
        headsetId: string , optional
             id of wanted headet which you want to work with it.
             If the headsetId is empty, the first headset in list will be set as wanted headset
        Returns
        -------
        None
        """
        if profile_name == '':
            raise ValueError('Empty profile_name. The profile_name cannot be empty.')

        self.profile_name = profile_name
        self.c.set_wanted_profile(profile_name)
        
        self.streams = streams

        if headsetId != '':
            self.c.set_wanted_headset(headsetId)

        self.c.open()

    def sub(self, streams):
        """
        To subscribe to one or more data streams
        'eeg': EEG
        'mot' : Motion
        'dev' : Device information
        'met' : Performance metric
        'pow' : Band power

        Parameters
        ----------
        streams : list, required
            list of streams. For example, ['eeg', 'mot']

        Returns
        -------
        None
        """
        self.c.sub_request(streams)

    def unsub(self, streams):
        """
        To unsubscribe to one or more data streams
        'eeg': EEG
        'mot' : Motion
        'dev' : Device information
        'met' : Performance metric
        'pow' : Band power

        Parameters
        ----------
        streams : list, required
            list of streams. For example, ['eeg', 'mot']

        Returns
        -------
        None
        """
        self.c.unsub_request(streams)

    def on_new_pow_data(self, *args, **kwargs):
        data = kwargs.get('data')
        # input_data = np.array([[[data['pow'][0], data['pow'][1],data['pow'][2],data['pow'][3],data['pow'][4],data['pow'][5],data['pow'][6],data['pow'][7],data['pow'][8],data['pow'][9],data['pow'][10],data['pow'][11],data['pow'][12],data['pow'][13],data['pow'][14],data['pow'][15],data['pow'][16],data['pow'][17],data['pow'][18],data['pow'][19],data['pow'][20],data['pow'][21],data['pow'][22],data['pow'][23],data['pow'][24]],
        #                [data['pow'][0], data['pow'][1],data['pow'][2],data['pow'][3],data['pow'][4],data['pow'][5],data['pow'][6],data['pow'][7],data['pow'][8],data['pow'][9],data['pow'][10],data['pow'][11],data['pow'][12],data['pow'][13],data['pow'][14],data['pow'][15],data['pow'][16],data['pow'][17],data['pow'][18],data['pow'][19],data['pow'][20],data['pow'][21],data['pow'][22],data['pow'][23],data['pow'][24]],
        #                [data['pow'][0], data['pow'][1],data['pow'][2],data['pow'][3],data['pow'][4],data['pow'][5],data['pow'][6],data['pow'][7],data['pow'][8],data['pow'][9],data['pow'][10],data['pow'][11],data['pow'][12],data['pow'][13],data['pow'][14],data['pow'][15],data['pow'][16],data['pow'][17],data['pow'][18],data['pow'][19],data['pow'][20],data['pow'][21],data['pow'][22],data['pow'][23],data['pow'][24]],
        #                [data['pow'][0], data['pow'][1],data['pow'][2],data['pow'][3],data['pow'][4],data['pow'][5],data['pow'][6],data['pow'][7],data['pow'][8],data['pow'][9],data['pow'][10],data['pow'][11],data['pow'][12],data['pow'][13],data['pow'][14],data['pow'][15],data['pow'][16],data['pow'][17],data['pow'][18],data['pow'][19],data['pow'][20],data['pow'][21],data['pow'][22],data['pow'][23],data['pow'][24]],
        #                [data['pow'][0], data['pow'][1],data['pow'][2],data['pow'][3],data['pow'][4],data['pow'][5],data['pow'][6],data['pow'][7],data['pow'][8],data['pow'][9],data['pow'][10],data['pow'][11],data['pow'][12],data['pow'][13],data['pow'][14],data['pow'][15],data['pow'][16],data['pow'][17],data['pow'][18],data['pow'][19],data['pow'][20],data['pow'][21],data['pow'][22],data['pow'][23],data['pow'][24]]]])
        
        input_data = np.array([[[data['pow'][0], data['pow'][1],data['pow'][2],data['pow'][3],data['pow'][4],data['pow'][5],data['pow'][6],data['pow'][7],data['pow'][8],data['pow'][9],data['pow'][10],data['pow'][11],data['pow'][12],data['pow'][13],data['pow'][14],data['pow'][15],data['pow'][16],data['pow'][17],data['pow'][18],data['pow'][19],data['pow'][20],data['pow'][21],data['pow'][22],data['pow'][23],data['pow'][24]]]])
        self.window = np.append(self.window, input_data, axis=1)
        # Process the prediction
        self.get_data_of_pow(self.window)

    def get_data_of_pow(self, input_data):
        # print(self.window) <- Debugging
        # print(len(input_data[0])) < - Debugging

        if len(input_data[0]) == 5:

            csv_file = 'real_time_data.csv'
            if self.rows_checker(csv_file): #Predict if no. of rows was met

                if os.path.exists('model.keras') and os.path.exists('scaler.joblib'):
                    self.prediction(input_data)
                else:
                    self.train_model()
                    
            else:  #Otherwise just collect data and append to csv
                reshaped_data = input_data.reshape(-1, input_data.shape[-1])
                final_row = [list(row) + [self.get_active_command()] for row in reshaped_data]
                header = ['Theta_AF3', 'Theta_T7', 'Theta_PZ', 'Theta_T8', 'Theta_AF4', 'Alpha_AF3', 'Alpha_T7', 'Alpha_PZ', 'Alpha_T8', 'Alpha_AF4', 'BetaL_AF3', 'BetaL_T7', 'BetaL_PZ', 'BetaL_T8', 'BetaL_AF4', 'BetaH_AF3', 'BetaH_T7', 'BetaH_PZ', 'BetaH_T8', 'BetaH_AF4', 'Gamma_AF3', 'Gamma_T7', 'Gamma_PZ', 'Gamma_T8', 'Gamma_AF4', 'Command']

                file_exists = os.path.exists(csv_file)

                # Append data to CSV file
                try:
                    with open(csv_file, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        if not file_exists:
                            writer.writerow(header)  # Write header only if file is new
                        writer.writerows(final_row)  # Append reshaped data
                    print("Data successfully appended to data.csv.")
                except PermissionError:
                    print("Permission denied. Ensure the file is not open in another program and you have write permissions.")
                self.window = np.empty((1,0,25))
    
    def prediction(self, input_data):

        new_data_scaled = self.scaler.transform(input_data.reshape(-1, input_data.shape[-1])).reshape(input_data.shape)
        # Make predictions
        predictions = self.loaded_model.predict(new_data_scaled)
        # Get the predicted classes
        predicted_classes = np.argmax(predictions, axis=1)
        self.window = self.window[:,1:,:]
        # Print the predictions
        
        print("Input Data: ", input_data)
        print("Prediction:", predicted_classes, self.get_active_command())

    def get_active_command(self):
        active_command = 0
        if self.action == 'neutral':
            active_command = 0
        elif self.action == 'push':
            active_command = 1                
        elif self.action == 'pull':
            active_command = 2
        return active_command
    
    def train_model(self):
        # Load the data
        data = pd.read_csv("real_time_data.csv")

        # Drop rows with any non-numeric data
        data = data.apply(pd.to_numeric, errors='coerce').dropna()

        # Separate features and target
        features = data.iloc[:, :25].values
        target = data.iloc[:, 25].values

        # Scale features for better LSTM performance
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)

        # Save the fitted scaler for future use
        joblib.dump(scaler, 'scaler.joblib')

        # Function to create sequences with a sliding window
        def create_sequences(features, target, window_size=5):
            X, y = [], []
            for i in range(len(features) - window_size):
                X.append(features[i:i + window_size])
                y.append(target[i + window_size])
            return np.array(X), np.array(y)

        # Create sequences
        X, y = create_sequences(features_scaled, target, window_size=5)

        # One-hot encode target for categorical prediction
        y = to_categorical(y, num_classes=3)

        # Split data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Hyperparameters
        kernel_regularizer_val = 0.0001
        regularization_dropout_rate = 0.2  # Adjusted dropout rate

        # Define the LSTM model with L2 regularization and batch normalization
        model = Sequential()

        # First LSTM layer with increased units and batch normalization
        model.add(LSTM(128, input_shape=(X_train.shape[1], X_train.shape[2]), return_sequences=True, 
                    kernel_regularizer=l2(kernel_regularizer_val), recurrent_dropout=0.2))
        model.add(BatchNormalization())
        model.add(SpatialDropout1D(regularization_dropout_rate))

        # Second LSTM layer with recurrent dropout
        model.add(LSTM(64, return_sequences=False, kernel_regularizer=l2(kernel_regularizer_val), recurrent_dropout=0.2))
        model.add(BatchNormalization())

        # Dense layer with increased units
        model.add(Dense(32, activation='relu', kernel_regularizer=l2(kernel_regularizer_val)))
        model.add(Dropout(regularization_dropout_rate))

        # Output layer
        model.add(Dense(3, activation='softmax'))

        # Compile the model
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        # Set up a checkpoint to save the best model based on validation accuracy
        checkpoint = ModelCheckpoint('model.keras', monitor='val_accuracy', save_best_only=True, mode='max')

        # Set up early stopping to prevent overfitting
        early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

        # Train the model with the checkpoint and early stopping callbacks
        history = model.fit(X_train, y_train, epochs=100, batch_size=16, 
                            validation_data=(X_test, y_test), 
                            callbacks=[checkpoint, early_stopping])

        print("Training Complete!")
        
    # Function to check if the rows in the file
    def rows_checker(self, file_path):
        if not os.path.exists(file_path):
            return False  # File does not exist

        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            row_count = sum(1 for row in reader)
            
        return row_count >= 200 #Specify no. of rows in csv  
    
    def on_new_com_data(self, *args, **kwargs):
        data = kwargs.get('data')
        self.action = data['action']

        # if data:
        #     print(data)
        #     # self.action = data['action']
        #     # if not self.prev_value:
        #     #     self.motion_prev = self.motion[4]
        #     #     self.prev_value = True
        #     #     print("initttt")
            
        #     # if True: #for left and right
        #     #     if(self.motion[4] < .5 and self.motion[4] > -.2):
        #     #         self.send_command('s') 
        #     #     elif(self.motion[4] < 0):
        #     #         self.send_command('l') 
        #     #     else:
        #     #         self.send_command('r') 
                
        #     #     print(self.motion[4])        
          
        #     # elif self.action == "pull":
        #     #     self.send_command('b')  # Move forward with speed 100
            
        #     # elif(self.action == "push"):
        #     #     self.send_command('f')  # Move forward with speed 100
        #     # else:
        #     #     self.send_command('s')  # Move forward with speed 100
            
        # else:
        #     print("No data received")

    def on_new_mot_data(self, *args, **kwargs):
        """
        To handle motion data emitted from Cortex

        Returns
        -------
        data: dictionary
             The values in the array motion match the labels in the array labels return at on_new_data_labels
        For example: {'mot': [33, 0, 0.493859, 0.40625, 0.46875, -0.609375, 0.968765, 0.187503, -0.250004, -76.563667, -19.584995, 38.281834], 'time': 1627457508.2588}
        """
        data = kwargs.get('data')
        self.motion = data['mot']
        
    # callbacks functions
    def on_create_session_done(self, *args, **kwargs):
        print('on_create_session_done')

        # subscribe data 
        self.sub(self.streams)

    def on_inform_error(self, *args, **kwargs):
        error_data = kwargs.get('error_data')
        print(error_data)

    # def send_command(self,command):
    #     self.ser.write((command + '\n').encode())  # Send command to Arduino
    #     time.sleep(0.1)  # Short delay to ensure command is sent

# -----------------------------------------------------------
# 
# GETTING STARTED
#   - Please reference to https://emotiv.gitbook.io/cortex-api/ first.
#   - Connect your headset with dongle or bluetooth. You can see the headset via Emotiv Launcher
#   - Please make sure the your_app_client_id and your_app_client_secret are set before starting running.
#   - In the case you borrow license from others, you need to add license = "xxx-yyy-zzz" as init parameter
# RESULT
#   - the data labels will be retrieved at on_new_data_labels
#   - the data will be retreived at on_new_[dataStream]_data
# 
# -----------------------------------------------------------

# def main():

#     # Please fill your application clientId and clientSecret before running script
#     your_app_client_id = 'eOkUjdmtu8y4WK8n0gGFW4TwpS8h1xvchKb3Xp9g'
#     your_app_client_secret = 'lRNYu1TsAB9MmfcD7CqbEIlKbr14pI0cYwDvrgs8b5ZbLUMX2KPS5b1ryds23gIJRC38Cg8Up5N9BTHTK3kiK0W980ZTBqx913hoyeIsKfgoTuTki90x8zQztf3lUT7Z'

#     s = Subcribe(your_app_client_id, your_app_client_secret)

#     # list data streams
#     streams = ['eeg','mot','met','pow']
#     s.start(streams)

# if _name_ =='_main_':
#     main()

# -----------------------------------------------------------
emotiv.gitbook.io