import asyncio
import websockets
import redis

# Create a Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Set the Redis channel name
channel_name = 'your_channel'  # Replace with the actual Redis channel name

# Set the WebSocket server host and port
server_host = 'localhost'
server_port = 8765

# Set the WebSocket server URL
server_url = f'ws://{server_host}:{server_port}'

# Set the list of connected clients
clients = set()

# Function to handle incoming WebSocket connections
async def handle_connection(websocket, path):
    # Add the client to the list of connected clients
    clients.add(websocket)

    try:
        # Continuously listen for messages from the Redis channel
        pubsub = redis_client.pubsub()
        pubsub.subscribe(channel_name)
        
        for message in pubsub.listen():
            # Check if the message is from the subscribed channel
            if message['type'] == 'message' and message['channel'].decode() == channel_name:
                # Broadcast the message to all connected clients
                await broadcast_message(message['data'].decode())

    except websockets.exceptions.ConnectionClosedError:
        # Handle disconnection
        pass

    finally:
        # Remove the client from the list of connected clients
        clients.remove(websocket)

# Function to broadcast a message to all connected clients
async def broadcast_message(message):
    # Send the message to each connected client
    for client in clients:
        await client.send(message)

# Start the WebSocket server
start_server = websockets.serve(handle_connection, server_host, server_port)

# Run the event loop
async def run_server():
    await start_server
    await asyncio.gather(*asyncio.all_tasks())

# Run the WebSocket server
asyncio.run(run_server())
