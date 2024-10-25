import torch
import curio
import socket
import prompts as prompts
from PIL import Image
from io import BytesIO
from transformers import LlavaNextProcessor, LlavaNextForConditionalGeneration

model_path = "your_model_path"
processor = LlavaNextProcessor.from_pretrained(model_path)

model = LlavaNextForConditionalGeneration.from_pretrained(model_path, torch_dtype=torch.float16, low_cpu_mem_usage=True) 
model.to("cuda:0")

def predict(input_prompt, image=None):
    """
    Generate a response based on the input prompt and optional image.

    Args:
        input_prompt (str): The text prompt to process.
        image (PIL.Image, optional): The image to include in the prompt. Defaults to None.

    Returns:
        str: The generated response from the model.
    """
    if image is not None:
        conversation = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": input_prompt},
                {"type": "image"},
            ],
        },
        ]
        prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
        inputs = processor(images=image, text=prompt, return_tensors="pt").to("cuda:0")
    else:    
        conversation = [
          {
              "role": "user",
              "content": [
                  {"type": "text", "text": input_prompt},
              ],
          },
        ]
        prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
        inputs = processor(text=prompt, return_tensors="pt").to("cuda:0")

    output = model.generate(**inputs, max_new_tokens=200)
    result = processor.decode(output[0], skip_special_tokens=True)
    end_index = result.find('[/INST]')
    if end_index != -1:
        result = result[end_index + len('[/INST]'):].strip()
    return result

async def handle_client(client_socket):
    """
    Handle incoming client connections and process requests.

    Args:
        client_socket (socket.socket): The socket connected to the client.
    """
    print("Client connected")
    try:
        while True:
            data = await curio.run_in_thread(client_socket.recv, 1024)
            if not data:
                break
            if data.startswith(b'IMAGE'):
                image_data = bytearray(data[len(b'IMAGE'):])
                while True:
                    chunk = await curio.run_in_thread(client_socket.recv, 4096)
                    if b'END' in chunk:
                        image_data += chunk[:chunk.find(b'END')]
                        break
                    image_data += chunk

                image = Image.open(BytesIO(image_data))
                user_prompt = prompts.asset_name_prompt
                result = predict(user_prompt, image)

            else:
                All_Defined_Prompts = [key for key in dir(prompts) if not key.startswith('__') and isinstance(getattr(prompts, key), str)]
                message = data.decode()
                print(f"Received: {message}")
                parts = message.split(":")
                mode = parts[0]
                object_name =  parts[1]
                if not mode.endswith('_prompt'): mode += '_prompt'
                if mode == "mass_prompt":
                    volume_str = parts[2]
                    volume = float(volume_str)
                    user_prompt = getattr(prompts, mode, None)
                    user_prompt = user_prompt.format(object=object_name, volume=volume)
                    result = predict(user_prompt)
                elif mode in All_Defined_Prompts:
                    user_prompt = getattr(prompts, mode, None)
                    user_prompt = user_prompt.format(object=object_name)
                    result = predict(user_prompt)
                else:
                    raise NotImplementedError(f"Please set prompt for {mode}")

            await curio.run_in_thread(client_socket.sendall, result.encode('utf-8'))
            
    except ValueError as e:
        print(f"Error parsing message: {e}")
        await curio.run_in_thread(client_socket.sendall, b"Error: Invalid message format")
    finally:
        client_socket.close()
        print("Client disconnected")

async def server(host, port):
    """
    Start the server to listen for incoming connections.

    Args:
        host (str): The hostname or IP address to bind the server.
        port (int): The port number to listen on.
    """
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind((host, port))
    listener.listen(5)
    print(f"Server started at {host}:{port}")
    
    while True:
        client_socket, addr = await curio.run_in_thread(listener.accept)
        print(f"Connection from {addr}")
        await curio.spawn(handle_client, client_socket)

if __name__ == "__main__":
    curio.run(server('0.0.0.0', 8000))