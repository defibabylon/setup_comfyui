import os
import subprocess
import logging
import sys
from tqdm import tqdm
import time
import requests
import gdown

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_command(command, desc=None):
    with tqdm(total=1, desc=desc, bar_format='{l_bar}{bar}', disable=desc is None) as pbar:
        try:
            subprocess.run(command, shell=True, check=True)
            pbar.update(1)
        except subprocess.CalledProcessError as e:
            logging.error(f"Command failed: {command}")
            logging.error(e)
            raise

def download_file(url, dest_path, desc=None):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(dest_path, 'wb') as file, tqdm(
        desc=desc,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            pbar.update(size)

def download_gdrive_file(file_id, dest_path, desc=None):
    gdown.download(f"https://drive.google.com/uc?id={file_id}", dest_path, quiet=False)

def setup_comfyui():
    logging.info("Starting ComfyUI setup")
    
    # Clone ComfyUI repository
    run_command("git clone https://github.com/comfyanonymous/ComfyUI.git", "Cloning ComfyUI repository")
    os.chdir("ComfyUI")
    
    # Install ComfyUI requirements
    run_command("pip install -r requirements.txt", "Installing ComfyUI requirements")
    
    # Install ComfyUI Manager
    os.makedirs("custom_nodes", exist_ok=True)
    os.chdir("custom_nodes")
    run_command("git clone https://github.com/ltdrdata/ComfyUI-Manager.git", "Cloning ComfyUI Manager")
    os.chdir("..")
    
    # Create model directories
    for dir in ["models/checkpoints", "models/controlnet/sdxl", 
                "models/clip_vision", "models/ipadapter", "models/upscale_models"]:
        os.makedirs(dir, exist_ok=True)
    
    # Download WildcardXL Turbo model
    download_gdrive_file("1-6dyenykoPUwZa48PBNNIsRKHogvO-t0", 
                         "models/checkpoints/wildcardxXLTURBO_wildcardxXLTURBOV10.safetensors",
                         "Downloading WildcardXL Turbo model")
    
    # Download mistoLine_rank256.safetensors
    download_file("https://huggingface.co/TheMistoAI/MistoLine/resolve/main/mistoLine_rank256.safetensors",
                  "models/controlnet/sdxl/mistoLine_rank256.safetensors",
                  "Downloading mistoLine_rank256.safetensors")
    
    # Download models
    clip_models = [
        ("https://huggingface.co/laion/CLIP-ViT-H-14-laion2B-s32B-b79K/resolve/main/model.safetensors",
         "models/clip_vision/CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors"),
        ("https://huggingface.co/laion/CLIP-ViT-bigG-14-laion2B-39B-b160k/resolve/main/model.safetensors",
         "models/clip_vision/CLIP-ViT-bigG-14-laion2B-39B-b160k.safetensors")
    ]
    
    for url, path in clip_models:
        download_file(url, path, f"Downloading {os.path.basename(path)}")
    
    # Download IPAdapter model (example)
    download_gdrive_file("1MFbP9_SwbylBUuv1W5RIleBUt5y8LBiX", 
                         "models/ipadapter/ip-adapter-plus_sdxl_vit-h.safetensors",
                         "Downloading IPAdapter model")
    
    # Install custom nodes
    custom_nodes = [
        "ComfyUI_IPAdapter_plus",
        "ComfyUI_essentials",
        "ComfyUI-Advanced-ControlNet",
        "ComfyUI-Impact-Pack",
        "ComfyUI-AnimateDiff-Evolved",
        "ComfyUI-VideoHelperSuite",
        "ComfyUI-Frame-Interpolation",
        "ComfyUI-Manager",
        "ComfyUI-Custom-Scripts",
        "ComfyUI-Noise",
        "MTB-ComfyUI-nodes"
    ]
    
    for node in tqdm(custom_nodes, desc="Installing custom nodes"):
        try:
            if os.path.exists("custom_nodes/ComfyUI-Manager/custom_nodes_picker.py"):
                run_command(f"python custom_nodes/ComfyUI-Manager/custom_nodes_picker.py --install {node}")
            elif os.path.exists("custom_nodes/ComfyUI-Manager/cm.py"):
                run_command(f"python custom_nodes/ComfyUI-Manager/cm.py --install {node}")
            else:
                logging.warning(f"ComfyUI Manager installation script not found. Skipping installation of {node}")
            time.sleep(1)
        except Exception as e:
            logging.error(f"Failed to install {node}: {e}")
    
    logging.info("Setup complete. You can now run ComfyUI.")

def start_comfyui():
    logging.info("Starting ComfyUI")
    comfyui_path = os.path.join(os.getcwd(), "ComfyUI")
    if not os.path.exists(comfyui_path):
        comfyui_path = os.path.join(os.path.dirname(os.getcwd()), "ComfyUI")
    
    if os.path.exists(comfyui_path):
        os.chdir(comfyui_path)
        run_command("python main.py --listen 0.0.0.0 --port 8188")
    else:
        logging.error(f"ComfyUI directory not found. Expected at: {comfyui_path}")
        raise FileNotFoundError(f"ComfyUI directory not found. Expected at: {comfyui_path}")

if __name__ == "__main__":
    try:
        with tqdm(total=3, desc="Overall Progress", position=0) as pbar:
            setup_comfyui()
            pbar.update(2)
            
            logging.info("Setup completed successfully")
            pbar.update(1)
            
            logging.info("Starting ComfyUI...")
            start_comfyui()
    except Exception as e:
        logging.error(f"Setup failed: {e}")
        sys.exit(1)
