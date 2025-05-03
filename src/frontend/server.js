const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const path = require('path');

// Create an express app
const app = express();
const port = 3000;

// Serve static files from the 'public' folder
app.use(express.static(path.join(__dirname, 'public')));

// Define a route for the home page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Create an HTTP server
const server = http.createServer(app);

// Variable to store the latest message from WebSocket
let latestMessage = null;
let pred_command = null;
let safe = null;
let p_time = null;

// API route to send data to the client-side JavaScript
app.get('/api/data', (req, res) => {
    if (latestMessage) {
        const data = {
            message: latestMessage,
            actual_command: latestMessage,
            predicted_command: pred_command,
            obstacle: safe,
            timestamp: new Date().toISOString(),
            j_time: p_time,
        };
        res.json(data); // Send data as JSON if WebSocket message exists
    } else {
        res.status(404).json({ error: 'No data available' }); // No message received yet
    }
});

// Create a WebSocket server on top of the HTTP server
const wss = new WebSocket.Server({ server });

// Broadcast to all connected clients
function broadcast(data) {
    wss.clients.forEach(function each(client) {
        if (client.readyState === WebSocket.OPEN) {
            client.send(data);
        }
    });
}

// Handle WebSocket connection
wss.on('connection', (ws) => {
    console.log('New client connected');

    // Listen for messages from clients
    ws.on('message', (message) => {
        console.log(`Raw message received: ${message}`); // Log the raw message
    
        try {
            // Parse the message as a JSON object
            const parsed_message = JSON.parse(message);
            console.log('Parsed message:', parsed_message); // Log the parsed message
    
            // Extract the 'actual' field
            const actualData = parsed_message.actual;
            safe = parsed_message.safe;
            if(parsed_message["time"]){
                p_time = parsed_message.time;
            }
            
          

    
            // Log the actual data
            console.log(`Received: Actual -> ${actualData}`);
            broadcast(`Server: Received -> Actual: ${actualData}`);
    
            // API route to send data to the client-side JavaScript
            if(actualData === "f"){
                latestMessage = "forward";
                pred_command = "forward"

            }
            else if(actualData === "b"){
                latestMessage = "backward";
                pred_command = "backward"
            }

            else if(actualData === "s"){
                latestMessage = "stop";
                pred_command = "stop"
            }

            else if(actualData === "l"){
                latestMessage = "left";
                pred_command = "left"
            }

            else if(actualData === "r"){
                latestMessage = "right";
                pred_command = "right"
            }

            else{
                console.error("non-valid data for actual mental command");
            }
      
    
        } catch (error) {
            console.error('Error parsing WebSocket message:', error);
        }
    });
    

    // Handle WebSocket closed 
    ws.on('close', () => {
        console.log('Client disconnected');
    });
});

// Start the HTTP and WebSocket server
server.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});


