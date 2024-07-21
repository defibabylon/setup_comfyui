import os
import subprocess
import requests
import logging

logging.basicConfig(level=logging.INFO)

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {command}")
        logging.error(e)
        raise

def setup_comfyui():
    logging.info("Starting ComfyUI setup")

    # Install dependencies
    run_command("pip install -r requirements.txt")

    # Clone ComfyUI repository
    run_command("git clone https://github.com/comfyanonymous/ComfyUI.git")
    os.chdir("ComfyUI")

    # Install ComfyUI requirements
    run_command("pip install -r requirements.txt")

    # Install ComfyUI Manager
    os.makedirs("custom_nodes", exist_ok=True)
    os.chdir("custom_nodes")
    run_command("git clone https://github.com/ltdrdata/ComfyUI-Manager.git")
    os.chdir("..")

    # Create model directories
    for dir in ["models/checkpoints", "models/controlnet/sdxl", 
                "custom_nodes/ComfyUI_IPAdapter_plus/models", "models/clip_vision"]:
        os.makedirs(dir, exist_ok=True)

    # Download models
    models = {
        "models/checkpoints/wildcardx-xl-turbo.safetensors": 
            "https://civitai.com/api/download/models/293331",  # Replace with actual URL
        "models/controlnet/sdxl/mistoLine_rank256.safetensors": 
            "https://huggingface.co/TheMistoAI/MistoLine/resolve/main/mistoLine_rank256.safetensors",
        "custom_nodes/ComfyUI_IPAdapter_plus/models/ip-adapter-plus_sdxl_vit-h.safetensors": 
            "https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/ip-adapter-plus_sdxl_vit-h.safetensors",
        "models/clip_vision/CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors": 
            "https://huggingface.co/laion/CLIP-ViT-H-14-laion2B-s32B-b79K/resolve/main/model.safetensors",
        "models/clip_vision/CLIP-ViT-bigG-14-laion2B-39B-b160k.safetensors": 
            "https://huggingface.co/laion/CLIP-ViT-bigG-14-laion2B-39B-b160k/resolve/main/model.safetensors"
    }

    for dest, url in models.items():
        download_file(url, dest)

    # Install ComfyUI Essentials
    run_command("git clone https://github.com/cubiq/ComfyUI_essentials.git custom_nodes/ComfyUI_essentials")

    logging.info("Setup complete. You can now run ComfyUI.")

def download_file(url, destination):
    logging.info(f"Downloading {url} to {destination}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(destination, 'wb') as f:
            f.write(response.content)
    except requests.RequestException as e:
        logging.error(f"Failed to download {url}: {e}")
        raise

def start_comfyui():
    logging.info("Starting ComfyUI")
    os.chdir("/root/ComfyUI")  # Adjust this path if ComfyUI is installed elsewhere
    run_command("python main.py --listen 0.0.0.0 --port 8188")

if __name__ == "__main__":
    try:
        setup_comfyui()
        start_comfyui()
    except Exception as e:
        logging.error(f"Setup failed: {e}")
