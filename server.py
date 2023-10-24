import asyncio
import websockets
import aiml
import subprocess
import os

# Initialize AIML kernel
kernel = aiml.Kernel()

# Check if the AIML brain file exists
brain_file = "aiml_brain.brn"

if os.path.isfile(brain_file):
    # If the brain file exists, load it
    kernel.bootstrap(brainFile=brain_file)
else:
    # If the brain file doesn't exist, load AIML files and save the brain
    kernel.learn("startup.xml")
    kernel.respond("load aiml")
    kernel.saveBrain(brain_file)
    print(f"AIML brain saved to {brain_file}")

async def respond(websocket, path):
    while True:
        user_input = await websocket.recv()
        if user_input.strip().lower() == "exit":
            await websocket.send("Goodbye!")
            break
        aiml_response = kernel.respond(user_input)
        if "python" in aiml_response:
            script = aiml_response.split("python")[1].strip()
            subprocess.call(script, shell=True)
        else:
            await websocket.send(aiml_response)

print("Listening on port 3000 : http://localhost:3000")
start_server = websockets.serve(respond, "localhost", 3000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
