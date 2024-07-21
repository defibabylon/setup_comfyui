import os
import subprocess
import requests
import zipfile
import shutil

def run_command(command):
    subprocess.run(command, shell=True, check=True)

def setup_comfyui():
    # Install dependencies
    run_command("pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu118")
    run_command("pip install git+https://github.com/huggingface/diffusers.git")

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

    # Download and place models
    os.makedirs("models/checkpoints", exist_ok=True)
    os.makedirs("models/controlnet/sdxl", exist_ok=True)
    os.makedirs("custom_nodes/ComfyUI_IPAdapter_plus/models", exist_ok=True)
    os.makedirs("models/clip_vision", exist_ok=True)

    # Download checkpoint (example)
    checkpoint_url = "https://example.com/path/to/wildcardx-xl-turbo.safetensors"
    download_file(checkpoint_url, "models/checkpoints/wildcardx-xl-turbo.safetensors")

    # Download controlnet model
    controlnet_url = "https://huggingface.co/TheMistoAI/MistoLine/resolve/main/mistoLine_rank256.safetensors"
    download_file(controlnet_url, "models/controlnet/sdxl/mistoLine_rank256.safetensors")

    # Download IP Adapter model
    ip_adapter_url = "https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/ip-adapter-plus_sdxl_vit-h.safetensors"
    download_file(ip_adapter_url, "custom_nodes/ComfyUI_IPAdapter_plus/models/ip-adapter-plus_sdxl_vit-h.safetensors")

    # Download CLIP vision models
    clip_vision_urls = [
        "https://huggingface.co/laion/CLIP-ViT-H-14-laion2B-s32B-b79K/resolve/main/model.safetensors",
        "https://huggingface.co/laion/CLIP-ViT-bigG-14-laion2B-39B-b160k/resolve/main/model.safetensors"
    ]
    clip_vision_filenames = [
        "CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors",
        "CLIP-ViT-bigG-14-laion2B-39B-b160k.safetensors"
    ]
    for url, filename in zip(clip_vision_urls, clip_vision_filenames):
        download_file(url, f"models/clip_vision/{filename}")

    # Install ComfyUI Essentials
    run_command("git clone https://github.com/cubiq/ComfyUI_essentials.git custom_nodes/ComfyUI_essentials")

    print("Setup complete. You can now run ComfyUI.")

def download_file(url, destination):
    response = requests.get(url)
    with open(destination, 'wb') as f:
        f.write(response.content)

def start_comfyui():
    os.chdir("/root/ComfyUI")  # Adjust this path if ComfyUI is installed elsewhere
    run_command("python main.py --listen 0.0.0.0 --port 8188")

if __name__ == "__main__":
    setup_comfyui()
    start_comfyui()


