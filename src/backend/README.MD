# 🔌 NeuroWarn BCI Backend

This directory contains the Python code that powers the brain-computer interface and hardware control system.

## 🧩 Key Components

- 🧠 **EEG Processing** - Processes brain signals from the Emotiv headset
- 🤖 **RNN Warning System** - Predicts potential hazards using neural networks
- 🔄 **Arduino Communication** - Controls the wheelchair motors and reads sensors
- 📡 **WebSocket Server** - Sends real-time data to the frontend dashboard

## 📁 File Structure

- `wheelchair_drive.py` - **MAIN PROGRAM** that coordinates all system components
- `cortex.py` - Interface with Emotiv Insight headset
- `sub_data.py` - Data subscription and processing
- `send_websocket.py` - Communication with web application
- `control.py` - Basic wheelchair control logic
- `ai_copypaste.py` - RNN model implementation

## 🚀 Setup & Installation

```bash
# Clone the repository
git clone https://github.com/mattenarle10/neurowarn.git
cd neurowarn/src/backend
```

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

```bash
# Install required Python packages
pip install -r requirements.txt
``` 

```bash
# Make sure your virtual environment is activated
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

# Go to the backend's neurowarn directory
cd neurowarn/src/backend/neurowarn

# Start the main program
python wheelchair_drive.py
```

## 🧠 Model Integration

The backend integrates with the LSTM neural network models to process EEG data and predict user intentions:

1. **Data Collection**: The system connects to the Emotiv Insight headset via the Cortex API
2. **Data Processing**: EEG data is collected in real-time and processed through the following steps:
   - Raw EEG data is collected from 5 channels (AF3, T7, PZ, T8, AF4)
   - Data is normalized using a pre-trained StandardScaler
   - Processed data is organized into a sliding window of 5 time steps
3. **Prediction**: The LSTM model predicts the user's intended movement direction
4. **Command Execution**: Predicted commands are sent to the Arduino to control the wheelchair

## 🔄 Data Flow

```
Emotiv Headset → Cortex API → Backend → LSTM Model → Command Prediction → Arduino → Wheelchair
                                  ↓
                              WebSocket
                                  ↓
                              Frontend
                          (Visualization)
```

## 🛠️ Hardware Communication

The backend communicates with the hardware components through:

1. **Serial Communication**: Commands are sent to the Arduino via serial connection
2. **Sensor Data**: LiDAR sensor data is received from the Arduino for obstacle detection
3. **WebSocket**: Real-time data is sent to the frontend for visualization

## ⚙️ Configuration

Before running the system, you need to:

1. Connect the Emotiv Insight headset and ensure it's paired
2. Connect the Arduino to the computer via USB
3. Configure the serial port in the wheelchair_drive.py script
4. Create a profile in the Emotiv app for consistent EEG readings

## 🧪 Testing

To test the system without a physical headset:

1. Use the test data provided in the `/src/models/testset.csv` file
2. Run the test script: `python test_prediction.py`
3. Monitor the console output for predicted commands
