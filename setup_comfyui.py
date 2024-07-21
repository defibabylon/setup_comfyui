import os
import subprocess
import logging
import sys
import json

logging.basicConfig(level=logging.INFO)

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {command}")
        logging.error(e)
        raise

def install_requirements():
    logging.info("Installing requirements")
    run_command("pip install -r requirements.txt")
    run_command("pip install gdown")
    os.execv(sys.executable, ['python'] + sys.argv)

def setup_comfyui():
    logging.info("Starting ComfyUI setup")
    
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
    
    # Use ComfyUI Manager to install custom nodes
    custom_nodes = [
        "ComfyUI_IPAdapter_plus",
        "ComfyUI_essentials"
    ]
    
    for node in custom_nodes:
        run_command(f"python custom_nodes/ComfyUI-Manager/cm.py --install {node}")
    
    # Download models using ComfyUI Manager
    models = {
        "checkpoints": ["wildcardxXLTURBO_wildcardxXLTURBOV10"],
        "clip_vision": ["CLIP-ViT-H-14-laion2B-s32B-b79K", "CLIP-ViT-bigG-14-laion2B-39B-b160k"],
        "upscale_models": ["4x-ClearRealityV1"],
        "controlnet": ["controlnet-mid-sd15-diffusers-v1"]
    }
    
    for model_type, model_list in models.items():
        for model in model_list:
            run_command(f"python custom_nodes/ComfyUI-Manager/cm.py --install-model {model_type}/{model}")
    
    # Download IP-Adapter model separately as it might not be in the default model list
    import gdown
    gdown.download("https://drive.google.com/uc?id=1MFbP9_SwbylBUuv1W5RIleBUt5y8LBiX", 
                   "custom_nodes/ComfyUI_IPAdapter_plus/models/ip-adapter-plus_sdxl_vit-h.safetensors", quiet=False)
    
    logging.info("Setup complete. You can now run ComfyUI.")

def start_comfyui():
    logging.info("Starting ComfyUI")
    os.chdir("/root/ComfyUI")  # Adjust this path if ComfyUI is installed elsewhere
    run_command("python main.py --listen 0.0.0.0 --port 8188")

if __name__ == "__main__":
    try:
        if 'gdown' not in sys.modules:
            install_requirements()
        setup_comfyui()
        start_comfyui()
    except Exception as e:
        logging.error(f"Setup failed: {e}")
