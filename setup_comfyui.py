import os
import subprocess
import logging
import sys
from tqdm import tqdm
import time

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

def install_requirements():
    logging.info("Installing requirements")
    run_command("pip install -r requirements.txt", "Installing pip requirements")
    run_command("pip install gdown tqdm", "Installing gdown and tqdm")
    logging.info("Requirements installed successfully")

def setup_comfyui():
    logging.info("Starting ComfyUI setup")
    
    run_command("git clone https://github.com/comfyanonymous/ComfyUI.git", "Cloning ComfyUI repository")
    os.chdir("ComfyUI")
    
    run_command("pip install -r requirements.txt", "Installing ComfyUI requirements")
    
    os.makedirs("custom_nodes", exist_ok=True)
    os.chdir("custom_nodes")
    run_command("git clone https://github.com/ltdrdata/ComfyUI-Manager.git", "Cloning ComfyUI Manager")
    os.chdir("..")
    
    custom_nodes = [
        "ComfyUI_IPAdapter_plus",
        "ComfyUI_essentials"
    ]
    
    for node in tqdm(custom_nodes, desc="Installing custom nodes"):
        run_command(f"python custom_nodes/ComfyUI-Manager/cm.py --install {node}")
        time.sleep(1)
    
    models = {
        "checkpoints": ["wildcardxXLTURBO_wildcardxXLTURBOV10"],
        "clip_vision": ["CLIP-ViT-H-14-laion2B-s32B-b79K", "CLIP-ViT-bigG-14-laion2B-39B-b160k"],
        "upscale_models": ["4x-ClearRealityV1"],
        "controlnet": ["controlnet-mid-sd15-diffusers-v1"]
    }
    
    total_models = sum(len(model_list) for model_list in models.values())
    with tqdm(total=total_models, desc="Downloading models") as pbar:
        for model_type, model_list in models.items():
            for model in model_list:
                run_command(f"python custom_nodes/ComfyUI-Manager/cm.py --install-model {model_type}/{model}")
                pbar.update(1)
                time.sleep(1)
    
    import gdown
    logging.info("Downloading IP-Adapter model")
    gdown.download("https://drive.google.com/uc?id=1MFbP9_SwbylBUuv1W5RIleBUt5y8LBiX", 
                   "custom_nodes/ComfyUI_IPAdapter_plus/models/ip-adapter-plus_sdxl_vit-h.safetensors", quiet=False)
    
    logging.info("Setup complete. You can now run ComfyUI.")

def start_comfyui():
    logging.info("Starting ComfyUI")
    os.chdir("/root/ComfyUI")  # Adjust this path if ComfyUI is installed elsewhere
    run_command("python main.py --listen 0.0.0.0 --port 8188")

if __name__ == "__main__":
    try:
        with tqdm(total=4, desc="Overall Progress", position=0) as pbar:
            install_requirements()
            pbar.update(1)
            
            setup_comfyui()
            pbar.update(2)
            
            logging.info("Setup completed successfully")
            pbar.update(1)
            
            logging.info("Starting ComfyUI...")
            start_comfyui()
    except Exception as e:
        logging.error(f"Setup failed: {e}")
