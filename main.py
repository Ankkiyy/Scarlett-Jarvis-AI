import os
import aiml
import asyncio
import websockets
import json  # Added import for JSON handling

brain_file = "aiml_brain.brn"

try:
    print("Initializing AIML kernel...")
    kernel = aiml.Kernel()
    
    if os.path.isfile(brain_file):
        print("Loading AIML brain from file...")
        kernel.bootstrap(brainFile=brain_file)
    else:
        print("Learning AIML from startup.xml...")
        kernel.learn("startup.xml")
        kernel.respond("load aiml")
        kernel.saveBrain(brain_file)
        print(f"AIML brain saved to {brain_file}")
except Exception as e:
    print(f"Error during AIML kernel initialization: {e}")

# Replace time.clock() with time.time() if AIML kernel was initialized successfully
if 'kernel' in locals() and isinstance(kernel, aiml.Kernel):
    try:
        file_path = "/data/data/com.termux/files/usr/lib/python3.11/site-packages/aiml/Kernel.py"
        os.system(f"sed -i 's/time\.clock()/time.time()/g' {file_path}")
        print("time.clock() replaced with time.time() successfully.")
    except Exception as e:
        print(f"Error replacing time.clock(): {e}")

async def handle_websocket(websocket, path):
    async for message in websocket:
        user_input = message
        aiml_response = kernel.respond(user_input)
        response_data = {'response': aiml_response}
        
        print(f"Received message: {user_input}")
        print(f"AIML Response: {aiml_response}")
        
        try:
            # Convert response_data to JSON before sending
            response_json = json.dumps(response_data)
            await websocket.send(response_json)
            print("Response sent successfully.")
        except Exception as e:
            print(f"Error sending response: {e}")

if __name__ == '__main__':
    print("Starting WebSocket server...")
    start_server = websockets.serve(handle_websocket, "localhost", 3000)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
