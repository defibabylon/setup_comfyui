import os
import subprocess
import logging
import sys

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
    
    # Ensure gdown is installed
    run_command("pip install gdown")
    
    # Restart the script to ensure all imports are available
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

    # Create model directories
    for dir in ["models/checkpoints", "models/controlnet/sdxl", 
                "custom_nodes/ComfyUI_IPAdapter_plus/models", "models/clip_vision", "models/upscale_models"]:
        os.makedirs(dir, exist_ok=True)

    # Import gdown here, after it's installed
    import gdown

    # Download models from Google Drive
    models = {
        "models/clip_vision/CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors": 
            "https://drive.google.com/uc?id=1HZygGQhhLr_w0jHqVfeYC4CwUdwbOk8N",
        "models/clip_vision/CLIP-ViT-bigG-14-laion2B-39B-b160k.safetensors": 
            "https://drive.google.com/uc?id=1mtd4NWSIu-pIqFBLld_DHUBlU9tHX-To",
        "models/upscale_models/ClearRealityV1.zip": 
            "https://drive.google.com/uc?id=1YOSexwiKYtb6BJ9iuIQXTNsTpNYNoJRh",
        "custom_nodes/ComfyUI_IPAdapter_plus/models/ip-adapter-plus_sdxl_vit-h.safetensors": 
            "https://drive.google.com/uc?id=1MFbP9_SwbylBUuv1W5RIleBUt5y8LBiX",
        "models/checkpoints/wildcardxXLTURBO_wildcardxXLTURBOV10.safetensors": 
            "https://drive.google.com/uc?id=1-6dyenykoPUwZa48PBNNIsRKHogvO-t0"
    }

    for dest, url in models.items():
        gdown.download(url, dest, quiet=False)

    # Extract ClearRealityV1.zip
    import zipfile
    with zipfile.ZipFile("models/upscale_models/ClearRealityV1.zip", 'r') as zip_ref:
        zip_ref.extractall("models/upscale_models")
    os.remove("models/upscale_models/ClearRealityV1.zip")

    # Install ComfyUI Essentials
    run_command("git clone https://github.com/cubiq/ComfyUI_essentials.git custom_nodes/ComfyUI_essentials")

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
