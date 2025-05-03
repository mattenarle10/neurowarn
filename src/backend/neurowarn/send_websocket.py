import websocket
import time
import json
import random



def open_websocket():
    ws_url = "ws://localhost:3000"
    # Open a WebSocket connection
    ws = websocket.WebSocket()
    ws.connect(ws_url)  # Replace ws_url with your WebSocket server URL
    return ws
    
    
# Assuming you already have the actual and predicted values from somewhere
def send_websocket_data(actual_c, pred_c, l1, l2,ws):


    try:
        # Get the actual and predicted data
        actual = actual_c
        predicted = pred_c
        # Prepare the data to be sent as a message
        
        safe_front = False
        
        if l1 +l2 > 0:
            safe_front = False
            
        else:
            safe_front = True
            
            
        # if not start_time.empty():
        #     time = start_time.get() * 1000000
            
        # else:
        #     time = -1
        
        message = {
            "actual": actual,
            "predicted": predicted,
            "safe": safe_front,
         
        }
        # Send the message via WebSocket
        ws.send(json.dumps(message))
        # print(f"Sent message: {message}")

        
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    return



# Replace 'ws://localhost:3000' with the actual WebSocket server URL


