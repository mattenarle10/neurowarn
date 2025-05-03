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
