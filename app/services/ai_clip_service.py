import torch
from PIL import Image
import clip
from torchvision import transforms

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def get_image_embedding(image_path: str):
    
    try:
        image = Image.open(image_path).convert("RGB")
        image = preprocess(image).unsqueeze(0).to(device)

        with torch.no_grad():
            image_features = model.encode_image(image)

        return image_features.cpu().numpy().tolist()[0] 
    
    except Exception as e:
        raise RuntimeError(f"Error processing image: {str(e)}")