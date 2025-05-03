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
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## ▶️ Running the System

```bash
# Start the main program
python wheelchair_drive.py
```
