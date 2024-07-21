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
    
    # Download models
    clip_models = [
        ("https://huggingface.co/laion/CLIP-ViT-H-14-laion2B-s32B-b79K/resolve/main/model.safetensors",
         "models/clip_vision/CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors"),
        ("https://huggingface.co/laion/CLIP-ViT-bigG-14-laion2B-39B-b160k/resolve/main/model.safetensors",
         "models/clip_vision/CLIP-ViT-bigG-14-laion2B-39B-b160k.safetensors")
    ]
    
    for url, path in clip_models:
        download_file(url, path, f"Downloading {os.path.basename(path)}")
    
    # Download IPAdapter models (example)
    download_gdrive_file("1MFbP9_SwbylBUuv1W5RIleBUt5y8LBiX", 
                         "models/ipadapter/ip-adapter-plus_sdxl_vit-h.safetensors",
                         "Downloading IPAdapter model")
    
    # Install custom nodes
    custom_nodes = [
        "ComfyUI_IPAdapter_plus",
        "ComfyUI_essentials"
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
